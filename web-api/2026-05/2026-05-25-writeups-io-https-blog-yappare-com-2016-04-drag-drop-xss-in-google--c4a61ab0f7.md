# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Google Bug Bounty (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Improper Input Validation, Drag and Drop Handler Vulnerability
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google's Drawing module (part of Docs/Sheets/Presentation suite) through drag-and-drop functionality. By dragging an HTML file containing an XSS payload with a broken image source into the drawing module, the onerror event handler would execute when the image failed to load. The vulnerability existed due to improper HTML validation when processing drag-dropped content.

## Attack scenario (step by step)
1. Attacker creates a malicious HTML file containing <img src=nonvalid.jpg onerror=alert(0)> payload
2. Attacker shares the file or tricks a victim into opening it
3. Victim drags the HTML file into the Google Drawing module
4. Drawing module accepts the content and attempts to process it as an image
5. Image source fails to load, triggering the onerror event handler
6. XSS payload executes in victim's browser with full document context

## Root cause
The Drawing module's drag-and-drop handler insufficiently validated HTML content before embedding it. The module only checked for valid image sources but did not sanitize or escape HTML attributes like event handlers. When an image source was invalid, error handlers (onerror, onload, onmouseover) were still executable, allowing arbitrary JavaScript execution.

## Attacker mindset
Researcher recognized that while Google patched similar XSS in the main Docs module, the Drawing submodule was overlooked. They analyzed the differential response behavior, identified that broken images trigger error events, and strategically used local Windows sample images to ensure payload execution on victim systems while maintaining the broken state after drag-drop.

## Defensive takeaways
- Implement Content Security Policy (CSP) to restrict event handler execution
- Use HTML sanitization libraries to strip dangerous attributes from user-supplied content
- Apply whitelist-based validation for drag-drop handlers, rejecting non-image files
- Escape HTML entities in all user-controlled content before embedding
- Test all modules and submodules consistently when patching XSS across related features
- Monitor error event handlers as attack vectors, not just success paths
- Validate file types server-side, not relying on client-side drag-drop validation

## Variant hunting
Similar drag-and-drop XSS patterns could exist in: other Google productivity suite modules (Forms, Keep, Slides), third-party document editors, collaborative platforms with drag-drop file handling, rich text editors that process external content, and design tools that accept SVG or image uploads with insufficient sanitization.

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1566 Phishing
- T1059 Command and Scripting Interpreter

## Notes
Writeup notes the finding was submitted as duplicate in Google Images context but not in the Drawing module specifically. The researcher's innovation was understanding that broken local image sources (from C:\Users\Public\Pictures\Sample Pictures) would trigger onerror handlers. This demonstrates the importance of testing attack scenarios beyond the obvious success path and considering how victim environment differences affect payload behavior.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
