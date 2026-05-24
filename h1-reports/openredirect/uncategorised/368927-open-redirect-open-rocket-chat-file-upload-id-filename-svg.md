# Open Redirect and XSS via SVG File Upload in Rocket.Chat

## Metadata
- **Source:** HackerOne
- **Report:** 368927 | https://hackerone.com/reports/368927
- **Submitted:** 2018-06-19
- **Reporter:** w2w
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Open Redirect, Cross-Site Scripting (XSS), Improper File Type Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Rocket.Chat's file upload feature fails to properly validate SVG files, allowing attackers to upload SVG files containing embedded JavaScript. When victims visit the file URL, the SVG executes arbitrary JavaScript, enabling open redirects to phishing sites or malware distribution. The vulnerability exists because SVG files are not restricted despite being capable of executing scripts, unlike HTML, SHTML, and PHP which are already blocked.

## Attack scenario
1. Attacker creates a malicious SVG file containing JavaScript code that redirects to a phishing site or triggers malware download
2. Attacker uploads the SVG file to any Rocket.Chat conversation/channel
3. The server stores the file on Google Cloud Storage but serves it via open.rocket.chat domain with a predictable URL pattern
4. Attacker shares the file link (e.g., open.rocket.chat/file-upload/ID/malicious.svg) with victims via phishing or social engineering
5. Victim clicks the link, browser interprets the SVG and executes embedded JavaScript in the context of the open.rocket.chat domain
6. JavaScript payload executes - victim is redirected to phishing site, malware downloads, or session tokens are exfiltrated

## Root cause
Insufficient file type validation on upload. The application blocks potentially dangerous file extensions (HTML, SHTML, PHP) but overlooks SVG files, which are XML-based and can contain executable script tags. The lack of Content-Type enforcement or SVG sanitization allows script execution.

## Attacker mindset
Attacker seeks to leverage trusted Rocket.Chat domain for social engineering by disguising malicious links as legitimate file shares from colleagues. SVG format bypasses existing blocklist, making it an effective vector for credential harvesting, malware distribution, or session hijacking.

## Defensive takeaways
- Implement comprehensive file type blocklist including SVG, or adopt allowlist approach for safe formats only
- Sanitize SVG files server-side using libraries that strip script content (e.g., bleach, DOMPurify)
- Serve all user-uploaded files from a separate subdomain (e.g., files.rocket.chat) to prevent cookie/session theft via XSS
- Set Content-Disposition: attachment header to force downloads rather than rendering in browser
- Implement Content-Security-Policy headers to restrict script execution from user content
- Validate MIME types server-side, not just file extensions
- Consider re-encoding/converting uploaded files to remove embedded content

## Variant hunting
Check for other XML-based formats that support scripts: SVGZ, XHTML, XML, XBM
Test image formats with embedded content: WebP with extended features, APNG with JavaScript
Verify if other media types bypass validation: PDF with embedded JavaScript, PostScript
Examine if polyglot files (e.g., JPEG+SVG) bypass validation
Check if unicode/encoding bypasses (e.g., SVG%00.txt) evade extension checks
Test if path traversal in filename parameter could access other files

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1080 - Taint Shared Content

## Notes
The vulnerability is straightforward but impactful. The attacker's suggestion to block SVG is a valid remediation, though proper sanitization would be better to preserve legitimate SVG functionality. The open.rocket.chat domain provides false trust to victims. The predictable URL structure (ID/filename) doesn't add security. This is a classic example of blocklist-based security failing when new attack vectors emerge.

## Full report
<details><summary>Expand</summary>

**Summary:** Open redirect through svg file upload

**Description:** When you upload a file to a chat, the link to it will look like https://open.rocket.chat/file-upload/ID/filename.svg, but the file will be on storage.googleapis.com.
We can embed js in our svg and when the victim goes to https://open.rocket.chat/file-upload/6ksXL2Mk4MonCcTpx/svgxss.svg, a redirect to the phishing site will occur, or any other js, for example, downloading the virus, will work.
I see you have forbidden downloading html, shtml and php file, I recommend you also prohibit svg, since it is also dangerous.

  1. Upload svg file in any chat (attached to the report)
  2. Go to open.rocket.chat/file-upload/ID/filename.svg.

**PoC:** https://open.rocket.chat/file-upload/6ksXL2Mk4MonCcTpx/svgxss.svg

## Impact

open redirect

</details>

---
*Analysed by Claude on 2026-05-24*
