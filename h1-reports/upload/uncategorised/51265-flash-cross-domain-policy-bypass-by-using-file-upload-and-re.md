# Flash Cross Domain Policy Bypass via File Upload and HTTP Redirects in Chrome

## Metadata
- **Source:** HackerOne
- **Report:** 51265 | https://hackerone.com/reports/51265
- **Submitted:** 2015-03-12
- **Reporter:** irsdl
- **Program:** Google Chrome / Adobe Flash
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF), Cross-Domain Policy Bypass, Information Disclosure, Open Redirect Abuse
- **CVEs:** CVE-2015-0337
- **Category:** uncategorised

## Summary
A vulnerability in Google Chrome's Flash implementation allows attackers to bypass cross-domain policies by chaining file uploads with HTTP redirects. By uploading a file to an attacker-controlled redirect endpoint, Flash will follow the redirect and disclose the response content via UPLOAD_COMPLETE_DATA events, and will forward POST requests with 307/308 status codes without CORS validation.

## Attack scenario
1. Attacker hosts a malicious SWF file on attacker.com that uses ActionScript FileReference.upload()
2. Victim visits attacker.com and the SWF is loaded, targeting an open redirect endpoint on 0me.me
3. The redirect parameter points to a sensitive endpoint like plus.google.com
4. The SWF initiates a file upload POST request to the redirect endpoint
5. 0me.me responds with 301/302 redirect (or 307/308 with same-method redirect) to plus.google.com
6. Chrome's Flash plugin follows the redirect without checking cross-domain policy and discloses response content via UPLOAD_COMPLETE_DATA event

## Root cause
Google Chrome's Flash implementation does not properly enforce Flash cross-domain policy (crossdomain.xml) validation when FileReference.upload() requests are redirected via HTTP 3xx status codes. Additionally, 307/308 redirects preserve the HTTP method (POST) and body, allowing POST requests to be forwarded to unintended destinations without CORS checks.

## Attacker mindset
An attacker seeks to exfiltrate sensitive user data from authenticated sessions or read protected content on third-party websites. By leveraging Flash's file upload mechanism and the browser's automatic redirect handling, they can bypass same-origin policies and access resources that would normally be protected by CORS and cross-domain policies.

## Defensive takeaways
- Disable or deprecate Flash Player; migrate to modern web technologies (HTML5, WebAssembly)
- Enforce strict cross-domain policy validation on all HTTP redirects, not just initial requests
- Implement CORS headers and SameSite cookie attributes to prevent unauthorized cross-origin requests
- For 307/308 redirects, re-validate cross-domain policies before forwarding POST requests to new origins
- Implement Content Security Policy (CSP) to restrict Flash file execution and external resource loading
- Monitor and audit open redirect vulnerabilities on your infrastructure
- Use security headers like X-Frame-Options to prevent embedding of untrusted SWF files

## Variant hunting
Test other HTTP redirect codes (301, 302, 303, 304, 305, 306, 307, 308) with Flash plugins in different browsers
Investigate if other Flash APIs (HTTPRequest, Socket) have similar redirect-following behavior without proper CORS validation
Check if file upload endpoints with redirect capabilities can be chained to perform CSRF attacks on POST endpoints
Test if Flash's crossdomain.xml is properly re-validated after following redirects to different subdomains or ports
Verify if this affects other browser engines (Firefox, Safari, Edge) with Flash support
Examine if JWT tokens, API keys, or session cookies in response headers are leaked via UPLOAD_COMPLETE_DATA

## MITRE ATT&CK
- T1190
- T1566
- T1499
- T1537

## Notes
This vulnerability (CVE-2015-0337) was patched by Adobe and Chromium. The attack is heavily dependent on the target website having an open cross-domain policy or the attacker controlling an intermediate redirect endpoint. The vulnerability demonstrates how legacy browser plugins (Flash) can create dangerous attack surfaces when interacting with modern web security mechanisms. This is a Chrome-specific issue due to how Chrome's Pepper Flash (PPAPI) handles redirects differently than other implementations.

## Full report
<details><summary>Expand</summary>

CVE-2015-0337: https://helpx.adobe.com/security/products/flash-player/apsb15-05.html
+ 
https://code.google.com/p/chromium/issues/detail?can=2&start=0&num=100&q=&groupby=&sort=&id=425280

==VULNERABILITY DETAILS==
It is possible to bypass Flash Cross Domain policy in Google Chrome to read other websites' contents after a user uploads a file to a destination that redirects the user to the target website. It is also possible to send a file upload request to a target website without checking the cross domain policy by using an open redirect with status code of 307 (or 308).
This attack works as follows:
1- The "FileReference" class provides a means to upload file to a target server in ActionScript.
2- It accepts a URL as the destination for the file upload process.
3- It also has access to the target website's contents via the "UPLOAD_COMPLETE_DATA" event. This event is dispatched after data is received from the server after a successful upload.
4- If the target website redirects the user to another website, Flash in Google Chrome follows the redirection and discloses the destination content via the "UPLOAD_COMPLETE_DATA" event (first security issue). Moreover, if the target website redirects the user with status code of 307 (or 308), Google Chrome send the same file upload request to the final destination without checking the cross domain policy (second security issue).

==REPRODUCTION CASE==
A SWF PoC file and its ActionScript source has been attached.
This SWF file can be hosted on any website to target other websites.
http://attacker.com/chromeFileUploadCrossDomain.swf?url=redirect.php?input=https://plus.google.com/u/0/

"redirect.php" is just a simple open redirect to the target URL. An example is as follows:
http://attacker.com/chromeFileUploadCrossDomain.swf?url=http://0me.me/demo/openredirect/redirect.php?target=https://plus.google.com/u/0/%26status=301
Note: "0me.me" has an open cross domain policy and that's why we did not need to host it on "attacker.com".

An image has been attached that shows the result of exploiting this vulnerability. Source code of the "redirect.php" file has also been attached just for information.

</details>

---
*Analysed by Claude on 2026-05-24*
