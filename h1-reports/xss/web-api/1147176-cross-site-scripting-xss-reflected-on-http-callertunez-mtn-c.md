# Reflected Cross-Site Scripting (XSS) in callertunez.mtn.com.gh sharedetail.ftl

## Metadata
- **Source:** HackerOne
- **Report:** 1147176 | https://hackerone.com/reports/1147176
- **Submitted:** 2021-04-03
- **Reporter:** renzi
- **Program:** MTN Ghana
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the sharedetail.ftl endpoint via the unvalidated 'callback' parameter. An attacker can inject malicious JavaScript code that executes in the victim's browser, allowing page content manipulation and arbitrary script execution.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the callback parameter: http://callertunez.mtn.com.gh/wap/noauth/sharedetail.ftl?callback=malicious_script&type=
2. Attacker sends the crafted URL to victim via phishing email, social media, or other social engineering tactics
3. Victim clicks the link while authenticated to the MTN service
4. Browser requests the page and the callback parameter is reflected into the HTML response without proper encoding
5. JavaScript payload executes in victim's browser context with access to session cookies and sensitive data
6. Attacker can steal session tokens, redirect to phishing page, modify page content, or perform actions on behalf of the victim

## Root cause
The application fails to properly sanitize or HTML-encode user input from the 'callback' parameter before reflecting it back into the HTTP response. The FreeMarker template (FTL) likely uses unsafe interpolation without escape directives.

## Attacker mindset
An attacker would identify this parameter as injectable by testing common XSS payloads. The 'callback' parameter name suggests JSONP functionality, which is a known XSS vector. The attacker realizes that no input validation or output encoding is in place, making exploitation trivial.

## Defensive takeaways
- Implement strict input validation: whitelist allowed characters and reject anything that doesn't match expected patterns
- Apply context-aware output encoding: HTML-encode all user input before reflection, use FreeMarker's ?html escape or ?xhtml_escape filter
- Use Content Security Policy (CSP) headers to restrict script execution and mitigate XSS impact
- Avoid using callback parameters for JSONP without proper validation; prefer CORS-enabled APIs
- Implement automated security testing (SAST/DAST) in CI/CD pipeline to detect XSS vulnerabilities
- Conduct security code review focusing on template rendering and parameter handling
- Apply principle of least privilege: ensure noauth endpoints don't process sensitive operations

## Variant hunting
Test other FTL template files in /wap/noauth/ directory for similar callback parameters
Fuzz the 'type' parameter and other query parameters for XSS vulnerabilities
Test mutation of payload: javascript:, data: URIs, SVG vectors, event handler variations
Check if callback parameter is used in JavaScript context (script tags) for script injection
Examine if other MTN properties use similar vulnerable patterns with callback parameters
Test POST-based XSS variations and stored XSS if callback data is persisted
Investigate if JSONP endpoint exists and test for JSONP-specific bypasses

## MITRE ATT&CK
- T1190
- T1566.002
- T1589.001

## Notes
The vulnerability is in a public-facing endpoint without authentication requirement (/noauth/), significantly increasing risk. The proof-of-concept uses a simple img onerror handler, suggesting basic exploitation. FreeMarker templates require explicit unsafe configuration to allow unrestricted variable interpolation, indicating either misconfiguration or use of deprecated syntax. The sharedetail.ftl likely serves user-generated or shared content, making it a high-value XSS target.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello,
I found a Reflected Cross site Scripting (XSS) on http://callertunez.mtn.com.gh/wap/noauth/sharedetail.ftl via `callback` parameter . With this security flaw is possible rewrite the content of page, executing JS codes...

## Steps To Reproduce:
How we can reproduce the issue:

  1. Go to http://callertunez.mtn.com.gh/wap/noauth/sharedetail.ftl?callback=">><img%20src=x%20onerror=confirm("Renzi")>&type=
  2. And we can see alert with Renzi message...

{F1252321}


## Supporting Material/References:
* https://owasp.org/www-community/attacks/xss/

## Impact

* The attacker can execute JS code.
* Rewrite the content of Page

</details>

---
*Analysed by Claude on 2026-05-12*
