# Reflected Cross-Site Scripting (XSS) in access_token Parameter on api.tiles.mapbox.com

## Metadata
- **Source:** HackerOne
- **Report:** 135217 | https://hackerone.com/reports/135217
- **Submitted:** 2016-04-28
- **Reporter:** dawgyg
- **Program:** Mapbox
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the access_token parameter of page.html on api.tiles.mapbox.com, allowing attackers to inject arbitrary JavaScript code that executes in the victim's browser context. The vulnerability results from insufficient input sanitization and output encoding of the access_token parameter before rendering it in the HTML response.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the access_token parameter
2. Attacker sends the link to a victim via email, chat, or social media
3. Victim clicks the link and visits api.tiles.mapbox.com with the malicious payload
4. The server reflects the unsanitized access_token value into the HTML response
5. The victim's browser parses the injected script tags and executes the JavaScript payload
6. Attacker gains ability to steal session tokens, perform actions as the victim, or redirect to phishing pages

## Root cause
The page.html endpoint fails to properly validate and encode user-supplied input from the access_token parameter before including it in the HTML response, violating output encoding best practices. The parameter is likely directly concatenated into HTML without sanitization or context-aware encoding.

## Attacker mindset
An attacker would recognize that API endpoints often handle sensitive tokens and authentication parameters without sufficient security hardening. By targeting the access_token parameter, the attacker demonstrates knowledge that developers may overlook security controls on seemingly internal or less-critical pages. The simple payload structure suggests testing for basic XSS patterns.

## Defensive takeaways
- Implement strict input validation on all parameters, especially security-sensitive ones like tokens and API keys
- Apply context-aware output encoding (HTML entity encoding) to all user-supplied data before rendering in HTML context
- Use a Content Security Policy (CSP) to restrict script execution and prevent inline script injection
- Employ templating engines with auto-escaping features to prevent XSS by default
- Conduct security code reviews focusing on parameter handling in page generation logic
- Implement automated XSS detection testing in CI/CD pipeline
- Apply principle of least privilege: validate that access_token format matches expected JWT/token structure

## Variant hunting
Search for similar parameter reflection vulnerabilities in other Mapbox endpoints (e.g., other query parameters like style, callback, redirect_uri). Check related domains and API endpoints that handle tokens or authentication parameters. Test other Mapbox pages (not just page.html) with various parameters for similar XSS patterns. Investigate if other API endpoints on subdomains like tiles.mapbox.com, api.mapbox.com expose similar issues.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1176

## Notes
This is a classic reflected XSS on a high-value target (map tile API service). The access_token parameter is particularly sensitive as it controls API authentication, making this vulnerability especially dangerous. The PoC payload escapes HTML context and injects script tags directly. The report demonstrates responsible disclosure to Mapbox's bug bounty program.

## Full report
<details><summary>Expand</summary>

There is a reflective XSS vulnerability in the access_token param found in the page.html at api.tiles.mapbox.com

A proof of concept link:
http://api.tiles.mapbox.com/v4/ctswebrequest.m4ga59jd/page.html?access_token=pk.eyJ1IjoiY3Rzd2VicmVxdWVzdCIsImEiOiJTb19VUHM0In0.muGg6tMDG4NOGrV4qQQ8yw.htaccess.aspx%27%3E%3Cscript%3Ealert%28document.domain%29%3C/script%3E#11/39.9168/-75.1595

</details>

---
*Analysed by Claude on 2026-05-12*
