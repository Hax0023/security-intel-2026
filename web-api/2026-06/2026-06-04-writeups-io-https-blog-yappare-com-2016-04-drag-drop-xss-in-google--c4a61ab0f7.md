# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Google Bug Bounty (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not explicitly stated
- **Severity:** High
- **Vuln types:** Stored XSS, Improper Input Validation, File Upload Vulnerability
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google's Drawing module (within Docs/Sheets/Presentation) that allowed attackers to execute arbitrary JavaScript by drag-dropping HTML files containing malicious payloads. The vulnerability exploited improper validation of uploaded content and the onerror event handler execution when images fail to load. The attack bypassed security measures by leveraging local Windows sample images that would fail to load in the Google Docs context, triggering XSS execution.

## Attack scenario (step by step)
1. Attacker creates an HTML file containing an img tag with a valid local Windows path (e.g., C:\Users\Public\Pictures\Sample Pictures) and an onerror event handler with malicious JavaScript: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker crafts the payload such that the image path is valid on the victim's local machine, appearing legitimate during preview/file inspection
3. Victim opens the HTML file locally or receives it via email/download, and the image initially appears valid
4. Victim drags and drops the HTML file into Google Docs Drawing module
5. Google's Drawing module processes the content and uploads it, but fails to properly validate/sanitize the HTML markup
6. The image source becomes invalid in Google's context (since local C:\ paths cannot load), triggering the onerror event handler and executing the attacker's JavaScript payload in the victim's browser within Google Docs context

## Root cause
The Drawing module implementation failed to properly sanitize user-supplied HTML content during drag-drop operations. The application parsed and preserved dangerous event handlers (onerror, onload, onmouseover) instead of stripping them. Additionally, the validation logic only checked for valid image sources but did not prevent event handler attributes in img tags, and did not account for paths that would become invalid after upload.

## Attacker mindset
The attacker demonstrated sophisticated understanding of browser security contexts and file system behaviors across operating systems. By weaponizing the onerror event specifically (rather than onload/onmouseover), they identified which handlers were executable in the Drawing module's context. The use of legitimate Windows sample pictures showed clever social engineering—appearing valid initially while becoming broken upon upload. The researcher also demonstrated methodical testing against different payloads and careful observation of Google's response variations to identify the vulnerability.

## Defensive takeaways
- Implement strict HTML sanitization/filtering for all user-uploaded or pasted content, removing dangerous attributes (onerror, onload, onclick, etc.) and event handlers
- Use content security policies (CSP) with strict img-src and script-src directives to prevent inline event handlers from executing
- Validate and whitelist image sources before processing; reject local file paths (file://) and paths that cannot be resolved
- Parse uploads as plain text or binary data rather than as HTML/XML to prevent markup interpretation
- Implement server-side validation that strips or rejects all HTML-like content in drag-drop operations
- Apply sandboxing and iframe isolation for user-generated content rendering
- Regularly audit file upload/paste functionality across all modules (Docs, Sheets, Drawings, Presentations) for consistent security controls

## Variant hunting
Similar vulnerabilities likely exist in: (1) other Google Workspace applications with rich content import features, (2) any drag-drop functionality accepting multiple MIME types, (3) content conversion tools (OpenOffice, LibreOffice, Microsoft Office online versions) that process pasted/dropped HTML, (4) email clients with WYSIWYG editors accepting drag-drop uploads, (5) collaborative tools (Figma, Miro, Notion) with similar drawing/canvas modules, (6) other onerror-based XSS vectors through SVG or object tag injection via drag-drop

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1059

## Notes
This vulnerability demonstrates the classic XSS attack surface expansion in web applications—drag-drop is often treated as a separate input vector and may bypass validation applied to paste/upload mechanisms. The researcher's observation that Google's response differed based on payload validity was key to discovering this. The finding highlights that fixing XSS in one module (Docs main editor) doesn't guarantee fixes across all related modules (Drawing module). The use of onerror specifically (rather than onload) shows the importance of testing all possible event handlers, not just common ones.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
