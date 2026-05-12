# Reflected Cross-site Scripting via Search Query Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2434904 | https://hackerone.com/reports/2434904
- **Submitted:** 2024-03-26
- **Reporter:** neg0x
- **Program:** Undisclosed (redacted)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Sanitization, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the search functionality of a subdomain where user input is directly injected into an h6 HTML tag without proper sanitization. An attacker can break out of the h6 tag and inject arbitrary JavaScript code that executes in the victim's browser, potentially stealing cookies and session tokens.

## Attack scenario
1. Attacker performs subdomain enumeration to identify a target subdomain with search functionality
2. Attacker discovers the search parameter echoes user input directly into an h6 HTML tag without escaping
3. Attacker crafts a malicious payload: </h6><image/src/onerror=alert(document.cookie)>
4. Attacker distributes a link containing the XSS payload to target users via phishing, social engineering, or other methods
5. Victim clicks the malicious link while authenticated to the application
6. JavaScript executes in victim's browser context, stealing sensitive data like cookies and session tokens

## Root cause
The application fails to implement proper output encoding/HTML escaping when displaying search query parameters in HTML context. User input is rendered directly into the DOM without sanitization, allowing attackers to break tag boundaries and inject script payloads.

## Attacker mindset
Opportunistic vulnerability hunter seeking low-hanging fruit through subdomain enumeration and parameter fuzzing. Exploits common development oversight of missing output encoding in search features to demonstrate client-side code execution.

## Defensive takeaways
- Implement consistent output encoding for all user-controlled data displayed in HTML context (use htmlspecialchars or equivalent)
- Apply Content Security Policy (CSP) headers with strict script-src directives to mitigate XSS impact
- Use templating engines with auto-escaping enabled by default
- Validate and sanitize all user inputs at both client and server-side
- Implement security testing in CI/CD pipeline to catch XSS vulnerabilities early
- Use security headers (X-XSS-Protection, X-Content-Type-Options) as defense-in-depth measures
- Conduct regular security code reviews focusing on user input handling

## Variant hunting
Check other search/filter parameters across the application for similar encoding issues
Test other HTML contexts (attributes, JavaScript strings, URLs) for XSS variants
Examine error messages and logging features for reflected XSS vulnerabilities
Review autocomplete/suggestion features that may echo user input
Test other subdomains for identical vulnerable patterns
Analyze any user-generated content display features (comments, profiles) for similar flaws

## MITRE ATT&CK
- T1190
- T1566
- T1204

## Notes
Report is minimal with significant redactions. The payload uses a simple tag-breaking technique combined with an img tag onerror handler. This is a straightforward reflected XSS that would be caught by basic output encoding. The fact that subdomain enumeration was required suggests the vulnerable endpoint may not have been obvious, indicating potential security through obscurity rather than proper security controls.

## Full report
<details><summary>Expand</summary>

Hi team

I found a reflected xss via search query on ████████ that allows an attacker to execute Javascript code into victim's browser.

## PoC

1- Doing subdomain enumeration of ██████████, i found the following one: ████████
2- On the search query i saw that is injecting inside an h6 html tag:

██████████

3- So to html escape, i used the following payload to trigger the XSS: `</h6><image/src/onerror=alert(document.cookie)>`

████

## Impact

An incorrect sanitization of search query parameter allows an attacker to execute JS code into victim's browser.

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Proof-of-concept above on the description.

## Suggested Mitigation/Remediation Actions
Sanitize input data from the user to avoid html/XSS injections.



</details>

---
*Analysed by Claude on 2026-05-12*
