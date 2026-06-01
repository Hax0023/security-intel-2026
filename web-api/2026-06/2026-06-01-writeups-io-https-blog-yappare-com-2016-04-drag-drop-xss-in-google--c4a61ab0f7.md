# Drag Drop XSS in Google Docs/Sheets/Drawing via Broken Image onerror Handler

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Google Bug Bounty Program
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Improper Input Validation, Drag-and-Drop Handler Vulnerability
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google Docs/Sheets/Drawing module that allowed arbitrary JavaScript execution through drag-and-drop functionality. By uploading an HTML file containing an img tag with an invalid src and onerror handler, the XSS payload would execute when the broken image triggered the error event. The vulnerability exploited inadequate HTML sanitization when processing user-dragged content into the drawing module.

## Attack scenario (step by step)
1. Attacker crafts an HTML file containing payload: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker hosts or creates a file that appears as valid image content to victim
3. Victim drags the HTML/image file into Google Docs/Sheets Drawing module
4. Drawing module accepts the content without proper sanitization
5. Module attempts to load the invalid image source, triggering onerror event
6. JavaScript payload executes in victim's browser with victim's privileges

## Root cause
The Drawing module's drag-and-drop handler validated only the presence of an image element but failed to sanitize HTML attributes like onerror before processing. The validation logic checked for image validity but did not strip event handlers, allowing arbitrary code execution when image loading failed.

## Attacker mindset
The researcher observed that Google's validation differed based on whether content was a valid image or not. By combining a structurally valid img tag with an intentionally broken src attribute, they bypassed image validation while preserving the malicious onerror handler. The use of a common Windows system image path demonstrated social engineering awareness to ensure victims had the resource available.

## Defensive takeaways
- Implement strict HTML sanitization on all drag-and-drop input, removing event handlers (onerror, onload, onclick, etc.)
- Use allowlist-based validation rather than blacklist when processing user content
- Parse and validate HTML separately from displaying it; sanitize before rendering
- Apply Content Security Policy (CSP) headers to prevent inline script execution
- Validate image content server-side by verifying MIME type and image headers, not just file extension
- Disable execution of event handlers on dynamically inserted HTML elements
- Test drag-and-drop functionality specifically for XSS vectors and malformed content

## Variant hunting
Search for similar drag-and-drop XSS in: Google Drive, OneDrive, Dropbox, Notion, Figma, and other collaborative tools. Test other event handlers (onload, onmouseover, oninput) on different element types (img, svg, video, iframe). Examine copy-paste functionality in addition to drag-drop, as format conversion can bypass filters.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566.002: Phishing - Spearphishing Link
- T1059.007: Command and Scripting Interpreter - JavaScript

## Notes
This vulnerability was initially discovered by Harry and fixed in Google Docs, but the drawing module in Google Docs/Sheets/Presentation inherited the same vulnerable code path. The writeup mentions the submission became a duplicate on Google Images, suggesting multiple researchers discovered similar variants. The clever use of onerror (rather than other handlers) was key to bypassing validation logic that only checked for image presence.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
