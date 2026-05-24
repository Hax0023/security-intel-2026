# Open Redirect on Login Page of Stocky App

## Metadata
- **Source:** HackerOne
- **Report:** 1087189 | https://hackerone.com/reports/1087189
- **Submitted:** 2021-01-26
- **Reporter:** luc1d
- **Program:** Stocky
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, Unvalidated Redirect, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Stocky login page contains an open redirect vulnerability via the 'return_to' parameter. An attacker can craft a malicious URL redirecting authenticated users to arbitrary external websites after successful login. This enables phishing attacks and credential harvesting by redirecting users to attacker-controlled domains.

## Attack scenario
1. Attacker crafts a malicious URL: https://stocky.shopifyapps.com/users/login?return_to=//evil.com
2. Attacker sends this URL to target user via email, social media, or other channels disguised as legitimate Stocky link
3. Target user clicks the link and accesses the genuine Stocky login page
4. User logs in with their credentials
5. Upon successful authentication, application redirects user to //evil.com
6. User lands on attacker's malicious website which may impersonate Stocky or execute secondary attacks

## Root cause
The application fails to validate and sanitize the 'return_to' parameter before using it in HTTP redirects. The parameter accepts protocol-relative URLs (//evil.com) without checking against a whitelist of allowed domains or enforcing same-site redirect policies.

## Attacker mindset
Exploit trusted application authentication flow to redirect users to attacker-controlled infrastructure. Leverage user trust in legitimate login process to conduct phishing campaigns, steal additional credentials, or perform credential stuffing attacks against other services.

## Defensive takeaways
- Implement strict whitelist validation for redirect parameters - only allow redirects to known safe URLs or relative paths
- Use allowlist pattern matching to reject protocol-relative URLs (//), javascript: schemes, and data: URIs
- Implement URL parsing and validation using language-native secure libraries rather than string manipulation
- Enforce same-site redirect policy requiring redirects to match request origin domain
- Add CSRF tokens to login forms and validate them before processing redirects
- Log and monitor suspicious redirect attempts for security analysis
- Educate users about legitimate Shopify app URLs and warn about suspicious redirects

## Variant hunting
Check other parameters accepting URLs: redirect_uri, next, destination, target, callback, url, forward_to, return_url, continue, goto
Test logout endpoints for similar redirect vulnerabilities
Check password reset flows for open redirect via return_to equivalents
Test OAuth/SSO callback handling for unvalidated redirects
Examine API endpoints accepting URL parameters in other Shopify apps
Test POST request redirect parameters not just GET
Check for double encoding bypass: return_to=%252F%252Fevil.com

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598.001 - Phishing: Spearphishing Attachment
- T1566.002 - Phishing: Phishing - Link

## Notes
This is a relatively simple but effective vulnerability commonly found in Shopify apps. The use of protocol-relative URLs (//) is a common bypass for naive redirect validation. Severity is Medium rather than High because successful exploitation requires user action (clicking link and logging in). However, combined with social engineering, this significantly increases phishing campaign success rates.

## Full report
<details><summary>Expand</summary>

Vulnerable app is Stocky,
1. Visit login page of app with vulnerable parameter & malicious website address`(?return_to=//evil.com)` like `https://stocky.shopifyapps.com/users/login?return_to=//evil.com`
2. Then login to account
3. Open Redirect is executed

PoC Video:
{F1172071}

## Impact

Open Redirect

</details>

---
*Analysed by Claude on 2026-05-24*
