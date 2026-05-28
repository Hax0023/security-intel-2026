# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Google VRP
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Unvalidated Redirect/Template Injection, Image Upload Vulnerability
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar rendered user-controlled templating snippets from location.hash parameters and XHR requests without escaping, combined with image upload functionality serving from the same origin. An attacker could craft polymorphic images containing embedded XSS payloads that survive image processing transformations, bypassing security controls to execute arbitrary JavaScript.

## Attack scenario (step by step)
1. Attacker identifies that Google Scholar renders templates from XHR-fetched content without proper escaping
2. Attacker discovers Scholar's image upload functionality serves images from the same origin
3. Attacker crafts a polymorphic image embedding JavaScript payload in the JPEG ECS (entropy-coded data segment) at specific byte offsets
4. Attacker uploads the crafted image, which bypasses image processing transformations that strip metadata and reprocess the image
5. Attacker references the uploaded image via location.hash parameter to trigger template rendering
6. JavaScript payload executes in the victim's browser context within Scholar's origin

## Root cause
Combination of three flaws: (1) unsafe template rendering from user-controlled hash parameters without output encoding, (2) image upload from same origin without content validation, (3) insufficient image processing that fails to completely sanitize embedded content while preserving exploitable data segments

## Attacker mindset
Sophisticated researcher bypassing the assumption that image processing transformations would sanitize payloads. Methodical approach: reverse-engineered image format specifications, tested multiple polymorphic techniques, identified specific byte patterns (0x00 and 0x14 separators) that survive transformation, and crafted images resistant to JPEG re-encoding while maintaining valid image display.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) with no 'unsafe-inline' and restrict script-src to prevent XSS regardless of template injection vectors
- Always escape/encode templating output, especially content derived from user-controlled parameters like location.hash
- Serve user-uploaded content from a separate, unprivileged origin (sandbox domain) isolated from application logic
- Implement comprehensive image validation: verify file magic bytes, strip all metadata, validate against expected image dimensions/format, perform binary comparison against known templates
- Use allowlist-based image processing libraries with explicit unsafe-content rejection rather than relying on transformation to sanitize
- Treat image uploads as potentially malicious binary content—re-encode/re-compress images completely rather than passing through transformations
- Audit all XHR/AJAX endpoints for unsafe rendering patterns, especially those combined with user-controlled parameters

## Variant hunting
['Investigate other image formats (GIF, WebP, BMP, TIFF) for similar polyglot payload injection in data segments', 'Test SVG upload endpoints which inherently support XML/JavaScript and may bypass image-specific protections', 'Examine PDF upload functionality combined with template injection for similar exploitation chains', 'Search for other endpoints using location.hash or similar user-controlled parameters for dynamic content loading without escaping', 'Review other Google services for unsafe template rendering patterns when combined with file upload capabilities', "Test polyglot image+script payloads against CSP policies claiming 'self' directive as mentioned in writeup", 'Investigate whether archived/cached versions of uploaded images retain payload integrity']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1204.001 - User Execution: Malicious Link
- T1567.002 - Exfiltration Over Web Service: Exfiltration to Cloud Storage

## Notes
The vulnerability required sophisticated understanding of image format internals and image library behavior. Key innovation was discovering the specific byte pattern (0x00 0x14 separators) in JPEG ECS that survives Google's transformation pipeline. The researcher developed a comprehensive test suite (StandardizedImageProcessingTest on Github) validating behavior across ImageMagick, GraphicsMagick, and Libvips. Google's initial skepticism about polymorphic image feasibility delayed remediation but highlights the importance of proof-of-concept research. Two separate endpoints were affected. The technique could theoretically bypass 'self' CSP directives as content is served from same origin.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
