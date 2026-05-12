# Cross Site Scripting (XSS) in Login Page - Firefox Browser Specific

## Metadata
- **Source:** HackerOne
- **Report:** 2587844 | https://hackerone.com/reports/2587844
- **Submitted:** 2024-07-06
- **Reporter:** prakhar0x01
- **Program:** HackerOne (Program redacted)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Reflected XSS, Improper Input Validation, Unvalidated URL Parameter
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Login.html page where the 'ErrMsg' parameter is insufficiently sanitized, allowing arbitrary JavaScript execution in Firefox browsers. The vulnerability requires user interaction via a specific keyboard shortcut (ALT+SHIFT+X on Windows/Linux, CTRL+ALT+X on macOS) to trigger the payload.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the ErrMsg parameter
2. Attacker sends the crafted link to victim via phishing email, chat, or social engineering
3. Victim opens the link in Firefox browser and navigates to the Login.html page
4. Victim presses the required keyboard shortcut (ALT+SHIFT+X or CTRL+ALT+X depending on OS)
5. The injected JavaScript executes in the victim's browser context with their privileges
6. Attacker could steal session cookies, credentials, or perform actions on behalf of the victim

## Root cause
The ErrMsg URL parameter is directly reflected into the HTML response without proper encoding or sanitization, and Firefox interprets the crafted payload when triggered by specific keyboard input

## Attacker mindset
While this is a valid XSS, the attacker must convince the user to perform a specific keyboard action, which significantly reduces exploitability compared to automatic payload execution. However, a sophisticated attacker could combine this with social engineering or keyboard event hijacking techniques.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data reflected in HTML context
- Use parameterized/templated approaches to prevent HTML injection
- Apply Content Security Policy (CSP) headers to restrict script execution
- Validate and sanitize all URL parameters on both client and server side
- Test XSS vulnerabilities across multiple browsers and versions
- Implement HTTP-only and Secure flags on session cookies
- Use security libraries for HTML encoding (e.g., OWASP ESAPI)

## Variant hunting
Check for similar parameter injection in other login-related pages; investigate other error message parameters in the application; test 'open' parameter for additional injection vectors; check if other browsers have similar keyboard shortcut vulnerabilities; search for other unvalidated URL parameters in the same domain

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539

## Notes
The browser-specific nature and keyboard shortcut requirement significantly limits the practical exploitability of this vulnerability. However, it represents a gap in input validation that could potentially be combined with other attack vectors. The redacted domain and researcher name suggest this was from an active program. This type of XSS is sometimes missed in security testing that focuses only on immediate payload execution without browser-specific triggers.

## Full report
<details><summary>Expand</summary>

Hii Team,

Through researching your asset, I found a XSS vulnerability at `www.███.████████`.

**The only concern is that it only works in the Firefox browser.**

## Impact

An attacker could execute arbitrary javascript in the client browser.

## System Host(s)
www.███.██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1 - Open Firefox browser.
2 - Navigate to `https://www.██████.███████/852585B6003EBA25/Login.html?open&ErrMsg=invalidlogin%22%20test=%22X%22%20onclick=%22confirm(%27H4CKED%20BY%20PRAKHAR0X01%27)`
3 - Press : `ALT+SHIFT+X` on **Windows/Linux**, and on **OS X**, it’s `CTRL+ALT+X`.

**_NOTE: we need to convince the user to press a specific key combination. In Firefox on Windows/Linux, it’s `ALT+SHIFT+X`, and on OS X, it’s `CTRL+ALT+X`._**

███████

## Suggested Mitigation/Remediation Actions
- Sanitize the input effectively.



</details>

---
*Analysed by Claude on 2026-05-12*
