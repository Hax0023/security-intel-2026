# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Google Bug Bounty (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, File Upload Validation Bypass
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google's Drawing module (embedded in Docs/Sheets/Presentation) through drag-and-drop functionality. By crafting an HTML file with an XSS payload disguised as an image with a broken src attribute, an attacker could execute arbitrary JavaScript when the victim dragged the file into the drawing canvas.

## Attack scenario (step by step)
1. Attacker creates an HTML file containing <img src=nonvalid.jpg onerror=alert(0)> payload
2. Attacker tricks victim into dragging the HTML file into Google Docs/Sheets Drawing module
3. Drawing module attempts to process the file as an image resource
4. Module validates presence of an image but fails to properly sanitize HTML/event handlers
5. Image source fails to load (broken reference), triggering the onerror event handler
6. Arbitrary JavaScript executes in victim's browser with access to their Google account context

## Root cause
The Drawing module's validation logic only checked for the presence of valid image sources but failed to sanitize HTML attributes and event handlers. The module only validated if an image exists, not if the HTML markup itself was malicious. The onerror handler executes when an image fails to load, providing an execution vector for JavaScript payload.

## Attacker mindset
Understanding that validation mechanisms often check only the happy path (valid image loads). By intentionally breaking the image source while embedding event handlers, the attacker bypassed validation while ensuring payload execution. The creativity in using local Windows sample pictures as valid references shows reconnaissance of common system configurations to increase success rates.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) to prevent inline script execution
- Sanitize all HTML input, not just image sources; strip event handlers (onerror, onload, etc.) from any user-supplied content
- Parse and validate file uploads at binary level, not just by file extension or HTML attributes
- Apply HTML entity encoding and use allowlist-based filtering for drag-drop operations
- Implement server-side re-validation of uploaded content before storage
- Use iframe sandboxing for user-generated content in collaborative tools
- Apply defense-in-depth: validate on client, server, and upon rendering

## Variant hunting
Search for similar drag-drop XSS in collaborative tools (Figma, Miro, Notion). Investigate other event handlers beyond onerror (onload, onmouseover, etc.) in different contexts. Test other Google products with drag-drop functionality. Examine SVG drag-drop implementations which may have similar sanitization gaps.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing (if used in targeted attack)

## Notes
This vulnerability was eventually marked as duplicate; another researcher submitted a similar finding in Google Images before this one. The writeup demonstrates the importance of understanding not just what validation exists, but how it fails under edge cases. The attacker's use of intentionally broken image references to trigger error handlers is a creative bypass of image validation logic.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
