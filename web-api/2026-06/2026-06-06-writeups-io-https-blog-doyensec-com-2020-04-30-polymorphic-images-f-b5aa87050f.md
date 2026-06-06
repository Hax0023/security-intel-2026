# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Google VRP (Vulnerability Rewards Program)
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Arbitrary File Upload, Improper Input Validation, Unescaped Template Rendering
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar had an XSS vulnerability stemming from unescaped template rendering combined with user image uploads from the same origin. The researcher discovered that polymorphic images could carry XSS payloads that survived Google's image processing backend by embedding JavaScript in JPEG entropy-coded segments (ECS), bypassing security transformations.

## Attack scenario (step by step)
1. Attacker identifies Google Scholar's design pattern using location.hash parameters and unescaped XHR-rendered templates
2. Attacker crafts a polymorphic JPEG image with XSS payload embedded in the ECS (entropy-coded segment) section
3. Attacker positions payload bytes using specific patterns (0x00 and 0x14 separators) to survive image transformations
4. Attacker uploads the polymorphic image via Scholar's image upload functionality
5. When the image is served from the same origin, attacker injects location.hash parameter to load image URL as template
6. XSS payload executes in victim's browser within Scholar's origin context

## Root cause
Combination of three security failures: (1) Unescaped template rendering from user-controlled XHR sources, (2) Insufficient image processing that doesn't completely sanitize all image segments, (3) Serving user-uploaded content from the same origin without proper isolation

## Attacker mindset
This is sophisticated polyglot exploitation research. The attacker demonstrates deep knowledge of image file formats, binary structures, and Huffman compression to create files that are simultaneously valid images and XSS vectors. They systematically tested multiple image processing libraries to find weaknesses, showing persistence after initial rejection and willingness to develop novel exploitation techniques.

## Defensive takeaways
- Always escape/encode template content, regardless of source; never render unescaped HTML from XHR responses
- Serve user-uploaded content from a separate origin/domain (CDN with different domain) to prevent same-origin XSS
- Implement strict CSP policies with 'script-src' that doesn't allow 'unsafe-inline' or data URIs
- Use sandboxed iframes with restrictive attributes when rendering user content
- Validate and sanitize all image metadata (EXIF, comments) and verify no data exists after expected file endings
- Use security-focused image processing libraries and keep them updated
- Implement defense-in-depth: validate file magic bytes, re-encode images completely, strip all metadata
- Test image processing pipelines against polyglot file attacks specifically

## Variant hunting
Search for similar issues in platforms with: image upload + same-origin content serving + template rendering from user input. Potential variants: SVG uploads with embedded scripts, PDF uploads with JavaScript, other document formats with metadata fields. Test image processing in popular platforms (Imgur, Pinterest, Flickr, social media). Investigate whether other image segments (PNG iDAT, APNG frames) can carry payloads across different platforms.

## MITRE ATT&CK
- T1190
- T1434
- T1523
- T1598
- T1204

## Notes
The researcher's systematic approach of testing multiple image libraries and developing a test suite (StandardizedImageProcessingTest) demonstrates mature vulnerability research methodology. The ECS technique required precise understanding of JPEG Huffman coding and trial-and-error to find byte patterns that survive transformation. Google's initial skepticism about polymorphic image feasibility highlights how novel polyglot attacks can evade assumptions of security teams. The 6+ week timeline and multiple PoC iterations show typical VRP friction for novel exploitation techniques.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
