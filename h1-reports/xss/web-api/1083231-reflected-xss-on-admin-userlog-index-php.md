# Reflected XSS on /admin/userlog-index.php

## Metadata
- **Source:** HackerOne
- **Report:** 1083231 | https://hackerone.com/reports/1083231
- **Submitted:** 2021-01-21
- **Reporter:** solov9ev
- **Program:** Revive Adserver
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** CVE-2021-22874
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Revive Adserver 5.1.0 on the /admin/userlog-index.php endpoint where the 'period_preset' parameter is not properly sanitized or encoded before being reflected in the HTTP response. An attacker can inject arbitrary JavaScript code that executes in the victim's browser when they visit a malicious link.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the period_preset parameter
2. Attacker sends the crafted URL to a victim (via email, social media, or other means)
3. Victim clicks the link while authenticated to Revive Adserver admin panel
4. The malicious payload is reflected back in the HTML response without proper encoding
5. Browser parses and executes the injected JavaScript in the context of the admin application
6. Attacker's JavaScript can steal session cookies, admin credentials, or perform unauthorized actions

## Root cause
The application fails to properly encode or sanitize the 'period_preset' query parameter before reflecting it into the HTML response. The parameter value is inserted directly into the page without HTML entity encoding or context-aware escaping.

## Attacker mindset
An attacker would target this endpoint to compromise administrator accounts by crafting phishing URLs that appear legitimate. By stealing admin session cookies or credentials through XSS, they could gain full control of the ad serving platform, modify campaigns, inject malicious ads, or access sensitive business data.

## Defensive takeaways
- Implement strict input validation on all query parameters, whitelisting expected values
- Apply context-aware output encoding (HTML entity encoding) for all user-controlled data reflected in HTML context
- Use a templating engine with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Sanitize and validate the period_preset parameter against expected preset values only
- Conduct security code review of all admin-facing endpoints that process user input
- Implement automated security testing (SAST/DAST) in the CI/CD pipeline to catch XSS vulnerabilities

## Variant hunting
Test other parameters on the same endpoint (advertiserId, publisherId, period_start, period_end, setPerPage)
Check /admin/userlog-index.php for other reflected XSS in different endpoints or admin modules
Examine other admin pages that accept date/time period parameters for similar vulnerabilities
Test for DOM-based XSS if JavaScript processes the period_preset parameter client-side
Check if the vulnerability can be escalated to Stored XSS if data is persisted in logs or preferences

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
This is a classic reflected XSS in an admin panel which significantly increases impact. The use of HTML entity encoding in the payload (%3C%3D for < and >) suggests the application may have basic WAF/filtering that only checks for literal script tags, making it vulnerable to encoding bypasses. The vulnerability requires the victim to be authenticated to the admin panel, limiting exposure but not eliminating risk in targeted attacks against administrators.

## Full report
<details><summary>Expand</summary>

I found a reflected XSS attack on `/admin/userlog-index.php`. 

Revive-Adserver  version is `revive-adserver-5.1.0`.

- Go to `http://revive-adserver.loc/admin/userlog-index.php?advertiserId=0&publisherId=0&period_preset=all_events%3C/script%3E%3Cscript%3Ealert(document.domain)%3C/script%3E%3Cscript%3E&period_start=&period_end=&setPerPage=10`
- Malicious code executed

{F1166698}

Rendered response from server:

{F1166701}

## Impact

With this vulnerability, an attacker can for example steal users cookies or redirect users on malicious website.

</details>

---
*Analysed by Claude on 2026-05-12*
