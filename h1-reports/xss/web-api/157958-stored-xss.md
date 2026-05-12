# Stored XSS in Instacart Lists Feature

## Metadata
- **Source:** HackerOne
- **Report:** 157958 | https://hackerone.com/reports/157958
- **Submitted:** 2016-08-09
- **Reporter:** s44mux
- **Program:** Instacart
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability was discovered in Instacart's lists feature where user-supplied input in list names was not properly sanitized or encoded before being stored and displayed. An attacker could inject malicious JavaScript payload through the list creation functionality that would execute in the context of any user viewing the affected list.

## Attack scenario
1. Attacker logs into their Instacart account
2. Attacker navigates to Lists and Recipes section
3. Attacker creates a new list with malicious payload in the list name: "></script></title><script>alert(document.domain)</script>
4. Payload is stored in the database without proper sanitization
5. When the list is accessed via the preview URL, the malicious script executes in victim's browser
6. Attacker can steal session cookies, perform actions on behalf of user, or redirect to phishing pages

## Root cause
The application failed to properly validate and encode user input when creating lists. The list name parameter was directly stored and rendered in the DOM without escaping HTML special characters, allowing script injection through tag breaking and script tag injection.

## Attacker mindset
An attacker would recognize that list names are user-controllable input that gets persisted and displayed. By breaking out of the existing context with "></script></title> and injecting a new script tag, they could achieve arbitrary JavaScript execution. The stored nature makes this particularly dangerous as multiple victims could be affected.

## Defensive takeaways
- Implement strict input validation on all user-supplied data, particularly on names/titles that will be stored
- Apply context-appropriate output encoding (HTML entity encoding) when rendering user data in HTML context
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Consider using templating engines that auto-escape by default
- Implement server-side sanitization in addition to client-side validation
- Perform security testing on all input fields, especially those involved in content creation and sharing
- Use parameterized rendering approaches rather than string concatenation

## Variant hunting
Check other list-related features (shopping lists, wish lists, etc.) for similar XSS
Test list description fields if they exist
Test list sharing/collaboration features with XSS payloads
Check recipe creation/editing functionality for similar issues
Test user profile fields and display names
Investigate any other user-generated content features in Instacart

## MITRE ATT&CK
- T1190
- T1204.001
- T1566.002

## Notes
This is a classic stored XSS vulnerability with high impact potential. The preview parameter in the URL suggests the vulnerability persists across different viewing modes. The simplicity of the payload breaking out of script tags indicates weak input validation. The fix would require both input validation (blocklist dangerous patterns or whitelist safe input) and output encoding (HTML entity encoding of user input before rendering).

## Full report
<details><summary>Expand</summary>

First log in account.

We headed to the "lists and recipes" option

https://www.instacart.com/store/demo/lists


create a new list "add list"

Payload
"></script></title><script>alert(document.domain)</script>


URL pwned.

https://www.instacart.com/lists/izy0w6Q?preview=true

attached a screenshot



</details>

---
*Analysed by Claude on 2026-05-12*
