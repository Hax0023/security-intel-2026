# Polymorphic Images for XSS on Google Scholar

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Google VRP (Google Scholar)
- **Bounty:** $6267.40
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Rendering, Inadequate Input Validation, Polymorphic Payload Bypass
- **Category:** web-api
- **Writeup:** https://blog.doyensec.com/2020/04/30/polymorphic-images-for-xss.html

## Summary
Google Scholar rendered user-supplied template snippets fetched via XHR without proper escaping, combined with an image upload feature serving from the same origin. An attacker could craft polymorphic images containing XSS payloads embedded in EXIF metadata, PNG iDAT chunks, or JPG entropy-coded segments that survived image processing transformations, allowing JavaScript execution in the context of the Scholar application.

## Attack scenario (step by step)
1. Attacker identifies that Google Scholar uses location.hash parameters to fetch and render template snippets via XHR without HTML escaping
2. Attacker discovers that Google Scholar allows users to upload images that are served from the same origin
3. Attacker crafts a polymorphic image with an XSS payload embedded in a location that survives the server's image processing (e.g., JPG ECS segment with specific byte patterns)
4. Attacker uploads the malicious image through Scholar's image upload functionality
5. Victim views the Scholar page containing a reference to the uploaded image through a crafted template parameter
6. The unescaped template snippet references the image from the same origin, browser parses the embedded XSS payload, and JavaScript executes with Scholar's privileges

## Root cause
The vulnerability resulted from three compounding issues: (1) unsafe DOM rendering of fetched templates via location.hash without HTML escaping, (2) user-controllable image uploads served from the same origin, and (3) insufficient understanding of how image processing libraries preserve data in different image file structures, allowing payloads to survive transformations

## Attacker mindset
A sophisticated attacker recognized that image processing libraries do not uniformly strip all data from image files and that different formats store data in predictable segments. Rather than accepting the initial rejection, the attacker reverse-engineered the specific transformations applied by Google's backend and crafted payloads that could persist through those operations, demonstrating advanced knowledge of image file formats and their processing.

## Defensive takeaways
- Always HTML-escape or use textContent (not innerHTML) when rendering user-supplied or dynamically fetched content, regardless of source
- Implement strict Content Security Policy (CSP) headers to prevent inline script execution even if XSS payloads are injected
- Serve user-uploaded content from a different origin/domain to prevent same-origin XSS exploitation
- Implement comprehensive image processing that strips all extraneous data (metadata, trailing bytes, chunks) rather than selective whitelisting
- Validate and re-encode images completely rather than just reprocessing them, ensuring polymorphic payloads cannot survive
- Use allowlists for accepted template parameters and validate against a strict whitelist before rendering
- Regularly audit image processing libraries for data preservation behaviors and test with malicious payloads

## Variant hunting
Search for other applications using similar patterns: (1) XHR-based template loading with hash parameters and unescaped rendering, (2) user image uploads combined with same-origin serving, (3) applications using image metadata whitelisting rather than complete stripping, (4) systems processing images without full re-encoding, (5) other Google properties or similar CMS platforms with templating features and image functionality

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol
- T1567 - Exfiltration Over Web Service
- T1598 - Phishing

## Notes
This research demonstrates advanced polyglot/polymorphic technique expertise. The attacker's persistence in developing a PoC after initial rejection showcases the importance of thorough vulnerability research. The technical depth involved understanding JPG ECS entropy-coded segments, PNG chunk structures, and image library transformation behaviors. Google Scholar later confirmed additional XSS instances using the same technique, indicating systemic issues. The researcher made their image processing test suite available (doyensec/StandardizedImageProcessingTest on Github), contributing to the security community.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
