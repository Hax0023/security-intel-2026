# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Google Vulnerability Reward Program (VRP)
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Unvalidated Redirect, Improper Input Validation, Unsafe Deserialization of User Input
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar contained an XSS vulnerability where user-uploaded images could be crafted to contain malicious JavaScript payloads that survive image processing transformations. The application rendered user-controlled content from image uploads unescaped via location.hash parameters and XHR requests. Attackers could exploit this by embedding payloads in various image segments (EXIF metadata, PNG iDAT chunks, or JPG entropy-coded data) that would persist through backend image processing.

## Attack scenario (step by step)
1. Attacker identifies that Google Scholar fetches and renders templating snippets from relative URIs using location.hash parameters without proper escaping
2. Attacker discovers that Scholar's image upload functionality allows arbitrary file uploads served from the same origin, enabling same-origin payload delivery
3. Attacker crafts a polymorphic image by embedding XSS payload in JPG's entropy-coded segment (ECS) or other image metadata sections
4. Attacker uploads the malicious image through Scholar's image upload feature
5. Backend image processing applies transformations but fails to strip the payload from certain image segments
6. Attacker references the uploaded image URL in location.hash parameters, triggering unescaped rendering of the embedded XSS payload

## Root cause
Multiple security failures: (1) Unsafe rendering of content retrieved via XHR without proper HTML escaping, (2) User-controlled content served from same origin without CSP protection, (3) Image processing library transformations did not adequately sanitize all image segments containing executable content, (4) Lack of input validation on image upload and content-type enforcement

## Attacker mindset
Sophisticated attacker with deep knowledge of image file formats and processing libraries. Researcher-oriented approach: when initial EXIF-based payloads failed, systematically tested alternative image segments (iDAT chunks, ECS sections) to find techniques surviving backend transformations. Persistence through multiple PoC iterations shows determination to prove conceptual vulnerability despite initial skepticism from vendor.

## Defensive takeaways
- Always HTML-escape user-controlled content regardless of source, especially content retrieved dynamically via XHR
- Implement strict Content Security Policy (CSP) with 'unsafe-inline' disabled to mitigate XSS from all vectors
- Apply comprehensive input validation and sanitization to uploaded files, not just filename/extension checks
- Understand image file format structure and ensure image processing libraries fully strip executable content from all segments (metadata, chunks, entropy data)
- Serve user-uploaded content from isolated domain (different origin) separate from main application
- Use allowlist-based image processing: recompress images to canonical format, strip all metadata, validate pixel data integrity
- Regularly test image processing pipelines against polyglot/polymorphic payloads
- Apply defense-in-depth: combine multiple controls (CSP, escaping, isolation, format validation)

## Variant hunting
Look for similar patterns in platforms with: (1) user image uploads served from same origin, (2) dynamic content rendering via hash/XHR without escaping, (3) image processing that doesn't fully sanitize all format-specific segments, (4) other document upload features (PDF, SVG, TIFF) that might embed scripts, (5) platforms using vulnerable versions of Imagemagick/GraphicsMagick/Libvips without security patches for polyglot handling

## MITRE ATT&CK
- T1190
- T1566.001
- T1059.007

## Notes
This research demonstrates sophisticated polyglot file creation techniques. The researcher created a test suite (doyensec/StandardizedImageProcessingTest) for evaluating image library behavior. Key insight: JPG entropy-coded segment (ECS) survivability depends on separating payload with 0x00 and 0x14 byte patterns. This technique can also conceal webshells to bypass 'self' CSP directives. Timeline shows vendor initially requested PoC due to skepticism about payload survival through transformations—persistence and technical proof was necessary for validation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
