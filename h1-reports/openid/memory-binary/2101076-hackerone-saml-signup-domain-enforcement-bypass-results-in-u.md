# SAML signup domain enforcement bypass via trailing control characters leading to unauthorized HackerOne source code access

## Metadata
- **Source:** HackerOne
- **Report:** 2101076 | https://hackerone.com/reports/2101076
- **Submitted:** 2023-08-08
- **Reporter:** 0xacb
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Authentication bypass, SAML enforcement bypass, Email validation bypass, Improper input normalization, Privilege escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
HackerOne's SAML signup domain enforcement can be bypassed by appending CRLF control characters (%0d%0a) to email addresses during registration. An attacker can create accounts using @hackerone.com email addresses, which normally redirect to SSO, and gain access to the HackerOne organization on PullRequest after email verification, exposing internal source code repositories.

## Attack scenario
1. Attacker identifies that @hackerone.com domain is protected by SAML enforcement and cannot be registered via normal signup
2. Attacker crafts POST request to /users endpoint with CRLF control characters appended to email parameter (email@hackerone.com%0d%0a)
3. Server's email validation logic fails to normalize input, treating CRLF-suffixed email as different from SAML-protected domain, allowing account creation
4. Attacker creates account but must complete email verification; sends verification email to target @hackerone.com user
5. When victim clicks verification link from their inbox, attacker gains authenticated access to the created account
6. Attacker logs in to PullRequest using 'Sign in with HackerOne' OAuth integration, gaining access to internal source code and pull requests

## Root cause
The signup endpoint fails to properly normalize and strip control characters from email addresses before checking against SAML-enforced domain list. The validation logic compares the user-supplied email string without removing trailing/embedded control characters, allowing bypass of domain enforcement checks.

## Attacker mindset
An attacker recognizes that security controls rely on exact string matching and can be circumvented through character encoding tricks. They understand OAuth chaining risks and that email verification requires only recipient interaction, not account owner approval. The 18-month dormancy of test accounts suggests patience in waiting for critical systems to become accessible.

## Defensive takeaways
- Always normalize email addresses by stripping/trimming whitespace and control characters (\r, \n, \t) before any validation logic
- Implement email validation using RFC 5321/5322 compliant parsers rather than regex or string matching
- Apply domain enforcement checks after normalization, not before
- Require manual approval or additional verification for accounts on domains with elevated privileges before granting OAuth access to downstream services
- Implement strict allowlists for OAuth token usage rather than implicit trust in email domain verification
- Audit and rotate API keys when SAML provisioning occurs, not just session revocation
- Consider implementing email domain-level restrictions (prevent @hackerone.com accounts accessing certain integrations without explicit admin approval)
- Add logging and alerting for signup attempts with suspicious control characters or encoding

## Variant hunting
Test other control characters (\x00, \x0c, \x1a) in email fields across authentication endpoints
Check if similar bypass applies to username, password, or organization fields
Test SAML enforcement on password reset and account recovery flows
Examine if domain enforcement is bypassable with Unicode normalization attacks (homograph attacks)
Check for similar control character bypasses in other email validation contexts (API key generation, email change endpoints)
Test if appending special characters before domain (@example.com) affects validation logic
Verify if URL encoding variations (double encoding, mixed case %0D%0A vs %0d%0a) bypass additional checks
Test domain enforcement bypass during SAML account provisioning/sync operations

## MITRE ATT&CK
- T1190
- T1566
- T1078
- T1556
- T1528
- T1550

## Notes
This is a chained vulnerability requiring: (1) input validation bypass, (2) email verification interaction, and (3) OAuth trust assumptions. The impact extends beyond direct HackerOne access to downstream systems (PullRequest) that trust HackerOne as identity provider. Pre-staging accounts months in advance demonstrates sophisticated attack planning. The mention of API keys persisting after SAML provisioning reveals secondary impact vector for long-term persistence.

## Full report
<details><summary>Expand</summary>

**Summary:**

SAML signup domain enforcement for new signups that belong to a SAML-enabled organization can be bypassed with trailing control characters. While the described issue affects all organizations with this feature enabled, it's possible to leverage it to access the PullRequest HackerOne organization, giving a real attacker access to HackerOne source code in Pull Requests.

**Description:**

When signing up on hackerone.com, email domains enforced by HackerOne SSO are not allowed for regular registration. The request to `/POST users` returns a redirect to the SSO provider:

```
POST /users HTTP/1.1
Host: hackerone.com
...

user%5Bname%5D=[NAME]&user%5Busername%5D=[USERNAME]&user%5Bemail%5D=email%40example.com&user%5Bpassword%5D=[PASSWORD]&user%5Bpassword_confirmation%5D=[PASSWORD]
```

```json
{"redirect_path":"/users/saml/sign_in?email=email%40example.com"}
```

However, adding a `%0d%0a` in the end of the email param will make the request go through:

```
POST /users HTTP/1.1
Host: hackerone.com
...

user%5Bname%5D=[NAME]&user%5Busername%5D=[USERNAME]&user%5Bemail%5D=email%40example.com%0d%0a&user%5Bpassword%5D=[PASSWORD]&user%5Bpassword_confirmation%5D=[PASSWORD]
```

```json
{"redirect_path":"/users/sign_in","errors":{}}
```

Then, logging in with the actual email `email@example.com` will work, but email verification is then enforced. Accessing the account will work if the email owner clicks on the HackerOne standard verification email sometime in the future.

Since hackerone.com is a domain part of a SAML-enabled organization itself, if an attacker creates multiple accounts that will send legitimate verification emails to `@hackerone.com` users and one clicks it, accessing PullRequest via `Sign in with HackerOne` on https://app.pullrequest.com/login, will then allow source code access.

The following steps were followed along with @jobert to create a `j@hackerone.com` account that will then allow access to PullRequest:

{F2581722}

### Steps To Reproduce

1. Go to https://hackerone.com 
2. Signup as the attacker with a `@hackerone.com` email you control, e.g. `x@hackerone.com` or `x+test@hackerone.com`, notice that this will redirect you to the SSO login
3. Try to signup again and intercept the request to `POST /users` and add the `%0d%0a` in the end of the email parameter
4. As the victim, click the confirmation email in a separate session
5. As the attacker on the original session, log in with the password you chose for the account
6. Go to https://app.pullrequest.com/login and click `Sign in with HackerOne`
7. You'll have access to all pull requests of HackerOne infrastructure codebase, including source code access

## Impact

An attacker can bypass the signup SAML enforcement for any organization on HackerOne, including HackerOne organization itself which leads to source code access. Verifying the email is the only interaction step, but an actual attack could be feasible.

On the other hand, when SAML accounts are provisioned for any organization, the previous sessions are revoked, but not API keys. So an attacker who can pre-stage an account on HackerOne and generate API keys will keep backdoor access to the account until the API keys are rotated explicitly by the victim, which could mean forever for specific accounts that will never rotate the API keys.

## Suggested mitigations

- Correctly strip and normalize the email address that is being processed in the signup endpoint to check if SAML is enforced
- Don't give access to anyone with an `@hackerone.com` email address to PullRequest without manual approval or account flags

## Notes:

- No source code was stored locally while performing this testing
- The accounts created while testing were `j@hackerone.com` and `0xacb@hackerone.com`
- The `0xacb@hackerone.com` was created around 18 months ago - I didn't realize any impact until now after showing this behavior to @jobert during h1-702-2023

</details>

---
*Analysed by Claude on 2026-05-24*
