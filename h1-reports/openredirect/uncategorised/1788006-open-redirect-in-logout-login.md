# Open Redirect in Logout & Login via 'logout' Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1788006 | https://hackerone.com/reports/1788006
- **Submitted:** 2022-11-29
- **Reporter:** qualw1n
- **Program:** Expedia
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, Unvalidated Redirect, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
The logout endpoint on Expedia's login page fails to validate the 'logout' parameter, allowing attackers to redirect authenticated users to arbitrary external URLs. An attacker can craft a malicious logout link that redirects users to a phishing site after they log out, potentially capturing credentials or spreading malware.

## Attack scenario
1. Attacker crafts a malicious URL: www.expedia.com/?logout=https://attacker-phishing-site.com
2. Attacker sends the URL to victims via email, social media, or embedded in a webpage
3. Victim clicks the link while logged into Expedia, triggering the logout process
4. The application processes the logout request and redirects to the attacker's URL without validation
5. Victim arrives at attacker's phishing site which mimics Expedia's login page
6. Victim re-enters credentials, which are captured by the attacker

## Root cause
The logout endpoint accepts the 'logout' parameter and uses it directly for redirection without implementing whitelist validation, URL scheme validation, or relative path enforcement. The application fails to verify that redirect destinations are part of an allowed domain list.

## Attacker mindset
An attacker recognizes that logout flows are trust moments where users expect to be redirected to a safe location. By injecting a malicious URL into a parameter that controls post-logout redirection, they can exploit user trust to redirect them to phishing pages. This is particularly effective because the redirect happens after legitimate logout, making it appear trustworthy to the victim.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters - only allow URLs matching known safe domains
- Use relative URLs for internal redirects instead of accepting full URLs as parameters
- Validate that redirect destinations have matching origin/scheme (https only)
- Avoid accepting redirect targets from user-controllable input entirely; use predefined safe endpoints
- Implement URL parsing to detect and block common open redirect bypasses (protocol confusion, double encoding)
- Add security headers like Content-Security-Policy to mitigate phishing post-redirect
- Log all redirect operations for monitoring suspicious patterns
- Conduct security code review of all authentication/logout flows for unvalidated redirects

## Variant hunting
Test 'rurl', 'return', 'redirect', 'returnUrl', 'next', 'continue' parameters on login/logout endpoints
Try protocol bypasses: javascript:, data:, \\attacker.com, //attacker.com, https:\\attacker.com
Test on login endpoint: www.expedia.com/login?redirect=https://attacker.com
Check if parameter validation differs between authenticated and unauthenticated states
Examine mobile app login flows for similar unvalidated redirect parameters
Test password reset, email verification, and account recovery endpoints for open redirects
Check third-party OAuth/SSO logout callbacks for unvalidated redirects

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (sending malicious logout link)
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1187 - Forced Authentication (redirecting to fake login after logout)
- T1598 - Phishing for Information

## Notes
The researcher notes that the vulnerability exists in the parameter section after '?' which handles redirects without validation. The write-up demonstrates clear impact through phishing potential. This is a classic open redirect vulnerability often overlooked in authentication flows. Expedia's impact likely mitigated by large user base awareness, but individual targeted attacks remain viable. The vulnerability affects both POST-logout and potentially login workflows.

## Full report
<details><summary>Expand</summary>

## Entry
Hello there! While browsing on expedia, I logged out of the account and as soon as I logged out, it was calling me a parameter called "rurl" directly on the link, I examined it and was able to redirect successfully.

## Default Request

GET /?logout=1 HTTP/2
Host: www.expedia.com
Cookie:  { REDACTED }
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Te: trailers

## Default Response

HTTP/2 200 OK

##In response, it redirects us to the homepage.

## Vulnerability Request

GET /?logout=https://qx4lw1nsec.blogspot.com HTTP/2
Host: www.expedia.com
Cookie: { REDACTED }
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Te: trailers


## Note
The part that exposes to explicit redirection is "?" in the section after the address. is use.
and whatever he does he will throw redirects.

## Video
{F2053834}

## Impact

Redirect
Phishing
Social Engineering

</details>

---
*Analysed by Claude on 2026-05-24*
