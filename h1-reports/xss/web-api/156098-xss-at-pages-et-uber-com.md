# Reflected XSS in pages.et.uber.com via lang_id Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 156098 | https://hackerone.com/reports/156098
- **Submitted:** 2016-08-02
- **Reporter:** raghav_bisht
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the lang_id parameter of pages.et.uber.com/icecream/ endpoint, allowing attackers to inject arbitrary JavaScript code that executes in victims' browsers. The vulnerability stems from unsanitized user input being reflected in HTML attributes without proper encoding or validation.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the lang_id parameter (e.g., with onmouseover event handler)
2. Attacker sends the URL to victim via email, chat, or social media, or hosts it on a controlled website
3. Victim clicks the link and visits the vulnerable page on pages.et.uber.com
4. The injected payload (e.g., onmouseover=prompt()) is reflected into the HTML without encoding
5. When victim interacts with the page (mouseover), the JavaScript executes in their browser context
6. Attacker can steal session cookies, redirect user, deface page content, or perform actions on behalf of the victim

## Root cause
The lang_id parameter is directly reflected into an HTML attribute without proper HTML entity encoding or content security measures. The application fails to escape special characters like quotes and event handler attributes, allowing attribute injection attacks.

## Attacker mindset
An attacker discovers that the lang_id parameter controls page behavior and tests for injection points by modifying the parameter value. Upon finding that input is reflected verbatim in HTML, they craft payloads leveraging event handlers (onmouseover) and JavaScript functions (prompt, fetch) to demonstrate code execution for credential theft or malware distribution.

## Defensive takeaways
- Implement HTML entity encoding for all user-controlled data reflected in HTML context (use libraries like OWASP ESAPI)
- Use Content Security Policy (CSP) headers with strict directive rules to prevent inline script execution
- Validate and whitelist lang_id parameter values against expected language identifiers (e.g., numeric or specific string formats)
- Apply principle of least privilege - avoid reflecting raw user input directly in HTML attributes
- Implement input validation on both client and server side to reject suspicious patterns
- Use templating engines with automatic escaping enabled by default
- Conduct regular security testing including SAST/DAST for XSS vulnerabilities across all entry points

## Variant hunting
Search for similar patterns: other subdomains/endpoints using language/locale parameters (lang, language, locale, region, country_id); parameter injection in URLs with onload, onerror, onclick, onchange handlers; reflected input in data attributes, href attributes, or JavaScript strings; similar patterns in related Uber properties and marketing/landing page infrastructure

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1598 - Phishing for Information
- T1566.002 - Phishing: Spearphishing Link

## Notes
The report demonstrates three payload variations targeting document.domain and document.cookie extraction, indicating reconnaissance for session hijacking. The lang_id parameter appears to control page language/localization without proper sanitization. The vulnerability is easily exploitable via URL manipulation and requires only user interaction (mouseover) rather than form submission. Multi-domain Uber infrastructure increases risk surface.

## Full report
<details><summary>Expand</summary>

Vulnerable Domain :
-------------------
https://pages.et.uber.com/

Vulnerable Link :
-----------------
https://pages.et.uber.com/icecream/?lang_id=5


Edited Link With Payload :
--------------------------
https://pages.et.uber.com/icecream/?lang_id=5%22%20onmouseover%3dprompt(document.domain)%20bad%3d%22
https://pages.et.uber.com/icecream/?lang_id=5%22%20onmouseover%3dprompt(document.cookie)%20bad%3d%22
https://pages.et.uber.com/icecream/?lang_id=5%22%20onmouseover%3dprompt(9020)%20bad%3d%22


Payload Used :
--------------

" onmouseover%3dprompt(9020) bad%3d"
" onmouseover%3dprompt(document.domain) bad%3d"
" onmouseover%3dprompt(document.cookie) bad%3d"

</details>

---
*Analysed by Claude on 2026-05-12*
