# Stored XSS in Post Title

## Metadata
- **Source:** HackerOne
- **Report:** 942859 | https://hackerone.com/reports/942859
- **Submitted:** 2020-07-26
- **Reporter:** zerox4
- **Program:** Imgur
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Sanitization, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the post title field where unsanitized user input is persisted and executed in victim browsers. The vulnerability allows attackers to inject malicious JavaScript that executes whenever the post is viewed, potentially compromising user sessions and cookies.

## Attack scenario
1. Attacker crafts a malicious post title containing JavaScript payload (e.g., <script>alert('XSS')</script> or <img src=x onerror=alert('XSS')>)
2. Attacker creates/submits a post with the malicious title through the normal post creation interface
3. The application stores the unsanitized title in the database without proper validation or encoding
4. When legitimate users visit the post page or search results, the malicious script is reflected in the DOM
5. The victim's browser executes the injected JavaScript in the context of the Imgur domain
6. Attacker's payload exfiltrates session cookies, performs actions on behalf of the user, or redirects to phishing site

## Root cause
The application fails to properly sanitize and encode user-supplied input in the post title field before storage. On retrieval, the title is rendered directly into the HTML response without contextual output encoding, allowing script execution.

## Attacker mindset
An attacker recognizes that post titles are user-controlled, rendered publicly, and likely trusted by the application. By testing basic XSS payloads, they identify the stored variant which is more severe than reflected XSS due to persistent impact across all users viewing the content.

## Defensive takeaways
- Implement input validation with strict whitelisting of allowed characters in titles (alphanumeric, basic punctuation)
- Apply HTML entity encoding (e.g., <, >, &, ", ') to all user input before storage or use a templating engine with automatic escaping
- Use Content Security Policy (CSP) headers to restrict script execution sources
- Implement output encoding specific to the context (HTML, JavaScript, URL, CSS) where data is rendered
- Conduct security code review of all user input handling paths
- Perform automated XSS testing during CI/CD pipeline
- Implement DOM-based XSS protections and use frameworks that auto-escape by default

## Variant hunting
Look for XSS in other user-controllable fields: post descriptions, comments, user profile fields, hashtags, image titles, captions, search queries. Test for bypass techniques using encoding (URL, double, Unicode), case variation, HTML comments, SVG elements, event handler variations, and DOM manipulation techniques.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
Report appears minimal with only PoC link provided. The imgur.com/gallery URL structure suggests the XSS persists in gallery/public-facing content. Session/cookie theft implies HttpOnly flags may not be set appropriately. Timeline and resolution status not documented in excerpt.

## Full report
<details><summary>Expand</summary>

Hello,

Stored XSS in Post title, example: https://imgur.com/gallery/Y5JUzv3,

Thanks

## Impact

steal cookies and session

</details>

---
*Analysed by Claude on 2026-05-12*
