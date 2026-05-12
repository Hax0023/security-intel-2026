# Reflected XSS in Wiki Attachment Editor (doeditattachment.action)

## Metadata
- **Source:** HackerOne
- **Report:** 866433 | https://hackerone.com/reports/866433
- **Submitted:** 2020-05-05
- **Reporter:** meryem0x
- **Program:** Topcoder
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Output Encoding, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the wiki attachment editing functionality at doeditattachment.action where user-supplied filename parameters are rendered without proper HTML encoding. An attacker can craft a malicious URL containing JavaScript payload in the fileName parameter to execute arbitrary code in victims' browsers.

## Attack scenario
1. Attacker identifies that the doeditattachment.action endpoint reflects the fileName parameter in error messages without encoding
2. Attacker crafts a URL with malicious JavaScript payload in the fileName parameter: s"><img src=X onerror=alert(document.domain)>ss.svg
3. Attacker socially engineers or tricks a victim into clicking the malicious link
4. Victim's browser processes the reflected payload and executes the JavaScript code
5. Attacker's script executes in the victim's session context with access to cookies, session tokens, and sensitive data
6. Attacker can steal authentication tokens, perform actions on behalf of the user, or redirect to phishing pages

## Root cause
The application fails to HTML-encode the fileName parameter before reflecting it back in error messages on the doeditattachment.action endpoint. The error handling path accepts untrusted user input and outputs it directly without sanitization, allowing JavaScript injection.

## Attacker mindset
The attacker recognized that error pages often echo back user input for debugging purposes and are frequently overlooked in security reviews. By manipulating the fileName parameter during a simulated attachment upload error, they discovered the application reflects the payload unencoded, enabling straightforward XSS execution.

## Defensive takeaways
- Implement strict output encoding for all user-supplied input reflected in HTML context (use HTML entity encoding)
- Apply input validation to restrict fileName to expected patterns (alphanumeric, dots, hyphens only)
- Use a templating engine with automatic context-aware encoding rather than manual string concatenation
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if reflected
- Apply the principle of least privilege - avoid echoing back unnecessary user input in error messages
- Perform security review of all error handling and redirect paths, not just main application flows
- Implement automated testing for XSS in both successful and error code paths

## Variant hunting
Check other action endpoints (*attachment.action, *edit.action, etc.) for similar reflection patterns
Test pageId parameter for XSS - may also be reflected without encoding
Review all error message generation code for unencoded user input reflection
Test other wiki-related endpoints (viewpage, editpage) for similar vulnerabilities
Check if fileName parameter is vulnerable to other injection types (SVG/XML, path traversal)
Test with different file extensions to bypass potential extension-based filters
Review redirect parameters and confirm they implement safe redirects

## MITRE ATT&CK
- T1190
- T1566.002
- T1047

## Notes
The vulnerability is particularly dangerous in enterprise wiki/collaboration platforms where users trust internal documentation links. The PoC uses IMG onerror technique to bypass basic filters. The SVG file extension in the payload demonstrates polyglot technique to appear legitimate while containing executable code.

## Full report
<details><summary>Expand</summary>

## Summary:

Hi :) A reflected XSS occurs on https://apps.topcoder.com/wiki/pages/doeditattachment.action when editing wiki pages attachments.

## Steps To Reproduce:

A user can add attachments on https://apps.topcoder.com/wiki/pages/viewpageattachments.action?pageId=165871793 a wiki page and can edit on https://apps.topcoder.com/wiki/pages/editattachment.action?pageId=165871793&fileName=sss.svg. If there is an error, user redirected to `doeditattachment` path with an error message. An attacker can change the filename parameter and add JS codes. When a victim opens this url, XSS will execute. 

PoC:
https://apps.topcoder.com/wiki/pages/doeditattachment.action?pageId=165871793&fileName=s%22%3E%3Cimg%20src=X%20onerror=alert(document.domain)%3Ess.svg
{F816100}

## Impact

XSS can use to steal cookies or to run arbitrary code on victim's browser.

</details>

---
*Analysed by Claude on 2026-05-12*
