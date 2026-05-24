# Email Verification Bypass in OAuth Flow Leading to Account Takeover via Third-Party Services

## Metadata
- **Source:** HackerOne
- **Report:** 922456 | https://hackerone.com/reports/922456
- **Submitted:** 2020-07-13
- **Reporter:** cache-money
- **Program:** GitLab/Bitbucket OAuth providers (impacting third-party services like LaravelShift)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Authentication Bypass, Email Verification Bypass, OAuth Implementation Flaw, Account Takeover, Insufficient Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical authentication bypass exists in the OAuth authorization flow where email verification requirements can be circumvented by directly submitting the /oauth/authorize request, bypassing the frontend validation prompt. This allows attackers to obtain OAuth tokens for unverified email accounts, which third-party applications trust implicitly, leading to account takeover of existing accounts associated with the same email address.

## Attack scenario
1. Attacker creates a legitimate account on a target OAuth provider (GitLab) with a victim's email address but intentionally does not verify it
2. Attacker initiates OAuth flow with a third-party service (LaravelShift) that trusts the OAuth provider's email validation
3. Attacker encounters the frontend validation message requiring email verification
4. Attacker intercepts the OAuth authorization request and submits it directly via Burp or similar tools, bypassing the frontend check
5. OAuth provider processes the request and issues an authorization code despite unverified email status
6. Attacker uses the authorization code to authenticate with the third-party service, which accepts the unverified email as trusted
7. If a victim previously registered with the same email on the third-party service, attacker gains access to that account

## Root cause
The OAuth provider enforces email verification check only at the UI/frontend layer rather than enforcing it server-side during the /oauth/authorize request processing. The backend authorization endpoint does not validate that the requesting user's email has been verified before issuing the authorization code.

## Attacker mindset
An attacker recognizes that OAuth providers are implicitly trusted by third-party applications and that email addresses often serve as account identifiers across services. By obtaining an OAuth token for an unverified email matching an existing victim account, the attacker can exploit the transitive trust relationship to hijack accounts without needing to compromise the original email account.

## Defensive takeaways
- Enforce email verification checks server-side in the OAuth authorization endpoint, not just at the UI level
- Include email verification status in OAuth token claims and validate it before granting authentication
- Require email verification before issuing OAuth authorization codes, regardless of request method
- Third-party applications should validate email verification status from OAuth providers rather than assuming all emails are verified
- Implement additional account linking validation when OAuth email matches existing accounts
- Add server-side request validation to prevent bypassing frontend security controls
- Log and alert on direct API requests to authorization endpoints that bypass normal UI flows

## Variant hunting
Check if other OAuth providers (Google, GitHub, Microsoft) have similar frontend-only email verification checks
Test if phone number verification has identical bypass vulnerabilities in OAuth flows
Investigate if 2FA requirements can be bypassed through direct API requests to authorization endpoints
Examine if other OAuth scopes or response types bypass security checks differently
Test if session validation is properly enforced when making direct authorization requests
Check if CSRF tokens are properly validated for direct /oauth/authorize POST requests
Investigate corporate/domain-restricted OAuth implementations for similar email validation bypasses

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1621
- T1556
- T1098

## Notes
This vulnerability demonstrates a critical trust assumption failure in OAuth implementations. The backend must never rely on frontend-only validation for security-critical operations. The issue is particularly severe because it affects not just the OAuth provider but all downstream third-party applications that integrate with it. The attacker requires no access to the victim's actual email account, only knowledge of the email address, making this a high-risk vulnerability for account takeover at scale.

## Full report
<details><summary>Expand</summary>

### Summary
There's a limitation that requires a validated email before going through the OAuth flow, however this is bypassable. Bypassing this means the target site assumes your email is validated, and actually ends up signing you in with an non-validated email. This behavior can frequently lead to account takeovers in 3rd parties since they often use the email as an identifier, and fold all OAuth/manually created accounts into one. In my example I am going to demonstrate an account takeover on https://laravelshift.com/, however this concept is widely exploitable.

It should also be possible to use this technique to get into internal company using pages that just look for `@domain.com` in the email before allowing them access.

### Steps to reproduce
1) Create a Bitbucket or GitHub account with a random email, and login to https://laravelshift.com/. (We're seeding a victim account).
2) In a different browser, create a new GitLab account with that same email but never confirm it.
3) In that browser, visit LaravelShift and click "Sign in with GitLab", notice you land on a page that states you cannot complete the OAuth grant without validating your email.

Run the following request in Burp replacing your cookies, CSRF token, and state parameter.

```
POST /oauth/authorize HTTP/1.1
Host: gitlab.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 354
DNT: 1
Connection: close
Cookie: [COOKIES]

utf8=%E2%9C%93&authenticity_token=[CSRF TOKEN]&client_id=6dd35c52b02a99eca3454505c4b1f1fa761ad1125bcdccdbc1c290877ef25093&redirect_uri=https%3A%2F%2Flaravelshift.com%2Fauth%2Fgitlab%2Fcallback&state=[STATE VALUE FROM URL]&response_type=code&scope=&nonce=
```
4) Notice the request succeeds with a 302 to LaravelShift with the `code`.
5) Visit that URL and notice you get logged into the victim's account from step 1. This works since the GitLab email is assumed to be trusted and validated.

### Impact

Account takeovers on 3rd parties due to developers assuming GitLab is properly checking validated emails.

### What is the current *bug* behavior?

It's possible to play the `/oauth/authorize` request directly to bypass the `Verify the email address in your account profile before you sign in.` prompt.

### What is the expected *correct* behavior?

The email verification check should be enforced at this step of the process as well.

## Impact

Thanks,
-- Tanner

</details>

---
*Analysed by Claude on 2026-05-24*
