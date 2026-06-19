# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Google Vulnerability Reward Program (VRP)
- **Bounty:** $6267.40
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Rendering, Image Upload Vulnerability, Polymorphic File Attack
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar rendered XHR-fetched templating snippets unescaped into the DOM using location.hash parameters, combined with user image upload functionality from the same origin. An attacker could craft polymorphic JPEG images embedding XSS payloads in the entropy-coded data segment (ECS) that survived server-side image transformations to achieve arbitrary script execution.

## Attack scenario (step by step)
1. Attacker discovers Google Scholar uses location.hash and XHR to fetch and render templating snippets unescaped
2. Attacker uploads a malicious image file containing XSS payload embedded in JPEG's ECS section with specific byte sequences (0x00 and 0x14 patterns)
3. Server processes the image (resizing, re-sampling, metadata stripping) but payload survives in ECS due to specific encoding patterns
4. Image is served from same origin as Scholar application, accessible via same-origin policy
5. Attacker crafts URL with location.hash referencing the uploaded image as a template source
6. Victim clicks malicious link; XSS payload executes in Scholar's origin context

## Root cause
Combination of unsafe DOM manipulation (unescaped XHR content rendering) and insufficient validation of user-uploaded content. Image processing transformations did not fully sanitize payload-carrying data in JPEG entropy-coded segments, allowing specially crafted polymorphic images to bypass security checks.

## Attacker mindset
Sophisticated researcher demonstrating that client-side controls combined with image processing quirks create exploitable attack surface. Focus on polymorph techniques to bypass server-side defenses and understanding of image format internals to hide payloads in ways that survive transformation pipelines.

## Defensive takeaways
- Always escape/sanitize content before inserting into DOM, regardless of source or retrieval method
- Validate and re-encode all user-uploaded files; do not assume transformations fully sanitize content
- Implement strict Content Security Policy (CSP) with non-self sources, avoiding unsafe-inline and unsafe-eval
- Use dedicated secure image processing libraries with known-safe behavior; test against adversarial inputs
- Serve user uploads from separate origin/domain to prevent same-origin XSS exploitation
- Implement file type validation beyond magic bytes; verify integrity after processing
- Apply defense-in-depth: combine multiple validation layers (format validation, sanitization, CSP, origin separation)

## Variant hunting
['Test other file formats (PNG iDAT chunks, GIF data sections) for similar polymorphic payload survival', 'Investigate SVG uploads with embedded JavaScript, especially with data: URIs or event handlers', 'Analyze PDF/PostScript upload features for similar payload-embedding techniques in ECS equivalents', 'Test WebP, AVIF, and newer image formats for similar entropy-coded segment vulnerabilities', 'Research polymorphic attacks in video processing (MP4, WebM) for web players', 'Examine image gallery/preview features that might render uploaded images without proper isolation', "Test CSP 'self' bypass via polymorphic assets on platforms using unsafe content rendering patterns"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link
- T1566 - Phishing - Phishing with Attachment/Content
- T1204 - User Execution - Malicious Link
- T1204.001 - User Execution - Malicious Link - User Clicks Link

## Notes
This is a sophisticated attack requiring deep knowledge of image format internals and server-side image processing libraries. The researcher's approach of creating a StandardizedImageProcessingTest suite is exemplary for discovering edge cases in security-critical libraries. The timeline shows Google's VRP initially required PoC before recognizing the polymorphic image technique's validity. Technique can also conceal web shells and bypass CSP 'self' directives. Related research available at doyensec/StandardizedImageProcessingTest GitHub repository.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
