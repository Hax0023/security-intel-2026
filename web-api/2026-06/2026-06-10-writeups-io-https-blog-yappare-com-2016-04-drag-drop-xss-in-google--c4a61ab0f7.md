# Drag Drop XSS in Google Docs/Sheets/Drawing/Presentation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Google Bug Bounty Program
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Improper Input Validation, HTML Sanitization Bypass
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google's drawing module (accessible from Docs, Sheets, Presentation) that allowed attackers to execute arbitrary JavaScript by dragging and dropping HTML files containing malicious image tags with event handlers. The vulnerability exploited improper validation of HTML content during the drag-drop upload process, specifically targeting broken image sources that would trigger onerror event handlers.

## Attack scenario (step by step)
1. Attacker creates an HTML file containing a malicious img tag with onerror handler: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker sends the file to victim or hosts it on a location where victim can access it
3. Victim opens the file locally or from attacker's source and drags it into Google's drawing module
4. The drawing module accepts the file and processes the HTML content without proper sanitization
5. When the image fails to load (broken src), the onerror event handler executes JavaScript payload
6. XSS payload executes in victim's browser within Google's trusted context

## Root cause
The drawing module implemented insufficient HTML sanitization during drag-drop file processing. The module validated for valid image presence but failed to strip event handlers (onerror, onload, onmouseover, etc.) from img tags. The validation logic checked if an image could load, but did not account for scenarios where images intentionally reference non-existent paths, allowing event handlers to execute on error states.

## Attacker mindset
Researcher creatively bypassed image validation by using invalid image sources that would still execute event handlers. The attacker recognized that while other event handlers wouldn't trigger without a valid image, onerror would reliably execute on broken images. Using local Windows system paths (C:\Users\Public\Pictures\Sample Pictures) as image sources was a clever technique to make payloads work on victim machines while appearing legitimate.

## Defensive takeaways
- Implement strict HTML sanitization/whitelist approach for all user-uploaded content, removing all event handlers regardless of tag type
- Sanitize HTML at parse time before any rendering or embedding occurs
- Use Content Security Policy (CSP) to prevent inline script execution and event handler execution
- Validate and strip event handler attributes (on*) from all HTML elements during processing
- Apply same security controls across all related modules (Docs, Sheets, Presentation, Drawing) consistently
- Test sanitization against various event handlers and edge cases, not just img tags
- Consider using iframe sandboxing or safer markup languages instead of direct HTML processing

## Variant hunting
['Check if other event handlers work with different file types (video, audio, embed, object tags)', 'Test drag-drop in other Google products for similar HTML processing vulnerabilities', 'Investigate if SVG files with event handlers bypass validation', 'Test if other broken resource types (script src, link href) trigger similar behaviors', 'Check if external URL schemes (file://, data://, blob://) can be exploited for XSS', 'Test nested HTML structures and encoding bypasses in drag-drop handlers', 'Look for similar patterns in other collaborative editing tools (Office 365, Notion, etc.)']

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1539

## Notes
Original vulnerability was discovered by Harry Makarovich and patched in main Google Docs interface. This writeup documents a duplicate/variant affecting the drawing module that was not fixed at time of submission. The researcher's use of system image paths as a vector was particularly clever for ensuring payload execution on target systems. Research was inspired by Dr. Mario's presentation on copy-paste XSS vectors from OpenOffice, showing the importance of studying content exchange mechanisms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
