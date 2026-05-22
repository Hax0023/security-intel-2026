# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Google Vulnerability Reward Program (VRP)
- **Bounty:** $6267.40
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Unsafe Template Rendering, Image Processing Bypass
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar contained an XSS vulnerability combining unsafe template rendering with user-controlled image uploads. The application fetched and rendered templating snippets from relative URIs without escaping, which could be exploited through polymorphic images containing embedded XSS payloads that survived image processing transformations.

## Attack scenario (step by step)
1. Attacker identifies Google Scholar uses location.hash parameters and XHR to render unescaped templating snippets
2. Attacker discovers Scholar's image upload functionality processes and serves images from the same origin
3. Attacker crafts polymorphic JPEG images with XSS payload embedded in the Entropy-Coded Segment (ECS) using specific byte patterns (0x00 and 0x14 separators)
4. Attacker uploads the malicious image through Scholar's image upload feature
5. During image processing, payload survives transformations and re-sampling operations
6. When the uploaded image URL is referenced in a template rendered unescaped, the XSS payload executes in victim's browser

## Root cause
Two distinct security issues combined: (1) unsafe rendering of template snippets without HTML escaping based on location.hash and XHR-retrieved content, and (2) failure to properly sanitize or restrict image uploads when serving from the same origin. Image processing transformations were not sufficient to strip embedded payloads in the ECS segment of JPEG files.

## Attacker mindset
Sophisticated attacker with deep knowledge of image file formats and processing libraries. Recognized that image metadata stripping alone wouldn't work and pivoted to embedding payloads in compressed image data segments. Used trial-and-error methodology to understand byte-level patterns that survive specific image library transformations, demonstrating persistence through multiple PoC iterations.

## Defensive takeaways
- Never render user-supplied or uploaded content as unescaped HTML/templates, even if retrieved via XHR
- Implement strict Content Security Policy (CSP) to prevent inline script execution and restrict script sources
- Serve user-uploaded content from a separate origin/subdomain to prevent XSS from affecting the main application
- Thoroughly validate and test image processing libraries for payload survival across various file formats and transformations
- Strip all unnecessary data from images (metadata, extra segments) when processing uploads
- Use allowlists for acceptable template content rather than blacklists
- Properly escape all dynamic content when rendering, regardless of perceived safety

## Variant hunting
['Test other image formats (PNG iDAT chunks, WebP) for similar payload embedding techniques', 'Investigate whether concatenating payloads after image EOF markers survives other platform transformations', 'Search for similar unsafe template rendering patterns using location.hash + XHR in other Google services', 'Examine other web applications with image upload + same-origin serving to identify similar XSS chains', 'Test polymorphic image techniques against different image processing library versions', 'Look for CSP bypass via self-referencing image URLs containing script payloads']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link (delivery vector)
- T1566 - Phishing - Spearphishing Attachment (image upload)
- T1059 - Command and Scripting Interpreter - JavaScript

## Notes
This vulnerability required sophisticated understanding of image format internals and processing library behaviors. Google Scholar's VRP team initially dismissed the vulnerability as unexploitable until provided with a working PoC, suggesting image polymorphism as an evasion technique was underestimated. The researcher developed a comprehensive test suite (StandardizedImageProcessingTest on GitHub) documenting how different image libraries handle various payload embedding techniques, providing valuable reference material for future research.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
