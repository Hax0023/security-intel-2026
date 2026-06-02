# Drag Drop XSS in Google Docs/Sheets/Drawing/Presentation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Google Bug Bounty
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Stored XSS, Insufficient Input Validation, HTML Sanitization Bypass
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google's drawing module (accessible from Docs, Sheets, Drawing, and Presentation) that allowed arbitrary JavaScript execution through drag-and-drop of HTML files containing malicious payloads. The vulnerability exploited improper HTML validation when processing dragged content, specifically leveraging image onerror event handlers that would trigger when images failed to load.

## Attack scenario (step by step)
1. Attacker creates an HTML file containing an img tag with onerror handler: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker crafts the payload using a valid local image path (e.g., from Windows sample pictures) that exists on victim's machine but will break when processed by Google
3. Victim opens Google Docs/Sheets/Drawing and the attacker tricks them into dragging the malicious HTML file into the drawing module
4. Google's drawing module accepts the drag-dropped content and processes it with insufficient validation
5. The image source becomes invalid during Google's processing, triggering the onerror event handler
6. Arbitrary JavaScript executes in the victim's browser within the Google application context

## Root cause
The drawing module failed to properly sanitize HTML content from drag-and-drop operations. It performed image validation checks but did not adequately filter or escape event handler attributes (onerror, onload, onmouseover). The module only validated image sources without preventing malicious event handlers from being embedded.

## Attacker mindset
Research-driven approach to finding attack surface in drag-and-drop functionality. Attacker analyzed differences in server responses to understand validation logic, then creatively exploited the onerror handler execution path by using valid-but-broken image sources. Demonstrated deep understanding of HTML parsing and event handler execution timing.

## Defensive takeaways
- Implement strict HTML sanitization on all user-supplied content, especially drag-dropped files
- Use Content Security Policy (CSP) to prevent inline script execution and restrict event handlers
- Strip all event handler attributes (on*) from HTML content at parse time, not just validate image sources
- Validate not just image existence but also content-type headers and file signatures
- Apply allowlist-based HTML parsing rather than blacklist filtering of dangerous attributes
- Test drag-and-drop functionality with various HTML payloads and event handlers
- Implement server-side conversion/re-encoding of dragged content to remove executable content

## Variant hunting
Search for similar drag-drop XSS in other Google products (Gmail attachments, Drive), other office suites (Microsoft 365, OnlyOffice), and collaborative tools. Test other event handlers beyond onerror (onload, onclick, onmouseover on different element types). Investigate SVG drag-drop as alternative vector. Look for similar issues in data paste operations with different formats (RTF, DOCX, ODT).

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link
- T1566: Phishing - Phishing via Service

## Notes
The vulnerability demonstrated creative exploitation by understanding the application's behavior differences and using valid-but-broken resources. The researcher noted a similar finding was submitted earlier but in a different Google product (Google Images), indicating multiple attack surfaces. The use of system default image paths showed understanding of attack delivery logistics.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
