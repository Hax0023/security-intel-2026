# Drag Drop XSS in Google Docs/Sheets/Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Google Bug Bounty
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Stored XSS, Improper Input Validation, Client-side File Handling
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A Stored XSS vulnerability was discovered in Google Docs/Sheets/Drawing/Presentation modules through drag-and-drop file upload. By dragging an HTML file containing XSS payload into the drawing module, an attacker could execute arbitrary JavaScript. The vulnerability exploited improper HTML validation when files were processed as images, specifically using img tags with broken src attributes to trigger onerror handlers.

## Attack scenario (step by step)
1. Attacker crafts an HTML file containing malicious img tag with onerror event handler: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker disguises or serves the HTML file in a way that appears as a valid image to initial validation checks
3. Victim opens Google Docs/Sheets/Drawing module and drags the malicious HTML file into the drawing interface
4. Google's drawing module accepts the file, processes the HTML content, and fails to properly sanitize event handlers
5. The img tag is embedded in the document with invalid src attribute, triggering the onerror event
6. Arbitrary JavaScript payload executes in victim's browser context with access to Google Docs session

## Root cause
The drawing module in Google's office suite performed insufficient validation of uploaded HTML content. While the module appeared designed to handle images only, it accepted and processed HTML files without properly sanitizing or escaping event handler attributes. The validation logic only checked for valid image sources but did not strip dangerous HTML attributes like onerror, onload, and onmouseover before embedding content.

## Attacker mindset
The researcher demonstrated lateral thinking by analyzing Google's validation behavior across different payload types. Upon discovering that only onerror handlers would execute (due to broken image src), they creatively solved the practical challenge of making images appear valid initially but become broken in the victim's context by referencing Windows system sample images. This shows methodical exploitation through behavior analysis and constraint-based problem solving.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) to restrict inline script execution and event handlers
- Use allowlist-based validation for file uploads rather than blocklist approaches
- Sanitize all user-supplied HTML content using well-tested libraries (e.g., DOMPurify, Bleach) that strip dangerous attributes
- Reject or convert uploaded files to safe formats (e.g., convert HTML to plaintext or safe image formats)
- Implement server-side file type validation based on MIME types and file signatures, not just extensions
- Apply context-aware output encoding when embedding user content
- Test drag-and-drop functionality with various file types and payloads beyond expected inputs
- Monitor for XSS patterns in event handler attributes across all modules

## Variant hunting
Test drag-drop XSS in: (1) Other Google products with file upload/embedding features (Slides, Forms, Sheets charts); (2) Similar office productivity suites (Microsoft Office Online, Notion, Airtable); (3) Try alternative event handlers and SVG-based payloads; (4) Test with different file type disguises (double extensions, MIME type mismatches); (5) Attempt to bypass validation via encoding (URL encoding, Unicode, HTML entities); (6) Test cross-origin drag-drop scenarios; (7) Explore other broken resource scenarios (video, audio, iframe with invalid src)

## MITRE ATT&CK
- T1190
- T1059
- T1071

## Notes
The researcher noted this vulnerability remained unpatched in the drawing module despite a similar issue being fixed in Google Docs. A duplicate submission from another researcher on Google Images suggests the vulnerability pattern was more widespread. The clever use of Windows sample images as a practical exploit vector demonstrates understanding of victim environment assumptions. The writeup references prior research by Dr. Mario on copy-paste XSS from OpenOffice, suggesting this is part of a broader class of office suite HTML handling vulnerabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
