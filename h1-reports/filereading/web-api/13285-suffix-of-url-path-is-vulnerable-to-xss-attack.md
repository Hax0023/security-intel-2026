# Suffix of URL-path Vulnerable to XSS Attack

## Metadata
- **Source:** HackerOne
- **Report:** 13285 | https://hackerone.com/reports/13285
- **Submitted:** 2014-05-25
- **Reporter:** bigbear
- **Program:** Khan Academy
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored XSS, Reflected XSS, Path-based XSS
- **CVEs:** None
- **Category:** web-api

## Summary
The application fails to properly sanitize user-controlled input in the URL path suffix, allowing attackers to inject arbitrary JavaScript code that executes in the victim's browser. An attacker can craft a malicious URL with script tags embedded in the path component, which is reflected back to the user without proper escaping or validation.

## Attack scenario
1. Attacker crafts a malicious URL with JavaScript payload embedded in the URL path suffix (e.g., Campin"><script>alert(/BigBear/)</script>.html)
2. Attacker sends the crafted URL to a victim via email, social media, or other communication channels
3. Victim clicks the malicious link, which loads the vulnerable web application
4. The application processes the URL path without proper input validation or output encoding
5. The injected JavaScript code is rendered in the victim's browser context and executes
6. Attacker can steal session cookies, perform actions on behalf of the victim, or redirect them to phishing pages

## Root cause
Insufficient input validation and output encoding on URL path parameters. The application accepts user-supplied data in the URL path suffix without sanitizing special characters or encoding them for safe HTML display. The path parameter is likely reflected directly in the HTTP response without proper escaping.

## Attacker mindset
The attacker identified that the application trusts and reflects URL path segments without validation. By breaking out of the expected filename format using a quote and angle bracket (>"), they discovered they could inject arbitrary HTML/JavaScript. The .html suffix continuation was a technique to bypass simple extension-based filtering.

## Defensive takeaways
- Implement strict input validation on all URL path parameters with allowlist approach
- Apply proper output encoding for context (HTML entity encoding for HTML context)
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Implement URL parsing and validation to reject paths with unexpected characters
- Avoid reflecting user input directly; sanitize and validate at both input and output layers
- Use security libraries for URL path normalization and validation
- Apply parameterized routing rather than accepting arbitrary path segments

## Variant hunting
Test other URL path segments for similar reflection vulnerabilities
Check if query parameters have similar issues
Test for DOM-based XSS in client-side path parsing
Look for stored XSS if path is saved to database
Test file upload endpoints that might use user-supplied filenames in paths
Check for path traversal combined with XSS
Test encoding bypasses (double encoding, Unicode, UTF-8)
Check for XSS in error messages that reflect the invalid path

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
This is a classic path-based reflected XSS vulnerability. The PoC shows the attacker escaped the expected context by injecting a quote and script tag. The application likely uses the URL path as a file identifier without proper validation. This affects educational platforms particularly due to their public nature and trust factor with users. The vulnerability could be used for credential harvesting, malware distribution, or defacement.

## Full report
<details><summary>Expand</summary>

PoC
http://smarthistory.khanacademy.org/Campin"><script>alert(/BigBear/)</script>.html

Malicious users may inject JavaScript, VBScript, ActiveX, HTML or Flash into a vulnerable application to fool a user in order to gather data from them.

</details>

---
*Analysed by Claude on 2026-05-24*
