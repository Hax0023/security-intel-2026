# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Google Bug Bounty Program
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Improper Input Validation, Client-side Code Injection
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google Docs/Sheets/Presentation drawing module where users could drag and drop HTML files containing XSS payloads. The vulnerability exploited improper validation of dragged content and execution of onerror event handlers when image sources failed to load, allowing arbitrary JavaScript execution.

## Attack scenario (step by step)
1. Attacker creates a malicious HTML file with embedded XSS payload in an img tag with onerror handler: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker uses a valid Windows system image path (e.g., C:\Users\Public\Pictures\Sample Pictures) as the initial src to bypass client-side image validation checks
3. Attacker sends the HTML file to victim or hosts it for download
4. Victim opens Google Docs/Sheets/Presentation and accesses the drawing module
5. Victim drags and drops the malicious HTML file into the drawing canvas
6. Google Docs validates and processes the file, but the image source becomes broken in the target context, triggering the onerror event handler and executing the JavaScript payload

## Root cause
The drawing module in Google Docs failed to properly sanitize and validate HTML content during drag-and-drop operations. While it checked for valid image sources, it did not strip event handlers or prevent execution of JavaScript when image loading failed. The validation occurred on the source filename rather than the actual content or event attributes.

## Attacker mindset
The researcher demonstrated creative bypass techniques by understanding Google's validation logic. Rather than using obviously malicious payloads, they leveraged the onerror event handler (while onload and onmouseover failed) and used trusted local image paths to pass initial validation. This shows sophisticated understanding of validation boundaries and error handling behavior.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) to prevent inline script execution from drag-drop content
- Sanitize all HTML content from user uploads using allowlist-based HTML sanitization libraries (e.g., DOMPurify)
- Strip all event handlers (onerror, onload, onmouseover, etc.) from user-provided HTML
- Validate and process user content server-side rather than relying on client-side validation alone
- Do not process raw HTML from drag-drop operations; convert to plain text or structured data formats first
- Apply same security controls to all modules (Docs, Sheets, Presentation, Drawing) consistently
- Use sandboxing/iframes with restrictive permissions for user-provided content rendering
- Test all event handler vectors, not just common ones like onload

## Variant hunting
['Test other event handlers beyond onerror: onwheel, ontouchstart, onanimationstart, onanimationend, ontransitionend', 'Try SVG drag-drop with embedded script tags or event handlers', 'Test with other Google products (Forms, Sites, Slides) for similar drag-drop vulnerabilities', 'Attempt encoded payloads (URL encoding, HTML entities, Unicode) in image src attributes', 'Test with data URIs: data:text/html,<script>alert(0)</script>', 'Explore other Office document formats (DOCX, XLSX) when dragged into Google Docs', 'Test drag-drop of CSS files with expression() or other injection vectors', 'Attempt polyglot files that are valid images with embedded HTML/JS']

## MITRE ATT&CK
- T1190
- T1659

## Notes
This vulnerability was notable for bypassing Google's existing fixes to similar issues. The researcher's insight about using system image paths to pass validation checks demonstrates understanding of trust boundary exploitation. The submission was marked as duplicate of another researcher's finding in Google Images, but the drawing module variant remained unpatched at time of publication (April 2016).

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
