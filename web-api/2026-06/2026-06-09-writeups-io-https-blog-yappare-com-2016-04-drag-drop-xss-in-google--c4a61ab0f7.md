# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Google (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not explicitly stated (marked as duplicate)
- **Severity:** High
- **Vuln types:** Stored XSS, Input Validation Bypass, Drag-and-Drop File Handling
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google Docs' drawing module that allowed attackers to inject malicious code through drag-and-drop functionality. The vulnerability exploited improper HTML validation when processing dragged files, specifically by crafting HTML files containing image tags with XSS payloads that execute on broken image sources.

## Attack scenario (step by step)
1. Attacker crafts an HTML file containing an img tag with onerror handler: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker drags and drops this HTML file into the drawing module of Google Docs/Sheets/Presentation
3. Google's drawing module processes the dragged file and extracts the image tag for validation
4. Since the image source references a non-existent file, the image fails to load and the onerror event triggers
5. The malicious JavaScript payload executes in the victim's browser within the Google Docs context
6. If stored in a shared document, the payload executes for all users who view the document

## Root cause
The drawing module's validation logic only checked for valid image sources but did not properly sanitize HTML tags and event handlers during the drag-and-drop import process. The module failed to strip or escape onerror, onload, and other event attributes from imported HTML content, allowing arbitrary code execution when image loading failed.

## Attacker mindset
The attacker recognized that while Google fixed similar XSS issues in the main Docs module, the drawing submodule was overlooked. They leveraged the insight that error events (onerror) execute even when images fail to load, and creatively used local Windows system paths to ensure images would fail on victims' machines while appearing valid during initial analysis.

## Defensive takeaways
- Implement strict HTML sanitization for all drag-and-drop file imports, not just document paste operations
- Use allowlist-based approaches for HTML tags and attributes rather than blacklist filtering
- Strip all event handler attributes (on*) during HTML import and sanitization
- Apply consistent security validation across all modules and features, not just primary functionality
- Test error conditions and edge cases (broken images, invalid sources) during security review
- Consider converting user-provided HTML to safe formats (SVG, canvas) rather than preserving raw HTML
- Implement Content Security Policy (CSP) headers to prevent inline script execution

## Variant hunting
['Test other Google products with drag-and-drop functionality (Forms, Slides, Drawings)', 'Attempt other event handlers beyond onerror (onload, onmouseover, onmouseenter, ontouchstart)', 'Try SVG-based XSS payloads via drag-and-drop', 'Test with data URIs and base64-encoded payloads in src attributes', 'Explore other file types (PDF, Office documents) with embedded content', 'Test collaborative features - whether XSS persists across user sessions', 'Investigate if other Google properties inherit the vulnerable drawing module code']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol (via drag-and-drop import)
- T1598 - Phishing
- T1566 - Phishing (Attachment)
- T1204 - User Execution

## Notes
The vulnerability was ultimately marked as a duplicate by another researcher. The writeup notably emphasizes creative thinking: using legitimate Windows system image paths to ensure images would be broken on victim machines while remaining valid during initial inspection. This demonstrates how attackers combine local system knowledge with web vulnerabilities. The researcher credited Dr. Mario's earlier research on copy-paste XSS from OpenOffice formats, showing how similar attack vectors can exist across different contexts.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
