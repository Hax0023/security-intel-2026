# Reflected XSS via URL Path Parameter on Government Domain

## Metadata
- **Source:** HackerOne
- **Report:** 1825942 | https://hackerone.com/reports/1825942
- **Submitted:** 2023-01-08
- **Reporter:** notajax
- **Program:** Government agency (redacted)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** CVE-2021-41878
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the /xapi/statements endpoint where user-supplied input in the URL path parameter is not properly sanitized or encoded before being reflected in the HTTP response. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when accessed with valid API credentials.

## Attack scenario
1. Attacker identifies the vulnerable /xapi/statements endpoint that reflects URL parameters without encoding
2. Attacker crafts a malicious URL containing JavaScript payload in the file parameter: https://██████.gov/xapi/statements?file"><script>alert(document.domain)</script>
3. Attacker obtains or guesses valid API credentials (Basic auth: xapi-tools:xapi-tools) and includes required headers
4. Attacker shares the malicious link via social engineering, phishing emails, or compromised websites targeting government users
5. Victim clicks the link while authenticated to the government domain, causing the JavaScript to execute in their browser context
6. Attacker steals session cookies, authentication tokens, or sensitive data, potentially leading to account takeover or lateral movement

## Root cause
The application fails to properly sanitize and encode user-supplied input from the URL path parameter before reflecting it in the HTTP response. The endpoint accepts the file parameter and includes it in the response without adequate output encoding or Content Security Policy protection.

## Attacker mindset
An attacker would recognize this as a straightforward reflected XSS opportunity requiring minimal effort. The presence of default/weak API credentials (xapi-tools:xapi-tools) suggests this is a testing or development endpoint accidentally exposed to production. The attacker would focus on credential theft and account compromise, particularly targeting government employees.

## Defensive takeaways
- Implement strict input validation: whitelist allowed characters and reject any input containing special characters like quotes, angle brackets, or script tags
- Apply proper output encoding: HTML-encode all user-supplied data before including it in responses, using established libraries
- Deploy Content Security Policy (CSP) headers to prevent inline script execution even if XSS payload reaches the DOM
- Rotate default API credentials immediately and enforce strong, unique credentials for all API endpoints
- Remove or restrict API endpoints that should not be production-accessible; implement proper environment separation
- Add Web Application Firewall (WAF) rules to detect and block common XSS patterns in URL parameters
- Implement security headers: X-XSS-Protection, X-Content-Type-Options: nosniff
- Use a security code review process to identify reflection points before deployment
- Implement automated security testing and SAST tools in CI/CD pipeline

## Variant hunting
Test other xapi endpoints for similar parameter reflection vulnerabilities (/xapi/activities, /xapi/agents, etc.)
Check if other URL parameters in the same endpoint are vulnerable (test with different parameter names)
Attempt DOM-based XSS variants if parameters are processed client-side via JavaScript
Test for mutation XSS by using various encoding bypass techniques (unicode, double-encoding, case variation)
Investigate if the API accepts other authentication methods that might bypass the Basic auth requirement
Check for stored XSS if any parameters are persisted in logs or user profiles
Test POST/PUT methods on the same endpoint for XSS vulnerabilities
Examine if error messages or 404 pages also reflect unsanitized input

## MITRE ATT&CK
- T1190
- T1583.001
- T1598.003
- T1566.002
- T1539
- T1185

## Notes
The CVE-2021-41878 reference suggests this vulnerability has been publicly disclosed. The presence of weak default credentials (xapi-tools:xapi-tools) is unusual for production endpoints and indicates inadequate credential management. The xAPI (Experience API) context suggests this is related to learning management systems. The video POC mentioned but not provided would be valuable for understanding the exact response behavior. The authorization header requirement makes this a lower-impact reflected XSS since victims need to be authenticated, but it could still lead to privilege escalation or data exfiltration within the government network.

## Full report
<details><summary>Expand</summary>

Hi team,
I was able to execute XSS on  ███████.gov  

Steps to produce - 
1 -Turn on the burp intercepter 
2- Go to  https://██████.gov/xapi/statements?file"><script>alert(document.domain)</script>
3-  In  Intercepter add the following Headers 

  Authorization: Basic eGFwaS10b29sczp4YXBpLXRvb2xz
   X-Experience-Api-Version: 1.0.1

4-  when you send this GET request you will receive a response with XSS payload executed.

## Impact

An attacker can send the malicious link to victims and steals victims' cookie leading to account takeover.

## System Host(s)
www.███.gov

## Affected Product(s) and Version(s)


## CVE Numbers
CVE-2021-41878

## Steps to Reproduce
I have attached the Video POC, please check it out.

## Suggested Mitigation/Remediation Actions
sanitize the inputs in the URL



</details>

---
*Analysed by Claude on 2026-05-24*
