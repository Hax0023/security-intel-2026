# Reflected XSS on mtnhottseat.mtn.com.gh API Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1069527 | https://hackerone.com/reports/1069527
- **Submitted:** 2021-01-01
- **Reporter:** lu3ky-13
- **Program:** MTN Ghana
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in the /api/v2/subscribe/ endpoint of mtnhottseat.mtn.com.gh allowing arbitrary JavaScript execution through unvalidated query parameters. The vulnerability permits attackers to steal session cookies, manipulate page content, and perform unauthorized actions on behalf of authenticated users.

## Attack scenario
1. Attacker crafts malicious URL containing XSS payload: ><img src=x onerror=alert(document.domain)>
2. Attacker sends URL to victim via phishing email or social engineering
3. Victim clicks link while authenticated to mtnhottseat.mtn.com.gh
4. Browser executes injected JavaScript in context of victim's session
5. Malicious script accesses document.cookies containing session tokens
6. Attacker exfiltrates session cookie or performs account takeover actions

## Root cause
The /api/v2/subscribe/ endpoint fails to properly validate and encode user-supplied input from URL parameters before reflecting it in HTTP responses. Input sanitization and output encoding mechanisms are not implemented.

## Attacker mindset
Opportunistic reconnaissance identifying unprotected API endpoints. Attacker likely leveraged basic XSS payloads knowing many systems lack input validation on API endpoints. Simple proof-of-concept demonstrates impact before developing sophisticated exploitation chains.

## Defensive takeaways
- Implement input validation using whitelist approach for all user-supplied parameters
- Apply context-aware output encoding (HTML, URL, JavaScript encoding) based on response context
- Deploy Content Security Policy (CSP) headers to restrict script execution sources
- Use security testing tools and SAST to identify reflection points in code
- Implement Web Application Firewall (WAF) rules to detect and block XSS payloads
- Conduct security training for developers on secure coding practices
- Establish mandatory security code review process for API endpoints
- Apply httpOnly and Secure flags to session cookies to limit JavaScript access

## Variant hunting
Test other /api/v2/* endpoints for similar parameter injection points
Check for stored XSS variants in subscription data that persists in backend
Examine DOM-based XSS vulnerabilities in JavaScript handling of subscribe responses
Fuzz endpoint parameters with various encoding methods and bypass techniques
Test for blind XSS using out-of-band callbacks in less obvious parameters
Check for second-order XSS where reflected input is stored and displayed elsewhere

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1539
- T1005

## Notes
Report lacks detailed proof-of-concept documentation and severity assessment. No response timeline or patch confirmation provided. The use of an API endpoint for XSS is notable as APIs may have reduced security scrutiny compared to web UI. The ;%22 encoding bypass technique suggests potential WAF evasion attempts.

## Full report
<details><summary>Expand</summary>

hello dear

I have found Reflected XSS on mtnhottseat.mtn.com.gh
parameters injectable /api/v2/subscribe/;

my payload "><img src=x onerror=alert(document.domain)>

URL: https://mtnhottseat.mtn.com.gh/api/v2/subscribe/;%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E

{F1140524}

## Impact

Malicious JavaScript has access to all the same objects as the rest of the web page, including access to cookies and local storage, which are often used to store session tokens. If an attacker can obtain a user's session cookie, they can then impersonate that user.

Furthermore, JavaScript can read and make arbitrary modifications to the contents of a page being displayed to a user. Therefore, XSS in conjunction with some clever social engineering opens up a lot of possibilities for an attacker.

</details>

---
*Analysed by Claude on 2026-05-12*
