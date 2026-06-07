# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Google Vulnerability Reward Program (VRP)
- **Bounty:** $6,267.40
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Arbitrary File Upload, Unescaped Template Rendering, Polymorphic File Bypass
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar contained an XSS vulnerability where location.hash parameters and XHR requests rendered templating snippets unescaped on the page. By uploading polymorphic images containing XSS payloads embedded in JPEG entropy-coded segments (ECS), attackers could bypass image processing transformations to execute arbitrary JavaScript. The vulnerability leveraged the platform's image upload functionality combined with insufficient output encoding.

## Attack scenario (step by step)
1. Attacker identifies that Google Scholar renders templates from XHR requests without proper escaping based on location.hash parameters
2. Attacker discovers Google Scholar hosts user-uploaded images from the same origin, allowing same-origin XSS
3. Attacker crafts a polymorphic JPEG image with XSS payload embedded in the entropy-coded segment (ECS), designed to survive Google's image processing transformations
4. Attacker uploads the crafted image to Google Scholar through the image upload functionality
5. When the image is processed by the server, the payload survives the transformation and is served back to users
6. Attacker delivers a link with location.hash parameters that causes the unescaped template rendering to execute the XSS payload from the image URI

## Root cause
Multiple security weaknesses converged: (1) Unescaped rendering of XHR-fetched templates based on user-controllable location.hash, (2) User-controlled image upload functionality with insufficient validation, (3) Images served from same origin as main application, (4) Image processing backend failed to completely sanitize embedded content in JPEG entropy-coded segments despite metadata stripping

## Attacker mindset
Determined researcher who recognized that Google's initial rejection of the vulnerability was based on incorrect assumptions about polymorphic image feasibility. Methodically researched historical polymorphic image techniques, tested multiple image processing libraries (ImageMagick, GraphicsMagick, Libvips), and iteratively crafted payload positioning through trial-and-error to survive specific server-side transformations. Persistence through multiple PoC iterations despite VRP skepticism demonstrated deep technical understanding.

## Defensive takeaways
- Always HTML-escape/encode output from templating engines regardless of source, especially when rendered from user-controllable parameters like location.hash
- Never serve user-uploaded content from the same origin as main application; use separate domain/CDN with restrictive Content-Type headers
- Implement strict CSP policies (script-src 'self' does not prevent same-origin data exfiltration) and consider script-src 'none' for upload domains
- Image processing should strip not just metadata but also verify file integrity and reject images with appended content after file format terminators (0xFFD9 for JPG, IEND for PNG)
- Validate that image processing library output matches expected dimensions/format and has not been modified during re-encoding
- Test image upload security with polymorphic file payloads, not just standard format validation
- Implement Content-Security-Policy headers with proper directives to prevent script execution from image sources
- Consider re-encoding images to fresh files rather than in-place transformations to eliminate partial content preservation

## Variant hunting
['Search for applications combining: user image uploads + same-origin serving + template rendering from XHR/hash parameters', 'Test image processing pipelines for content preservation in PNG iDAT chunks, APNG animation frames, WebP VP8 bitstream', 'Investigate GIF comment sections and application extensions (App Ext) for payload survival through processing', 'Examine SVG upload handling combined with object/embed tag injection and JavaScript event handlers', 'Test TIFF file structure for payload embedding in IFD (Image File Directory) or embedded preview images', 'Look for EXIF preservation in specific image libraries (PIL/Pillow, ImageSharp, ImageResizer)', 'Test for ZIP-based formats (DOCX, XLSX, ODT) with embedded media where polymorphic payloads could hide', 'Investigate concurrent upload + serving race conditions where original file served before processing completes']

## MITRE ATT&CK
- T1190
- T1566.002
- T1203
- T1059.007

## Notes
This vulnerability demonstrates the importance of defense-in-depth: a single weakness (unescaped output OR user uploads OR same-origin serving) would be manageable, but the combination created a critical issue. The polymorphic image technique is not new but required significant expertise to apply in this specific context. Google's initial skepticism about polymorphic image viability highlights how security teams may underestimate novel attack chains. The researcher's publication of test suite and image examples on GitHub (doyensec/StandardizedImageProcessingTest) provides valuable resource for future image-based security research. Report timeline shows 6 weeks from initial report to reward, with 2 PoC iterations required.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
