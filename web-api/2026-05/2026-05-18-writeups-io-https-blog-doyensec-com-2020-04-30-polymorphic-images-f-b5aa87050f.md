# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Google Vulnerability Reward Program (VRP)
- **Bounty:** $6267.40
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Arbitrary File Upload, Improper Input Validation, Unsafe Template Rendering
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar's web application rendered user-supplied templating snippets unescaped via location.hash parameters and XHR, combined with an image upload feature that served content from the same origin. The researcher discovered that polymorphic images—crafted to survive image processing transformations—could deliver XSS payloads through manipulated JPEG entropy-coded data segments (ECS), bypassing backend image sanitization.

## Attack scenario (step by step)
1. Attacker crafts a polymorphic JPEG image embedding an XSS payload in the entropy-coded data (ECS) segment at the beginning of the section, separated by specific byte patterns (0x00 and 0x14)
2. Attacker uploads the malicious image via Google Scholar's image upload functionality
3. Google Scholar's image processing backend applies transformations (metadata stripping, resampling) which preserve the carefully positioned payload bytes in the ECS section
4. Attacker uses location.hash parameters to specify a relative URI pointing to the uploaded image
5. Scholar's XHR mechanism fetches and renders the image content unescaped as templating snippets on the page
6. Browser executes the XSS payload (onclick/mouseover events), allowing session hijacking, credential theft, or further compromise

## Root cause
Combination of three weaknesses: (1) unescaped rendering of dynamically loaded templates via XHR, (2) same-origin image upload and serving, and (3) insufficient validation that uploaded images cannot contain executable content after processing. Image libraries' preservation of certain JPEG structures (particularly ECS segments) during transformation allowed XSS payloads to persist.

## Attacker mindset
Sophisticated threat actor who recognized that defense-in-depth failures (upload validation + image processing + output encoding) could be chained together. By understanding image file format internals and library behavior, the attacker could craft payloads that survive sanitization filters, turning a seemingly secure image upload into a vector for template injection and XSS.

## Defensive takeaways
- Never render user-supplied or uploaded content unescaped, regardless of its apparent type or origin
- Implement strict Content Security Policy (CSP) to prevent inline script execution and restrict script sources
- Serve user-uploaded content from a different origin/domain to prevent same-origin script execution
- Apply defense-in-depth to image uploads: validate MIME type, magic bytes, and re-encode images completely (not just transform)
- Use libraries that fully re-encode images rather than in-place transformation (forces reconstruction of image structures)
- Audit all dynamic template loading mechanisms for proper output encoding
- Test image processing pipelines against adversarial inputs, including polymorphic payloads
- Monitor for suspicious byte patterns in EXIF, ECS, and other image metadata during upload

## Variant hunting
Similar vulnerabilities likely exist in other platforms with (1) user image uploads + same-origin serving, (2) dynamic content rendering via XHR without escaping, or (3) weak image re-encoding. Pinterest, Flickr, Instagram, and other photo-sharing platforms may be susceptible if they use similar template injection patterns. SVG uploads on any platform with unescaped rendering are particularly high-risk. Polymorphic PDF or other file format attacks using similar entropy-section manipulation techniques could target systems relying on library-based transformation.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1570 - Lateral Tool Transfer (polymorphic payload delivery)
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1566.002 - Phishing: Spearphishing Link (to Scholar with malicious image)
- T1204.001 - User Execution: Malicious Link (triggering XSS via hash parameter)
- T1657 - Defense Evasion: Abuse Image Processing Libraries

## Notes
This research exemplifies advanced exploitation requiring deep understanding of file format internals (JPEG entropy-coded segments, EXIF structures, PNG iDAT chunks) and image library behavior. The researcher developed a StandardizedImageProcessingTest suite (available on GitHub) to systematically test how different libraries (ImageMagick, GraphicsMagick, Libvips) preserve or strip image metadata and structures. Google VRP initially doubted polymorphic image feasibility, highlighting the gap between theoretical vulnerability understanding and practical PoC requirements. The technique has implications beyond XSS—similar approaches could conceal web shells or bypass 'self' CSP directives. Two endpoints were affected; the timeline shows 52 days from initial report to reward.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
