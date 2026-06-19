# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Google Bug Bounty (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Drag-and-Drop File Handling
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google's drawing module through drag-and-drop functionality. By dragging an HTML file containing XSS payload with a broken image source into the drawing module, the onerror event handler executes when the image fails to load. The vulnerability exploited improper HTML validation when processing user-dragged content.

## Attack scenario (step by step)
1. Attacker crafts an HTML file containing payload: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker hosts or provides this file to victim user with a valid image reference that exists locally (e.g., C:\Users\Public\Pictures\Sample Pictures)
3. Victim's browser initially loads the image successfully from local filesystem
4. Victim drags the HTML file into Google Docs drawing module
5. Google Docs processes the drag-drop event and inserts the img tag without sanitizing event handlers
6. Image src fails to resolve in Google Docs context, triggering onerror event and executing malicious JavaScript

## Root cause
The drawing module's HTML content processor validated that an image source exists but failed to sanitize event handler attributes (onerror, onload, onmouseover). The validation only checked image availability, not the safety of the HTML markup containing the image reference.

## Attacker mindset
Attacker recognized that drag-drop operations bypass standard upload security checks. By leveraging local image paths that work during initial load but fail in the target context, they bypassed image validation logic. The focus on onerror (vs onload) was tactical, as only broken images trigger that handler, making detection harder.

## Defensive takeaways
- Sanitize all HTML markup from drag-drop events, not just validate file types/sources
- Strip event handler attributes (on*) from pasted/dropped HTML content
- Use allowlist-based HTML parsing rather than blacklist approaches
- Implement Content Security Policy (CSP) to block inline script execution
- Apply same validation logic to drag-drop, copy-paste, and file upload workflows
- Test with polyglot files and multi-format content (OpenOffice, HTML hybrids)

## Variant hunting
Search for similar drag-drop XSS in: Google Slides presentations, other Google productivity apps, Microsoft Office online, Notion, Figma, and any WYSIWYG editors. Test dragging HTML files with other event handlers (ondrag, ondrop, onpaste) and various image sources (data URIs, blob URLs). Check if similar bypass exists with SVG embedded in image drag operations.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing: Spearphishing Link
- T1566 - Phishing: Phishing with Malicious Attachment
- T1059 - Command and Scripting Interpreter

## Notes
This submission was marked as duplicate of another researcher's finding (likely Harry's earlier Google Docs XSS), but the researcher notes it wasn't in Google Images specifically. The attack's elegance lies in exploiting the temporal window between local image availability and cloud context failure. The onerror handler constraint narrowed the attack surface but didn't eliminate it. Published April 2016, indicating this was a persistent issue across multiple Google products despite earlier fixes in main Docs module.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
