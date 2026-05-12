# XSS in Request Approvals via Project Settings

## Metadata
- **Source:** HackerOne
- **Report:** 402658 | https://hackerone.com/reports/402658
- **Submitted:** 2018-08-29
- **Reporter:** circuit
- **Program:** Unknown (HackerOne Report #402658)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Input Validation Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the project settings where user-supplied input in a username field is not properly sanitized before being rendered in request approval contexts. An attacker can inject malicious JavaScript by entering crafted payloads in the username field, which executes when the approval request is viewed.

## Attack scenario
1. Attacker navigates to project settings in the vulnerable application
2. Attacker pastes a malicious JavaScript payload (e.g., <img src=x onerror=alert(1)>) in the username or related field
3. Attacker clicks to confirm or save the settings
4. The payload is stored in the database without proper HTML encoding or sanitization
5. When another user views the request approvals page, the stored XSS payload executes in their browser
6. Attacker can steal session tokens, credentials, or perform unauthorized actions on behalf of the victim

## Root cause
The application fails to properly encode or sanitize user input in project settings before storing and rendering it in the request approvals feature. Output encoding is either missing or insufficient when displaying the username field in approval contexts.

## Attacker mindset
Low effort, high impact attack. The attacker identified a simple injection point in settings that persists data and is displayed without sanitization. This is a common oversight in web applications where input validation occurs at the form level but output encoding is neglected.

## Defensive takeaways
- Implement context-aware output encoding (HTML entity encoding for HTML context, JavaScript encoding for JavaScript context)
- Apply input validation and whitelist acceptable characters for username fields
- Use a security library or templating engine with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Apply the principle of least privilege to approval workflows
- Conduct security testing including XSS payload testing in all user-input fields
- Implement server-side validation and sanitization for all stored data

## Variant hunting
Test all project settings fields for stored XSS (description, tags, metadata)
Check approval request templates and notification email generation for XSS
Test other user-facing features that display project settings data
Look for similar patterns in team settings, user profiles, and group configurations
Test SVG/image upload fields in settings for stored XSS via file content
Check API endpoints that return project settings for proper JSON encoding

## MITRE ATT&CK
- T1190
- T1566

## Notes
This appears to be a straightforward stored XSS vulnerability with minimal complexity. The writeup lacks technical detail (no actual payload shown, only references to attachments), making reproduction slightly unclear. The 'link777' reference suggests the payload may have been injected into a URL or link field. The vulnerability likely affects any user with project settings access, with impact reaching all users who view the approval requests.

## Full report
<details><summary>Expand</summary>

Hello, team!

I found xss.

Steps to reproduce:

1.  Open project settings
2.  paste in this field link777
{F339770}
3. click on result
{F339772}

In the username, a XSS poc should be written, like mine.

## Impact

XSS.

</details>

---
*Analysed by Claude on 2026-05-12*
