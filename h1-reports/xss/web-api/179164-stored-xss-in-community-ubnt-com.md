# Stored XSS via SVG File Upload in community.ubnt.com

## Metadata
- **Source:** HackerOne
- **Report:** 179164 | https://hackerone.com/reports/179164
- **Submitted:** 2016-10-31
- **Reporter:** vibs123i
- **Program:** Ubiquiti Networks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper File Upload Validation, Insufficient SVG Content Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can upload malicious SVG files containing embedded JavaScript to the Ubiquiti community platform, creating persistent XSS payloads accessible to all users without authentication. The vulnerability allows attackers to distribute malicious links via community features that execute arbitrary scripts in victim browsers when clicked.

## Attack scenario
1. Attacker creates account (vibhuti123_i) on community.ubnt.com
2. Attacker crafts SVG file with embedded JavaScript payload (e.g., <script> or event handlers)
3. Attacker uploads SVG file to community platform, receiving a direct image URL
4. Attacker shares the malicious image URL via community posts, messages, or replies targeting victim account
5. Victim (john_victim) clicks the link from trusted source (community.ubnt.com domain), bypassing suspicion
6. XSS payload executes in victim's browser context with access to session tokens, cookies, and page content

## Root cause
The application fails to properly sanitize SVG file content before storage and serving. SVG files are XML-based and can contain inline JavaScript, event handlers (onload, onerror), and script tags that execute in the browser. The server accepts and stores SVG files without stripping dangerous elements, and serves them with MIME types that allow script execution.

## Attacker mindset
An attacker leverages the trust users place in content from the legitimate community.ubnt.com domain to distribute XSS payloads without detection. By using SVG format (commonly perceived as safe image files), the attacker bypasses user caution. The public accessibility without authentication maximizes attack surface and victim reach.

## Defensive takeaways
- Implement strict SVG validation: strip all script tags, event handlers (on*), and foreign elements before storage
- Serve uploaded SVG files with Content-Security-Policy headers restricting script execution (script-src 'none')
- Use Content-Type: image/svg+xml with X-Content-Type-Options: nosniff to prevent MIME-sniffing
- Convert SVG files to raster formats (PNG/JPEG) on upload to eliminate dynamic content
- Sanitize all user-supplied content using established libraries (DOMPurify, sanitize-html) with strict allowlists
- Implement Content Security Policy (CSP) on all pages to prevent inline script execution
- Add security headers: X-XSS-Protection, X-Frame-Options, Strict-Transport-Security
- Perform server-side file type validation beyond extension checking (magic bytes/MIME type verification)
- Apply principle of least privilege to file upload directories (no execute permissions)

## Variant hunting
Upload other XML-based formats (SVG, XML, PDF) and test for script injection
Test image EXIF data injection in JPEG/PNG for XSS payloads
Upload files with polyglot content (image + script hybrid files)
Test nested SVG elements and use of <foreignObject> tags
Check if CSS @import or data: URIs execute in served SVG context
Test filename-based XSS if filenames are reflected in HTML
Verify if SVG transformation filters (feDisplacementMap, feConvolveMatrix) enable exploitation
Check for XXE (XML External Entity) injection via SVG upload

## MITRE ATT&CK
- T1190
- T1204.001
- T1566.002
- T1071.001
- T1059.007

## Notes
Report references OWASP documentation on SVG-based XSS attacks. The vulnerability is particularly severe due to: (1) authentication bypass - accessible without login, (2) persistence - stored on server, (3) distribution mechanism - easily shared via community features, (4) trust exploitation - appears to come from legitimate domain. The reporter provided video POC demonstrating practical exploitation. This is a classic case of insufficient input validation on file uploads combined with lack of output encoding/sanitization.

## Full report
<details><summary>Expand</summary>

I have created two accounts
one attacker account: vibhuti123_i
other victim account: John_victim

 attacker account:vibhuti123_i who will create a malicious link after uploading svg file embeded with script and doing stored xss.Now attacker vibhuti123_i will send this  stored xss malicious link to victim:john_victim by posts,message,reply of ubnt community features or anyother way of communication.After this John_victim will believe this link as it is saved on community.ubnt.com server.It's no way look dangerous so john_victim will click this link and xss gets executed.

This stored xss link created by attacker will execute in every account and also it is accessible without login.
http://community.ubnt.com/t5/image/serverpage/image-id/0iA7662344C5BC7B7E/image-size/thumb/is-preview/true?v=v2&px=100

Please go through Video POC:--
https://youtu.be/Z0UCmv-Tpqs 


PLease read the Document of OWASP.org about svg xss below:

https://www.owasp.org/images/0/03/Mario_Heiderich_OWASP_Sweden_The_image_that_called_me.pdf

</details>

---
*Analysed by Claude on 2026-05-12*
