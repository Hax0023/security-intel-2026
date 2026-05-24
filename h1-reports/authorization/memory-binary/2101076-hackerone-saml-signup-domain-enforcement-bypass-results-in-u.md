# SAML signup domain enforcement bypass via trailing control characters leads to HackerOne source code access

## Metadata
- **Source:** HackerOne
- **Report:** 2101076 | https://hackerone.com/reports/2101076
- **Submitted:** 2023-08-08
- **Reporter:** 0xacb
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Authentication Bypass, SAML Policy Bypass, Email Validation Bypass, Control Character Injection, Unauthorized Account Creation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A SAML signup domain enforcement mechanism on HackerOne can be bypassed by appending CRLF control characters (%0d%0a) to email addresses during registration. This allows attackers to create accounts with restricted @hackerone.com domains, which combined with email verification clicking by legitimate users, grants unauthorized access to HackerOne infrastructure source code via PullRequest integration.

## Attack scenario
1. Attacker attempts to register with @hackerone.com email but receives SAML redirect as expected
2. Attacker intercepts POST /users request and appends %0d%0a control characters to email parameter to bypass domain validation
3. Signup succeeds with malicious account, email verification is pending
4. Attacker sends verification email which legitimately appears in HackerOne employee inbox
5. HackerOne employee clicks verification link, activating the attacker's account without realizing compromise
6. Attacker logs into activated account and uses 'Sign in with HackerOne' on PullRequest to access infrastructure codebase and source code

## Root cause
The email domain validation logic for SAML-enforced organizations fails to properly normalize and strip trailing control characters (CRLF - %0d%0a) before checking if the domain is in the restricted list. The validation likely uses simple string matching that doesn't account for whitespace or control character manipulation, allowing 'email@example.com%0d%0a' to bypass checks intended for 'email@example.com'.

## Attacker mindset
The attacker recognized that control characters in URLs/forms are often stripped by various layers of the application stack, allowing one layer's validation to be bypassed while another layer processes the 'clean' version. By injecting CRLF, they exploited the gap between the validation layer (which saw the control characters) and the storage layer (which stripped them). The secondary insight was leveraging the cross-integration with PullRequest and the social engineering aspect of email verification to gain account activation without direct compromise.

## Defensive takeaways
- Always normalize and canonicalize email addresses before validation (trim whitespace, lowercase, remove control characters) using dedicated email parsing libraries
- Apply validation AFTER normalization, not before - ensure the input you validate is identical to what gets stored
- Implement strict input validation using allowlists for email format rather than relying on string matching
- For SAML-enforced domains, validate the domain against the policy at multiple layers and log validation failures
- Revoke API keys when SAML accounts are provisioned/linked, not just sessions - treat it as a security event
- Implement additional controls for sensitive domains like @hackerone.com including manual approval workflows
- Monitor for registration attempts with control characters or unusual encoding patterns
- Use standard libraries for email validation (RFC 5321/5322 compliant parsers) rather than custom regex
- Consider requiring additional verification for accounts claiming restricted domains (callback verification, knowledge questions)

## Variant hunting
Test other control characters (%09 tab, %0c form feed, %20 space) in email and username fields during signup
Check if other special characters like %00 (null byte) can be injected to truncate validation
Test unicode normalization bypass using homoglyphs or combining characters (e.g., ä vs a+combining diaeresis)
Attempt the bypass on other endpoints that process email validation (password reset, email change)
Check if the vulnerability exists in API token creation or OAuth token generation endpoints
Test domain validation in other authentication flows (password reset, account recovery)
Investigate if API keys created before SAML provisioning are truly not revoked as mentioned
Test if subdomains or email aliases (x+tag@hackerone.com) bypass other controls
Check for similar issues in other organizations with SAML enforcement
Test if the bypass works retroactively for existing accounts by changing email addresses

## MITRE ATT&CK
- T1190
- T1583
- T1110
- T1621
- T1078
- T1199
- T1528

## Notes
The vulnerability is particularly severe because: (1) it affects HackerOne itself, not just customer organizations; (2) it requires relatively minimal interaction (one employee click on verification email); (3) it provides access to infrastructure source code; (4) the pre-staging capability with persistent API keys creates a backdoor condition; (5) the vulnerability was discoverable for 18 months before reporting. The control character injection technique is a classic bypass pattern that should be caught in security reviews. The cross-service risk (PullRequest integration) amplified the impact significantly.

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
