# Reflected XSS in ViewContent.aspx via i Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 924650 | https://hackerone.com/reports/924650
- **Submitted:** 2020-07-15
- **Reporter:** nirajgautamit
- **Program:** Private Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the ViewContent.aspx endpoint where the 'i' URL parameter is not properly sanitized or HTML-encoded before being rendered in the response. An attacker can inject arbitrary JavaScript payloads through URL-encoded SVG event handlers to execute malicious scripts in victim browsers.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'i' parameter using URL encoding to bypass basic filters
2. Attacker distributes the link via phishing email, social engineering, or third-party websites to target users
3. Victim clicks the link while authenticated to the vulnerable application
4. The server reflects the unsanitized 'i' parameter value back in the HTML response without proper encoding
5. Browser parses the reflected SVG/JavaScript payload and executes the confirm() function (or malicious code in real attack)
6. Attacker gains ability to steal session cookies, perform CSRF actions, redirect to phishing pages, or harvest credentials

## Root cause
The application fails to properly HTML-encode or sanitize user-supplied input in the 'i' query parameter before reflecting it in the HTTP response. The use of URL encoding obscures the payload but does not prevent execution once decoded by the browser.

## Attacker mindset
Low-effort exploitation - attacker uses publicly available XSS payloads with URL encoding to bypass basic string matching filters. The simple proof-of-concept (confirm dialog) demonstrates the capability without requiring sophisticated attack infrastructure.

## Defensive takeaways
- Implement output encoding using context-aware encoding (HTML encoding for HTML context, JavaScript encoding for JS context, URL encoding for URL context)
- Use a security library or framework built-in XSS protection mechanisms rather than manual encoding
- Apply input validation with whitelist approach - define what characters/formats are acceptable for the 'i' parameter
- Implement Content Security Policy (CSP) headers to restrict inline script execution and limit XSS impact
- Use HTTPOnly flag on session cookies to prevent JavaScript access
- Conduct security code review of all user input handling, especially query parameters
- Perform dynamic security testing (DAST) and static analysis (SAST) in CI/CD pipeline
- Use parameterized templating engines that auto-escape by default

## Variant hunting
Search for similar vulnerable patterns: (1) Other ASP.NET endpoints reflecting query parameters without encoding; (2) Parameters with single-letter names (commonly less scrutinized: a=, b=, c=, i=, x=, y=); (3) ViewContent, GetContent, Display endpoints; (4) URL parameters in 'con_id', 'content_id', 'id' with adjacent reflection parameters; (5) Check for similar encoding bypass techniques (double-encoding, mixed case, entity encoding) on other parameters

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566.002: Phishing - Spearphishing Link
- T1598.003: Phishing - Spearphishing Link

## Notes
The report lacks specific impact demonstration beyond the confirm() proof-of-concept. The redacted URLs prevent full verification but the vulnerability is clearly demonstrated. The researcher tested across multiple browsers showing consistent behavior. The URL encoding bypass (e.g., %3C for <, %2F for /) indicates potential filter evasion against naive blacklist-based protection. Report quality could be improved with: full payload explanation, screenshot evidence, browser console output, and potential impact scenarios.

## Full report
<details><summary>Expand</summary>

Hello Security Team,
I would like to report the XSS vulnerability on your system.
The `i=` parameter is not escaped properly for URL encoded values.

Steps To Reproduce:
Visit the following POC link:
https://www.████/ViewContent.aspx?con_id_pk=2726&fr=s&i=l9716%27();}]9836&001%3C%2FScript%2F%3E%3CSvg%2FOnLoad%3D(confirm)(1)%3E=1

1. Tested on firefox browser: █████████ 

2.Tested on google chrome browser: ██████████
Thanks
Niraj

## Impact

An XSS attack allows an attacker to execute arbitrary JavaScript in the context of the attacked website and the attacked user. This can be abused to steal session cookies, perform requests in the name of the victim, or for phishing attacks.

</details>

---
*Analysed by Claude on 2026-05-12*
