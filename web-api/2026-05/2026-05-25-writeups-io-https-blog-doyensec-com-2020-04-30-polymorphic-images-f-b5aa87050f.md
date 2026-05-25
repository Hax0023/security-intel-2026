# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Google Vulnerability Rewards Program (VRP) - Google Scholar
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Insecure Direct Object References, Improper Input Validation, Unsafe Rendering of User-Supplied Content
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar allowed users to upload images and rendered content from the same origin without proper escaping, combined with insecure XHR-based template rendering via location.hash parameters. By crafting polymorphic images that survive image processing transformations while retaining embedded XSS payloads, an attacker could bypass initial security assumptions and achieve stored XSS.

## Attack scenario (step by step)
1. Attacker identifies that Google Scholar renders templating snippets fetched via XHR based on location.hash parameters without escaping output
2. Attacker discovers image upload functionality that serves images from the same origin
3. Attacker crafts a polymorphic JPEG image embedding JavaScript payload in the entropy-coded data segment (ECS), positioned to survive server-side image processing transformations
4. Attacker uploads the crafted image file to Google Scholar, bypassing basic image validation
5. When the image is processed by Scholar's backend and served, the embedded payload persists through transformations
6. Attacker crafts a location.hash parameter that references the uploaded image as a template, triggering XSS execution in victims' browsers

## Root cause
Multiple security flaws in combination: (1) unsafe rendering of templated content via XHR without proper escaping based on location.hash input, (2) image upload functionality serving content from the same origin without content-type enforcement, (3) insufficient understanding of image processing library behavior allowing payloads to persist through transformations, (4) lack of content validation beyond basic image format checks

## Attacker mindset
Methodical researcher recognizing that image processing libraries don't uniformly strip all data sections. Instead of accepting that polymorphic images with embedded payloads are impossible, the attacker conducted systematic testing across ImageMagick, GraphicsMagick, and Libvips. They reverse-engineered byte-level patterns that survive JPEG recompression by analyzing the entropy-coded segment structure and identifying preserved byte patterns (0x00 and 0x14 separators). This represents sophisticated understanding that security through obscurity or transformation is not reliable.

## Defensive takeaways
- Never render user-controlled or user-supplied content without proper output encoding, regardless of retrieval mechanism (XHR, templates, etc.)
- Implement strict Content-Security-Policy headers, especially 'script-src' to prevent inline execution even if XSS payloads are injected
- Serve user-uploaded content from a separate domain/origin to prevent same-origin XSS exploitation
- Enforce strict Content-Type headers on all served content; do not rely on file extension validation
- Implement comprehensive image re-encoding (not just resampling) that completely reconstructs the image to eliminate extraneous data
- Do not trust that image processing libraries will strip all metadata and payloads by default; validate behavior empirically
- Use allowlist-based template and parameter validation rather than relying on location.hash processing
- Implement defense-in-depth: multiple layers of validation, encoding, and isolation should all fail safely

## Variant hunting
Search for similar patterns in other Google properties and web applications that: (1) allow image uploads and serve from same origin, (2) use XHR-based templating with hash parameter control, (3) process images but don't fully re-encode them, (4) lack output encoding on dynamically rendered content. Test other image formats (GIF, WebP, TIFF) for polymorphic payload insertion. Investigate whether other image processing backends preserve EXIF data, PNG iDAT chunks, or have similar byte-pattern preservation in recompression.

## MITRE ATT&CK
- T1190
- T1059.007
- T1204.001
- T1566.002

## Notes
The researcher's methodical approach of building a standardized image processing test suite (doyensec/StandardizedImageProcessingTest) demonstrates best practice for vulnerability research. The extended timeline (30+ days) reflects Google's initial skepticism about polymorphic image feasibility, highlighting the importance of PoC delivery in VRP programs. The vulnerability demonstrates that combining multiple weak controls (unsafe rendering + same-origin uploads + incomplete image processing) creates exploitable conditions. The discovery that specific byte patterns (0x00, 0x14) survive JPEG recompression suggests deep knowledge of the JPEG standard and image library internals.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
