# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Google Vulnerability Reward Program (VRP)
- **Bounty:** $6267.40
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe Template Rendering, Polymorphic File Upload
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar had an XSS vulnerability combining unsafe template rendering (unescaped XHR-fetched snippets via location.hash) with image upload functionality from the same origin. The researcher developed polymorphic image techniques to embed XSS payloads that survived Google's image processing transformations, bypassing the platform's security assumptions.

## Attack scenario (step by step)
1. Attacker discovers Google Scholar fetches and renders templates via location.hash parameters with unescaped XHR responses
2. Attacker identifies that Google Scholar accepts user image uploads from the same origin and serves them back
3. Attacker crafts a polymorphic JPEG image embedding XSS payload in the Entropy-Coded Segment (ECS) using byte patterns (0x00, 0x14) that survive image reprocessing
4. Attacker uploads the polymorphic image and obtains its URL served from Scholar's origin
5. Attacker crafts a malicious URL with location.hash pointing to the image, causing the template renderer to fetch and execute the embedded JavaScript
6. JavaScript payload executes in the context of Google Scholar, enabling session hijacking or account compromise

## Root cause
The vulnerability stems from three combined design flaws: (1) unsafe template rendering that doesn't escape XHR-fetched content, (2) user-controllable image uploads from the same origin, and (3) the false assumption that image processing transformations would strip all non-image content, failing to account for polymorphic image techniques that embed payloads in image format internals.

## Attacker mindset
Sophisticated attacker with deep knowledge of image file formats who recognizes that image processing libraries often preserve certain binary structures. Rather than accepting that image transformations would strip payloads, the attacker methodically researched file format specifications, tested multiple image libraries, and engineered payloads that survive JPEG recompression by embedding content in the ECS segment where byte sequences naturally persist.

## Defensive takeaways
- Always escape/sanitize content fetched dynamically, regardless of perceived source safety
- Never assume image processing will strip all potentially dangerous content; test transformations empirically
- Implement strict Content-Security-Policy headers to prevent inline script execution from user-controlled sources
- Validate and re-encode uploaded images using secure libraries with explicit format preservation settings
- Separate user-uploaded content from application origin using different domains/subdomains
- Implement additional validation on template content (JSON schema validation, allowlist patterns)
- Monitor image processing library behaviors and apply security patches immediately

## Variant hunting
['Test other image formats (PNG iDAT chunks, WebP) for similar polymorphic payload embedding in other web applications using image uploads with same-origin rendering', 'Investigate GIF frame data and animation segments for payload persistence through optimization', 'Examine SVG upload handling combined with unsafe rendering patterns, as SVG is technically an image format but supports XML/script content natively', 'Research TIFF, BMP, and other legacy formats for similar entropy segment manipulation techniques', 'Look for applications combining image upload with JSONP callbacks or other dangerous client-side template systems', "Hunt for CSP bypasses using polymorphic images with 'self' directives on platforms with image upload functionality"]

## MITRE ATT&CK
- T1190
- T1203
- T1567
- T1598
- T1566

## Notes
This research demonstrates sophisticated file format exploitation requiring deep technical knowledge. The researcher's development of a standardized image processing test suite (doyensec/StandardizedImageProcessingTest) is valuable for the security community. Google's initial skepticism about polymorphic image viability highlights how novel attack chains combining known vulnerabilities can bypass experienced reviewers' threat models. The technique has implications for CSP bypass and web shell concealment. Timeline shows typical VRP friction with initial PoC rejection, resolved after multiple submissions.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
