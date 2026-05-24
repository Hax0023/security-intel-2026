# Open Redirect and XSS via SVG File Upload in Rocket.Chat

## Metadata
- **Source:** HackerOne
- **Report:** 368927 | https://hackerone.com/reports/368927
- **Submitted:** 2018-06-19
- **Reporter:** w2w
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Open Redirect, Cross-Site Scripting (XSS), Insufficient File Type Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Rocket.Chat allowed uploading SVG files to the file-upload endpoint without proper validation, enabling attackers to embed JavaScript within SVG files. When victims accessed the uploaded file via the open.rocket.chat domain, the embedded JavaScript could execute, allowing open redirects to phishing sites or malicious payload delivery.

## Attack scenario
1. Attacker crafts a malicious SVG file containing embedded JavaScript code (e.g., redirect script)
2. Attacker uploads the SVG file to any Rocket.Chat channel using the file upload feature
3. File is stored on storage.googleapis.com but served via open.rocket.chat/file-upload/ID/filename.svg URL
4. Attacker shares the file URL with target victims via chat message, email, or social engineering
5. Victim clicks the link and the SVG file is downloaded/rendered in the browser from the trusted open.rocket.chat domain
6. Embedded JavaScript executes in victim's browser context, performing redirect to phishing site, malware distribution, or credential theft

## Root cause
Rocket.Chat's file upload validation was insufficient - the application only blacklisted specific dangerous file extensions (HTML, SHTML, PHP) but failed to recognize SVG as a viable XSS vector. SVG files are XML-based and can contain embedded JavaScript via event handlers or script tags, yet were allowed through the upload filter.

## Attacker mindset
An attacker recognized that SVG files, while appearing benign and often used for legitimate purposes, can execute JavaScript just like HTML. By leveraging the whitelist approach (only blocking known bad extensions rather than using a whitelist of safe types), the attacker found a bypass. The trusted domain context (open.rocket.chat) increases effectiveness since victims are more likely to trust URLs from the legitimate service.

## Defensive takeaways
- Implement whitelist-based file type validation instead of blacklist approach - only allow explicitly safe file types
- Validate file content/MIME type in addition to extension to prevent extension spoofing
- Use a separate domain or subdomain for serving user-uploaded content (Content Delivery Isolation) to prevent XSS in the application's origin
- Implement Content-Security-Policy headers to restrict script execution in uploaded content
- Serve uploaded files with Content-Disposition: attachment header to force download instead of rendering
- Consider using a CDN with proper security headers and CORS restrictions
- Regularly audit and update the list of blocked file types, including vector formats (SVG, PDF, etc.)
- Implement sandboxing or content inspection for file uploads

## Variant hunting
Test other vector file formats: PDF with embedded JavaScript, XML files, SVGZ (compressed SVG), animated GIFs with event handlers
Check if other media formats can bypass validation: WEBP, APNG, ICO files
Test polyglot files combining safe extensions with dangerous content
Verify if Content-Type header manipulation allows serving content as different types
Check if path traversal exists in file-upload/ID/filename parameter
Test if double extensions (file.svg.png) bypass filtering
Verify CORS and cross-origin resource sharing policies on the upload domain
Check for XXE (XML External Entity) vulnerabilities in SVG processing

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1059

## Notes
This report demonstrates a common vulnerability pattern where developers implement blacklist-based filtering rather than whitelist-based validation. The attacker specifically noted that HTML, SHTML, and PHP were already blocked, indicating previous awareness of file upload risks, yet SVG slipped through. The use of a content delivery network (storage.googleapis.com) with a trusted domain frontend (open.rocket.chat) increased attack viability. This is a good example of why security controls must be comprehensive and understand the full attack surface of file formats.

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
