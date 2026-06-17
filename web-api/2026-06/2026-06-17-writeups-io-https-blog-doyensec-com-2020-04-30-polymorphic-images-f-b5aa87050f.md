# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Google VRP
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe Template Rendering, Insufficient Input Validation, Polymorphic File Exploitation
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar rendered templating snippets retrieved via XHR unescaped on the page, combined with user image upload functionality on the same origin, allowing XSS exploitation. The researcher crafted polymorphic images that survived Google's image processing transformations (metadata stripping, resampling) by embedding payloads in JPEG entropy-coded segments and EXIF metadata, bypassing initial skepticism from Google's security team.

## Attack scenario (step by step)
1. Attacker identifies that Google Scholar uses location.hash parameters and XHR to fetch and render templating snippets unescaped
2. Attacker discovers Google Scholar's image upload functionality accepts user-supplied images on the same origin
3. Attacker embeds XSS payload in image file using multiple polymorphic techniques (EXIF metadata, JPEG ECS section, PNG iDAT chunks)
4. Image processing backend applies transformations (metadata stripping, resampling, quality conversion) but payload survives in specific byte sequences
5. Attacker uploads the polymorphic image and crafts URL with location.hash parameter pointing to the image URI
6. Browser renders unescaped XSS payload from the polymorphic image, executing malicious JavaScript in Scholar's origin context

## Root cause
Two separate vulnerabilities combined: (1) Unsafe rendering of template content retrieved via XHR without HTML escaping based on untrusted location.hash parameters, and (2) insufficient validation that user-uploaded images are actually valid image files, allowing polymorphic files containing executable code to persist through image processing transformations.

## Attacker mindset
Sophisticated adversary researching image file format internals and image processing library behaviors to craft files that maintain hidden payloads through transformations. Demonstrates deep understanding of JPEG/PNG specifications, Huffman compression, and image processing edge cases. Persistence in overcoming platform skepticism by providing multiple proof-of-concept iterations.

## Defensive takeaways
- Always HTML-escape/sanitize content retrieved dynamically, regardless of expected format or source
- Do not trust location.hash or other user-controllable parameters to dictate code execution paths
- Implement strict Content Security Policy (CSP) with 'unsafe-inline' avoided and script-src restrictions
- Validate uploaded files using magic bytes/file signatures, not just extensions; re-encode images to eliminate extraneous data
- Use image libraries with robust file format validation; consider sandboxing image processing operations
- Test image processing pipelines for polymorphic file resilience across multiple libraries (ImageMagick, Libvips, etc.)
- Serve user-generated content from a separate, sandboxed origin to prevent same-origin XSS attacks
- Implement integrity checks and canonicalization of image files before serving

## Variant hunting
['Test other file formats supporting metadata or content appending (GIF89a, WEBP, TIFF, BMP) for similar polymorph techniques', 'Investigate image processing libraries beyond ImageMagick/GraphicsMagick for edge cases in format handling', "Explore CSS polyglots combined with image uploads to bypass CSP 'self' directives", 'Research polymorph techniques in other binary formats (PDF, SVG, ZIP) served from user-upload endpoints', 'Test behavior of image lazy-loading, picture elements, and srcset attributes with polymorphic payloads', 'Examine cloud image processing services (Cloudinary, Imgix) for similar transformation bypass methods', 'Investigate JavaScript injection in image alternative text, title attributes, and IPTC keyword fields']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1105

## Notes
This research represents advanced exploitation of file format polymorphism in the context of web security. The researcher's systematic approach—testing multiple image libraries and creating a test suite—establishes this as a reproducible technique category rather than isolated bug. Google's initial skepticism highlights the importance of persistence and thorough PoC submission in vulnerability disclosure. The technique can also conceal web shells or bypass 'self' CSP directives, indicating broader applicability beyond Scholar. The use of specific byte sequences (0x00, 0x14) to preserve payload through JPEG reprocessing demonstrates deep reverse-engineering effort. Published research and GitHub test suite provide valuable reference for future image polymorph research.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
