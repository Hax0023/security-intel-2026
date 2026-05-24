# Open Redirect via Unvalidated 'next' Parameter in Email Disconnection Flow

## Metadata
- **Source:** HackerOne
- **Report:** 238117 | https://hackerone.com/reports/238117
- **Submitted:** 2017-06-08
- **Reporter:** atruba
- **Program:** Weblate
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in Weblate's email account disconnection endpoint where the 'next' parameter is not properly validated. An attacker can craft a malicious URL that redirects authenticated users to arbitrary external domains after they disconnect their email account.

## Attack scenario
1. Attacker identifies the vulnerable disconnect email endpoint accepting an unvalidated 'next' parameter
2. Attacker crafts a malicious URL with next=https://attacker-controlled-domain.com
3. Attacker tricks a Weblate user into clicking the malicious link via phishing email or social engineering
4. User authenticates and initiates email account disconnection on the vulnerable endpoint
5. Application redirects the user to the attacker's domain after disconnection completes
6. Attacker can harvest credentials, perform session hijacking, or deliver malware via the redirect destination

## Root cause
The application accepts the 'next' parameter for post-action redirection without performing proper validation (e.g., whitelist checking, URL scheme validation, same-origin verification). The parameter is directly used in redirect logic without sanitization.

## Attacker mindset
An attacker exploiting this would focus on credential harvesting by redirecting users to a lookalike login page, credential re-entry prompts, or malware distribution sites. The trust users place in being redirected after legitimate account actions makes this particularly effective for phishing campaigns.

## Defensive takeaways
- Implement strict whitelist validation for redirect parameters - only allow relative URLs or explicitly approved domains
- Use URL scheme validation to prevent javascript: and data: URIs
- Implement same-origin policy checks ensuring redirects stay within the application domain
- Avoid user-supplied redirect parameters entirely when possible; use server-side session state instead
- Add security headers like X-Frame-Options and Content-Security-Policy to prevent clickjacking attacks
- Log and monitor redirect parameter usage for suspicious patterns
- Educate users about verifying URL bars after authentication actions

## Variant hunting
Check all authentication-related flows for similar 'next' parameter usage: login, logout, account recovery, 2FA
Audit other disconnection endpoints (social accounts, API tokens, connected services)
Search for URL redirection patterns across codebase: redirect(), location.href, HttpResponseRedirect
Test for double-encoding bypasses: %252e, URL normalization tricks
Check POST-based redirects and whether they validate the referring origin
Investigate if 'next' parameter is reflected in error messages or logs

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1187 - Forced Authentication

## Notes
This is a straightforward open redirect with clear security implications. Severity is medium rather than high because it requires user interaction (clicking a crafted link) and may be mitigated by browser warnings on cross-domain navigation. However, in combination with social engineering or trusted account contexts, it becomes highly effective. The endpoint deals with account modifications (email disconnection), making it particularly attractive for attackers since users may be more inclined to follow security-related links.

## Full report
<details><summary>Expand</summary>

Hi team, 
there is a open redirect end point when any account owner disconnect email accounts. He is redirected to some other domain.

Vulnerable URL

https://demo.weblate.org/accounts/disconnect/email/2354/?next=http://google.com
POC

Steps:
Go to authentication tab.
Disconnect Email account and capture the request.
Now, after next= write https://evil.com.
You are redirected to evil.com

Thanks,

</details>

---
*Analysed by Claude on 2026-05-24*
