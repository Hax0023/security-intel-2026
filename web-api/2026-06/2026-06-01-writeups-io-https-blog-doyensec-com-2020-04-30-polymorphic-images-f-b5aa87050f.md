# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Google Vulnerability Rewards Program (VRP)
- **Bounty:** $6267.40
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Rendering, Image Processing Bypass, Polymorphic File Exploitation
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar allowed arbitrary image uploads from users and rendered location.hash parameters with XHR-fetched templates unescaped into the page. By crafting polymorphic JPEG images embedding XSS payloads in the Entropy-Coded Segment (ECS) that survived server-side image processing transformations, an attacker could achieve stored XSS attacks. The vulnerability chained user image upload functionality with unsafe DOM rendering practices.

## Attack scenario (step by step)
1. Attacker discovers Google Scholar accepts image uploads and serves them from the same origin
2. Attacker identifies the application renders location.hash parameters and XHR-fetched templates without proper escaping
3. Attacker crafts a polymorphic JPEG image with XSS payload embedded in the ECS section, engineered to survive the backend's image processing transformations
4. Attacker uploads the malicious image through Scholar's image upload functionality
5. Attacker creates a link with crafted location.hash parameter referencing the uploaded image as a template source
6. When victims click the link, the XSS payload embedded in the image survives processing and executes in their browser context

## Root cause
Two primary vulnerabilities combined: (1) Unsafe rendering of dynamically-fetched content via location.hash and XHR without HTML escaping, and (2) Insufficient validation that uploaded image files contain only valid image data, combined with predictable image processing transformations that don't completely strip all file content.

## Attacker mindset
The attacker demonstrated sophisticated understanding of image file formats, binary structures, and server-side image processing libraries. Rather than relying on standard XSS vectors, the attacker invested significant reverse-engineering effort to understand Google Scholar's image transformation pipeline and engineered payloads to survive those specific transformations. This reflects a methodical, research-oriented approach to discovering bypasses for security controls.

## Defensive takeaways
- Always HTML-escape dynamically rendered content, especially when loaded via XHR or from user-supplied parameters like location.hash
- Implement strict Content-Security-Policy headers to prevent inline script execution
- Validate uploaded files not just by extension/MIME type, but by deeply inspecting binary content and stripping all non-essential data
- Use image processing libraries with options to completely strip metadata and re-encode images from scratch rather than preserving original data
- Apply defense-in-depth: validate file format integrity, whitelist allowed content types, and sandbox user-uploaded content on separate origins/domains
- Regularly audit the actual capabilities and bypass vectors of image processing libraries used in production
- Never serve user-uploaded files from the same origin as your application JavaScript

## Variant hunting
['Test other image formats (PNG iDAT chunks, WebP metadata) for similar payload persistence through processing', 'Investigate whether SVG uploads allow embedded JavaScript or script references', 'Check if other file types accepted by Scholar (PDFs, documents) have similar polymorphic payload vulnerabilities', 'Look for similar unsafe template rendering patterns in other Google products that accept user uploads', 'Test whether other image processing backends (Vips, ImageMagick, GraphicsMagick) have consistent transformation behaviors or varying attack surfaces', "Examine if CSP bypass techniques using image-based payloads apply to other 'self' CSP configurations"]

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1059

## Notes
This vulnerability is particularly noteworthy for demonstrating the intersection of file format exploitation and web application security. The researcher's development of a standardized test suite for image processing libraries (doyensec/StandardizedImageProcessingTest) represents valuable contribution to the security community. The timeline shows Google VRP's initial skepticism about polymorphic image feasibility, requiring multiple PoCs before acceptance. The technique of embedding payloads in JPEG ECS sections that survive recompression is technically complex and represents advanced knowledge of image codec internals. The vulnerability also touches on a broader class of issues where user-uploaded content combined with unsafe rendering can be exploited through file format polymorphism.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
