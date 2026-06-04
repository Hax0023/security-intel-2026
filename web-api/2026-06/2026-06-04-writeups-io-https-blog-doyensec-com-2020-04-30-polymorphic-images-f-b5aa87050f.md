# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Google Vulnerability Reward Program (VRP)
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Unescaped Template Rendering, Arbitrary File Upload, Polymorphic File Attack
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar contained an XSS vulnerability combining unescaped template rendering via location.hash parameters with user-controlled image uploads. The researchers bypassed image processing defenses by crafting polymorphic JPEG images that preserved XSS payloads in the entropy-coded data segment (ECS), surviving server-side image transformations.

## Attack scenario (step by step)
1. Attacker identifies Google Scholar fetches templating snippets via XHR using location.hash parameters and renders them unescaped
2. Attacker uploads a specially crafted polymorphic JPEG image containing XSS payload embedded in the ECS (entropy-coded data segment)
3. Image processing backend applies transformations (metadata stripping, reprocessing) but payload survives due to positioning at variable offset with 0x00 and 0x14 byte patterns
4. Attacker crafts payload using onclick/mouseover events that survive user agent parsing with low-value bytes
5. Attacker references the uploaded image URL in location.hash parameter to trigger template rendering with XSS payload
6. Victim visits malicious link, XSS executes in Scholar context with attacker's privileges

## Root cause
Combination of three design flaws: (1) unescaped rendering of dynamically loaded templates via location.hash and XHR, (2) permissive image upload functionality from same origin, (3) insufficient validation that image processing libraries completely sanitize embedded data in image format structures like JPEG ECS segments

## Attacker mindset
Persistence and deep technical understanding of image file formats. When initial EXIF-based payloads failed, researcher methodically tested alternative techniques (PNG iDAT, JPEG ECS), reverse-engineered image transformation behavior through trial-and-error, and developed a test suite to understand library-specific quirks. Demonstrated that 'trivial' XSS requires sophisticated polymorphic image engineering.

## Defensive takeaways
- Always HTML-escape or use safe templating engines for dynamically rendered content, regardless of source (including location.hash)
- Avoid serving user-uploaded content from the same origin as application logic; use dedicated CDN or separate domain
- Implement strict Content Security Policy (CSP) with 'unsafe-inline' disabled and script-src restricting to trusted sources
- Re-validate and re-process uploaded files server-side; use standardized libraries and verify format integrity post-processing
- Understand that image format structures (EXIF, ECS, PNG chunks) can persist through transformations; sanitize or strip all non-essential data
- Monitor image processing library behavior through automated test suites when changes to dependencies occur
- Apply defense-in-depth: even if image upload succeeds, the unescaped template rendering should have been prevented

## Variant hunting
['Search for other web platforms combining user image uploads with same-origin template rendering', 'Test image upload endpoints on platforms supporting dynamic content generation (wikis, galleries, document management systems)', 'Audit implementations of ImageMagick, GraphicsMagick, and Libvips integration for post-processing validation gaps', 'Investigate GIF/WebP/AVIF format structures for similar payload smuggling opportunities in lesser-known chunks', "Test if polymorphic images can bypass 'self' CSP directives by embedding JavaScript in recoverable segments", 'Examine whether web shells can be similarly embedded in image ECS segments for persistent compromise']

## MITRE ATT&CK
- T1190
- T1071
- T1566
- T1204
- T1059

## Notes
This research demonstrates a sophisticated multi-stage attack requiring deep knowledge of image formats and library behaviors. Google's initial skepticism about polymorphic image XSS feasibility highlights the need for security teams to validate extraordinary claims with PoC. The public disclosure of this technique and the test suite (doyensec/StandardizedImageProcessingTest on GitHub) provides valuable security research infrastructure. The technique's applicability to concealing web shells or bypassing 'self' CSP directives extends its impact beyond XSS.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
