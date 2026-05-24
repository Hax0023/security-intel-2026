# Open Redirect on lovable.dev via redirect parameter leads to phishing attacks

## Metadata
- **Source:** HackerOne
- **Report:** 3581815 | https://hackerone.com/reports/3581815
- **Submitted:** 2026-03-02
- **Reporter:** jdc94
- **Program:** Lovable
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on lovable.dev in the redirect parameter of the /auth/post-login and /purchase-success endpoints. By supplying a backslash-prefixed URL (e.g., /\google.com), an attacker can bypass the relative path validation and redirect authenticated users to arbitrary external domains, enabling phishing and social engineering attacks.

## Attack scenario
1. Attacker crafts a malicious URL: https://lovable.dev/auth/post-login?redirect=/\attacker-phishing.com
2. Attacker sends the crafted URL to a target user via email or social media, disguised as a legitimate Lovable domain link
3. Target user clicks the link while authenticated or logs in through the redirect
4. Application processes the redirect parameter and fails to properly validate the backslash-prefixed URL
5. User is silently redirected to attacker-phishing.com (trusted domain in browser URL bar history)
6. Attacker's phishing page harvests user credentials, API keys, or sensitive information

## Root cause
The application implements a redirect validation mechanism that checks for relative paths but fails to properly normalize or parse URLs containing backslash characters. The backslash (\) is interpreted as a path separator in some contexts rather than a URL path component, allowing the validator to accept it as a relative path while browsers interpret it as a protocol-relative or absolute URL redirect.

## Attacker mindset
An attacker would recognize that domain-based open redirects are highly effective for phishing because the browser's location bar still shows the trusted lovable.dev domain during the redirect process. By using backslash encoding, they bypass simple validation rules that only check for forward slashes or protocol prefixes, making this a low-effort, high-success-rate attack vector for credential harvesting.

## Defensive takeaways
- Implement strict URL parsing using a language-native URL parser that normalizes all path separators before validation
- Use an allowlist of permitted redirect destinations rather than attempting to block dangerous patterns
- Validate the redirect parameter against a strict whitelist of internal paths only (e.g., /dashboard, /settings)
- Implement proper URL normalization that treats backslashes as separators on all platforms before any validation logic
- Consider removing the redirect parameter entirely and using session-based post-login navigation instead
- Add security headers like X-Frame-Options and Content-Security-Policy to limit redirect-based attacks
- Test redirect validation with Unicode variations, double encoding, and mixed separators during security review

## Variant hunting
Test other endpoints with redirect parameters using: /\, /\\, /%5C, /%255C variants
Check for similar issues in other authentication flows (/logout, /forgot-password, /verify-email)
Test with protocol-relative URLs: redirect=/\//attacker.com, redirect=//attacker.com
Try mixed encoding: redirect=/%252F%252Fattacker.com
Test double dot encoding: redirect=/..\attacker.com
Check if the vulnerability exists in API endpoints that accept redirect parameters

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1598.004
- T1192

## Notes
The vulnerability is present in at least two endpoints (/auth/post-login and /purchase-success), suggesting a systemic validation issue rather than an isolated bug. The use of backslash as a bypass technique indicates insufficient URL parsing. This is a classic open redirect that gains severity from being on an authenticated endpoint where users are already logged in and may not scrutinize the redirect as carefully.

## Full report
<details><summary>Expand</summary>

## Summary:
An open redirect exists on lovable.dev. After logging in, a request is sent to 'https://lovable.dev/auth/post-login?redirect=%2F%3Fshould-refresh-credentials%3D1&_rsc=1b5jt'. Changing the redirect URL to /\google.com (https://lovable.dev/auth/post-login?redirect=/\google.com), for instance, allows a redirect to be performed to google.com. The application expects a relative path, but supplying a backslash-prefixed value (e.g., /\google.com) results in a redirect to an external domain (https://google.com).

This open redirect allows an attacker to craft URLs on the lovable.dev domain that redirect users to arbitrary external sites, which could be used in phishing campaigns or social engineering attacks.

### Note:

This vulnerability also exists at https://lovable.dev/purchase-success?redirect=/%5Cgoogle.com.

## Steps To Reproduce:
1. Login to an account
2. Visit https://lovable.dev/auth/post-login?redirect=/\google.com
3. You will be redirected to google.com

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

</details>

---
*Analysed by Claude on 2026-05-24*
