# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Google Vulnerability Reward Program
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Unsafe Template Rendering, Image Processing Bypass
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar rendered templating snippets retrieved via XHR and location.hash parameters without proper escaping, combined with image upload functionality that served user content from the same origin. An attacker could craft polymorphic images embedding XSS payloads in various image structures (EXIF metadata, ECS segments, PNG iDAT chunks) that survived server-side image transformations to achieve arbitrary JavaScript execution.

## Attack scenario (step by step)
1. Attacker crafts a polymorphic JPEG image embedding JavaScript payload in the entropy-coded data segment (ECS) using specific byte patterns (0x00 and 0x14 separators)
2. Attacker uploads the image via Google Scholar's image upload functionality
3. Server processes the image through resampling/re-encoding but payload bytes in ECS section survive transformation due to specific byte sequence placement
4. Attacker accesses Scholar pages that render templating snippets via location.hash parameters without HTML escaping
5. Attacker crafts malicious URL with hash parameters pointing to the uploaded polymorphic image URI
6. When page renders unescaped content, embedded XSS payload from image executes in victim's browser with same-origin privileges

## Root cause
Three compounding issues: (1) unsafe rendering of templating content retrieved via XHR without HTML escaping, (2) same-origin serving of user-uploaded image content, and (3) incomplete image processing that failed to strip all payload vectors from image files during transformations

## Attacker mindset
Researcher bypassed initial skepticism from Google security team by demonstrating that polymorphic images could survive aggressive image processing pipelines through careful engineering of payload placement within image data structures. Persistence through multiple PoC iterations revealed the necessity of understanding both web application architecture and low-level image format specifications.

## Defensive takeaways
- Always HTML-escape templating content rendered from any source, regardless of supposed safety mechanisms
- Serve user-uploaded content from a separate origin/domain to prevent same-origin XSS exploitation
- Implement comprehensive image sanitization beyond basic format validation - strip all optional data segments (EXIF, ICC profiles, XMP)
- Re-encode images through multiple format conversions and validation cycles to eliminate embedded payloads
- Apply strict Content Security Policy headers to limit inline script execution
- Test image processing libraries against adversarial inputs as part of security validation
- Consider sandboxing or size restrictions on image metadata
- Implement integrity verification on served user content

## Variant hunting
['Test other image formats (GIF, WebP, AVIF, TIFF) for payload embedding opportunities in their respective data structures', 'Investigate vector image formats (SVG) when user-uploaded content serves from same origin', 'Examine audio file upload handling for similar template injection + metadata payload vectors', 'Research PDF upload functionality for embedded JavaScript payloads surviving processing', 'Test document format uploads (DOCX, XLSX) for macro/embedded content exploitation', 'Probe video thumbnail generation pipelines for frame injection techniques']

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002

## Notes
This research demonstrates sophisticated understanding of image processing internals. Key insight: image libraries prioritize format compliance over security, preserving data structures that don't affect visual output. The trial-and-error byte sequence discovery (0x00, 0x14 patterns) shows deep reverse-engineering effort. Google's initial dismissal highlights gap between security team assumptions and determined researcher capabilities. Doyensec's public StandardizedImageProcessingTest suite enables security community to validate similar issues across platforms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
