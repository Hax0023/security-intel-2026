# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Google VRP (Vulnerability Reward Program)
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Rendering, Polymorphic Image Payload Encoding
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar's design pattern combined location.hash parameters with unescaped XHR-rendered template snippets, enabling XSS when users could upload images from the same origin. The researcher bypassed image processing defenses by embedding XSS payloads within JPEG entropy-coded segments using polymorphic image techniques, surviving backend transformations that stripped metadata and reprocessed images.

## Attack scenario (step by step)
1. Attacker identifies Google Scholar's unsafe rendering pattern using location.hash and unescaped template injection from XHR responses
2. Attacker discovers Scholar allows image uploads from the same origin as vulnerable endpoints
3. Attacker creates a polymorphic JPEG image with XSS payload embedded in the entropy-coded segment (ECS) section, carefully positioned to survive image reprocessing
4. Attacker uploads the malicious image through Scholar's image upload functionality
5. Attacker crafts a URL with location.hash parameters pointing to the uploaded image URI as a template source
6. When victim visits the URL, Scholar's unescaped template rendering extracts and executes the XSS payload from the polymorphic image

## Root cause
Combination of three weaknesses: (1) unsafe DOM rendering without output encoding of XHR-fetched template snippets, (2) same-origin upload functionality allowing attacker-controlled content, (3) insufficient validation of image file content after processing, permitting payload-bearing polymorphic images to remain intact through transformations

## Attacker mindset
Determined researcher systematically analyzing image processing libraries and their transformation behaviors to craft a payload that would persist through backend sanitization. Displayed persistence through iterative PoC refinement when initial approach failed, eventually discovering byte-level patterns that survived JPEG recompression.

## Defensive takeaways
- Always HTML-encode/escape dynamically rendered content regardless of perceived source trust, especially template snippets fetched via XHR
- Implement Content Security Policy (CSP) with strict script-src to prevent inline script execution even if XSS payloads reach the DOM
- When processing uploaded files, validate file integrity comprehensively beyond metadata stripping—verify binary structure and entropy patterns
- Use strict image format validation and re-encode images from scratch rather than relying on format-preserving transformations
- Segregate user-uploaded content to a separate origin/subdomain to prevent same-origin XSS exploitation
- Implement Defense-in-Depth: combine input validation, output encoding, CSP, and sandboxing rather than relying on single defenses

## Variant hunting
['Investigate PNG iDAT chunk payload embedding on platforms that preserve PNG-to-PNG conversions without resampling', 'Test SVG upload scenarios where polymorphic images could contain embedded SVG with XSS in xmlns or event handlers', 'Examine WebP format processing for similar ECS-like sections that might survive transformation', 'Research GIF frame injection techniques where payloads could be embedded in animation data segments', 'Test EXIF payload persistence on platforms with less aggressive metadata stripping (common CMS platforms)', "Investigate polymorphic images for CSP bypass when 'self' directive is used, embedding JavaScript disguised as image data"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS vulnerability in Scholar)
- T1059 - Command Line Interface (exiftool usage for payload insertion)
- T1566.002 - Phishing: Spearphishing Link (malicious Scholar URL with hash parameters)
- T1204.001 - User Execution: Malicious Link (victim clicks XSS-triggering URL)
- T1083 - File and Directory Discovery (reconnaissance of image processing behavior)
- T1036.005 - Masquerading: Match Legitimate Name or Location (polymorphic image appears as valid image file)

## Notes
This represents sophisticated vulnerability research requiring deep understanding of image format specifications and library behavior. The researcher demonstrated exceptional persistence when initial payloads failed, conducting methodical testing against multiple image processing backends (ImageMagick, GraphicsMagick, Libvips). The polymorphic image technique is generalizable to other web platforms with image uploads and template rendering. Google's initial skepticism about PoC feasibility suggests the attack surface may have been overlooked in other similar systems. The timeline shows VRP coordination challenges in convincing security teams of non-obvious exploitation paths.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
