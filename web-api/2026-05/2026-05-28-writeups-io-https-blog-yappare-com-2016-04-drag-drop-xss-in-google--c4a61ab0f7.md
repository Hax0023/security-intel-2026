# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Google Bug Bounty (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Input Validation Bypass, Drag-and-Drop File Handling
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google's Drawing module (used within Docs/Sheets/Presentation) that allowed attackers to execute arbitrary JavaScript by dragging and dropping a specially crafted HTML file containing an img tag with an onerror event handler. The vulnerability exploited improper HTML validation in the drawing module's file upload and embedding mechanism, where broken image sources would trigger the onerror payload.

## Attack scenario (step by step)
1. Attacker creates a malicious HTML file containing an img tag with a valid local image path (e.g., C:\Users\Public\Pictures\Sample Pictures) and an onerror event handler with XSS payload
2. Attacker shares a Google Docs/Drawing document with a victim and tricks them into opening it
3. Victim drags and drops the malicious HTML file into the Drawing module within the Google document
4. Google's Drawing module processes the dropped file and attempts to extract the image
5. The image path becomes invalid when processed server-side or in the victim's document context, triggering the onerror event
6. The onerror handler executes the attacker's JavaScript payload, compromising the victim's session and document data

## Root cause
The Drawing module performed insufficient validation on dropped HTML files. It only verified whether a valid image could be extracted, but did not properly sanitize HTML tags and event handlers. The implementation allowed img tags with onerror handlers to pass through, and the error condition (broken image source) reliably triggered the payload execution.

## Attacker mindset
The researcher demonstrated sophisticated understanding of how browsers handle broken images and event handlers. They recognized that while Google validated image validity, they didn't sanitize malicious HTML attributes. The use of Windows system image paths showed creativity in ensuring images appeared valid on the attacker's machine but would fail on the victim's side, guaranteeing payload execution.

## Defensive takeaways
- Implement strict HTML sanitization on all user-uploaded or drag-dropped content, not just image validation
- Strip or escape all event handler attributes (onerror, onload, onmouseover, etc.) from any HTML elements before processing
- Use a whitelist approach for allowed tags and attributes rather than blacklist
- Validate file content based on MIME type and file signature, not user-provided paths
- Apply Content Security Policy (CSP) to prevent inline script execution even if sanitization fails
- Treat drag-and-drop file handling with the same security rigor as direct file uploads
- Test HTML parsing across different contexts (local files, URLs, embedded content)

## Variant hunting
Look for similar drag-drop XSS in: other Google products (Forms, Sites, Slides), other collaborative tools (Microsoft Office 365, Notion, Figma), embedded editors within CMS platforms, and any application accepting HTML content through drag-and-drop. Test event handlers beyond onerror (onload, onmouseover, onmousemove, onfocus, onblur). Investigate whether similar issues exist in the main Google Docs/Sheets modules or were only present in the Drawing submodule.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1598 - Phishing: Search Engine
- T1566 - Phishing

## Notes
The vulnerability was marked as a duplicate, but the researcher noted it wasn't affecting Google Images specifically. The research was influenced by prior work from Dr. Mario (@0x6D6172696F) and Harry on similar drag-drop XSS techniques. The vulnerability demonstrates the importance of defense-in-depth; even though the drawing module only accepted images, the HTML parsing weakness allowed XSS. The researcher's use of system-level image paths as a proof-of-concept was clever social engineering combined with technical exploitation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
