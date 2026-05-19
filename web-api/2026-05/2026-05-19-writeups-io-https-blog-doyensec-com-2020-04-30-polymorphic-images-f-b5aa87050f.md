# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Google Vulnerability Reward Program (VRP) - Google Scholar
- **Bounty:** $6267.40
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Arbitrary File Upload, Polymorphic Payload Delivery, Unsafe DOM Rendering
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar featured a design pattern that fetched and rendered templating snippets from relative URIs unescaped into the DOM. Combined with Google Scholar's image upload functionality serving from the same origin, an attacker could upload polymorphic images containing XSS payloads that survived server-side image processing transformations, achieving code execution.

## Attack scenario (step by step)
1. Attacker identifies that Google Scholar renders content from location.hash and XHR-fetched templates unescaped into the page
2. Attacker discovers that Google Scholar allows image uploads serving from the same origin, making them eligible for same-origin XSS
3. Attacker crafts a polymorphic image containing JavaScript payload embedded in JPG's Entropy-Coded Segment (ECS) that survives image transformation
4. Attacker uploads the crafted image to Google Scholar's image upload endpoint
5. Server processes the image through transformation pipeline but payload bytes survive in the ECS section
6. Attacker triggers XSS by referencing the uploaded image URL in a crafted location.hash parameter, causing unescaped rendering of the payload

## Root cause
Combination of three security failures: (1) unsafe DOM rendering of templating snippets retrieved via XHR without HTML escaping, (2) same-origin file upload functionality, and (3) insufficient image processing that failed to completely strip or sanitize all image data segments containing potentially executable content

## Attacker mindset
Sophisticated researcher demonstrating that security assumptions about image file safety are flawed. Attacker understood image format specifications deeply, analyzed server-side image processing behavior through systematic testing, and developed novel polymorphic techniques to bypass additional security measures (image transformation, metadata stripping). Showed persistence in iterating PoCs when initial bypass attempts failed.

## Defensive takeaways
- Always HTML-escape user-controlled content before inserting into DOM, regardless of apparent source (even fetched templates)
- Serve user uploads from a completely different origin/domain to prevent same-origin XSS exploitation
- Implement strict image processing: convert to canonical format, validate using dedicated parsers, and strip all non-essential data segments
- Apply Content Security Policy (CSP) with restrictive directives to prevent inline script execution
- Test image processing libraries against adversarial inputs; understand that library defaults may not remove all metadata
- Validate file content (magic bytes) independent of extension; reprocess images through standard libraries in strict mode
- Use allowlist-based approach for which image data segments/metadata to preserve

## Variant hunting
['Investigate other platforms allowing image uploads and rendering unescaped content from same origin', 'Test alternative polymorphic image techniques: PNG iDAT chunk manipulation, WEBP payloads, SVG polyglots stored as images', 'Examine other image format specifications (BMP, GIF, TIFF) for similar ECS-like segments that survive transformation', 'Research whether other Google products have similar XHR-based template rendering patterns', "Test whether polymorphic images can bypass CSP 'self' directives when served as images but interpreted as scripts", 'Investigate if image metadata (EXIF, IPTC, XMP) persists in other web platforms and can be used for payload delivery']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1059 - Command and Scripting Interpreter
- T1567 - Exfiltration Over Web Service
- T1204 - User Execution

## Notes
This research demonstrates that image file formats are more complex and less sanitizable than commonly assumed. The attacker had to understand: JPEG JFIF structure and ECS segments, PNG iDAT chunks, image library behavior across ImageMagick/GraphicsMagick/Libvips, and the specific transformation pipeline used by Google Scholar. The polymorphic image technique is particularly dangerous because it defeats file-based security assumptions and CSP policies. The researcher published their test suite and PoC images on GitHub, advancing the field's understanding of this attack vector.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
