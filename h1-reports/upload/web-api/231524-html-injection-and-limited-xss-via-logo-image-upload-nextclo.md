# HTML Injection and Limited XSS via Logo Image Upload - Nextcloud 12.0.0

## Metadata
- **Source:** HackerOne
- **Report:** 231524 | https://hackerone.com/reports/231524
- **Submitted:** 2017-05-24
- **Reporter:** netranger
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Unrestricted File Upload, HTML Injection, Cross-Site Scripting (XSS), Content-Type Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
Nextcloud 12.0.0's logo upload function fails to validate file types, allowing administrators to upload arbitrary HTML files containing JavaScript payloads. While CSP mitigates XSS in modern browsers, Internet Explorer 11 allows execution of JavaScript through SVG onload and IMG onerror attributes, potentially enabling session hijacking and privilege escalation between admin users.

## Attack scenario
1. Attacker identifies target Nextcloud instance and determines admin user
2. Attacker crafts malicious HTML file containing SVG/IMG JavaScript bypass payloads
3. Attacker gains or shares admin access, uploads HTML file via /apps/theming/ajax/updateLogo endpoint
4. Attacker social engineers admin victim to visit /apps/theming/logo URL via phishing
5. Victim opens logo URL in Internet Explorer 11, triggering JavaScript execution
6. Attacker's JavaScript executes in victim's session context, enabling data theft or lateral movement

## Root cause
The logo upload endpoint does not validate file MIME type or extension, accepting any file type. The uploaded file is then served with a content-type that allows browser interpretation as HTML/text rather than forcing image rendering. CSP implementation has insufficient IE 11 coverage for SVG and IMG tag event handlers.

## Attacker mindset
Opportunistic insider threat leveraging legitimate admin access to compromise peer administrators. Attacker recognizes that while admins are generally trusted, not all admins have OS-level access, making web-level privilege escalation valuable. IE 11 usage among targeted users is the key success factor.

## Defensive takeaways
- Implement strict file type validation on upload endpoints - check magic bytes/file signatures, not just extensions
- Enforce whitelist of allowed MIME types and reject anything outside the whitelist
- Serve uploaded files with restrictive Content-Type headers (image/png, image/jpeg) and X-Content-Type-Options: nosniff
- Add Content-Disposition: attachment header to force download rather than inline rendering
- Strengthen CSP with img-src restrictions and svg-src isolation
- Audit all file upload endpoints in theming and other modules for similar issues
- Monitor for IE 11 CSP bypass techniques in security advisories
- Implement additional CSRF protections for sensitive operations like logo changes

## Variant hunting
Check other upload endpoints in theming module (favicon, background images)
Audit document preview/thumbnail generation endpoints for similar validation gaps
Review plugin/app upload mechanisms for file type validation
Test avatar upload functionality for identical vulnerability
Examine backup/restore import features for unrestricted file upload
Check if SVG/XML external entity (XXE) injection possible via image upload
Test polyglot file uploads (valid image + HTML concatenated)
Investigate if uploaded files can be accessed with directory traversal

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1434 - External Remote Services
- T1566 - Phishing
- T1189 - Drive-by Compromise
- T1567 - Exfiltration Over Web Service
- T1598 - Phishing for Information

## Notes
Reporter responsibly acknowledged Nextcloud's threat model trusting admins but correctly identified that not all admin users have OS-level access. The vulnerability is contextual to IE 11 usage; modern browsers' CSP implementations effectively blocked the payloads. The attack requires social engineering component (tricking admin to visit URL), reducing practical impact but still valid for multi-admin deployments where privilege separation exists at application rather than OS level. No evidence of actual bounty payment provided in report.

## Full report
<details><summary>Expand</summary>

## Summary
The logo image upload function in Nextcloud Server v12.0.0 does not validate the uploaded file, leading to XSS in certain circumstances.

## Vulnerable URL(s)
Replace [server] with the IP address or hostname of your Nextcloud server.
File upload - http://[server]/nextcloud/index.php/apps/theming/ajax/updateLogo
XSS endpoint - http://[server]/nextcloud/index.php/apps/theming/logo

## Description
A Nextcloud user with administrator rights has the option to upload a new site logo image file. However, the Nextcloud server does not verify that the uploaded file is actually an image file and accepts any file. An HTML file can be uploaded as the logo and accessed at the XSS endpoint URL: http://[server]/nextcloud/index.php/apps/theming/logo.

If a user visits the XSS endpoint URL (through a phishing link for example; since the URL is located on the valid Nextcloud server this shouldn't be too difficult) the victim's browser renders the contents of the file like any HTML page. An attacker can also include Javascript in the HTML file but it will be blocked by most major browsers through Nextcloud's Content Security Policy. However, I found 2 Javascript vectors that appear to bypass CSP and result in successful Javascript execution under Internet Explorer 11 (see Reproduction section).

## Reproduction
Create an HTML file with the following content and upload it as the Nextcloud site's logo. Alternatively, upload the HTML file provided with this report.

<!DOCTYPE html>
<head>
</head>
<body>
<h1>The logo!</h1>

<p>This HTML page was uploaded instead of a logo image.</p>
<p>Content Security Policy (CSP) prevents Javascript from executing as far as I can tell - except in Internet Explorer 11. View this page in IE 11 and you should see a pair of Javascript alert dialogs demonstrating code execution.</p>
<!-- Following both bypass CSP in IE -->

<!-- For some reason if spaces appear in the alert text this one won't work -->
<svg/onload=alert('SVG

<img/id="alert&lpar;'image XSS')"/alt="/"src="/"onerror=eval(id)>'">

</body>
</html>

Once uploaded, visit http://[server]/nextcloud/index.php/apps/theming/logo in any web browser. The browser should display rendered HTML content. Javascript execution is blocked by Nextcloud's CSP in most browsers; however, if you visit the page in IE 11, a pair of Javascript alert boxes should appear. The use of the onload attribute in an SVG tag and an IMG onerror attribute both appear to execute Javascript in IE 11:

<svg/onload=alert('SVG')>
<img/id="alert&lpar;'image XSS')"/alt="/"src="/"onerror=eval(id)>'">

During testing, IE 11 on Windows 7, 10 and IE on Windows Phone 8.1 update 2 executed the Javascript. Firefox, Chrome, Edge, Opera Mini, and Safari IOS all rendered the HTML page but did not execute the Javascript.

## Impact/Notes
Only users who are members of the Admin group have permission to change the logo. The Nextcloud Threat Model (https://nextcloud.com/security/threat-model/) indicates that Nextcloud admins are trusted. Therefore, if this vulnerability is considered an acceptable risk I understand; I thought it best to report it just in case.

One potential attack could involve one user who has admin rights uploading a malicious HTML file and tricking another admin or regular user into visiting the logo page. If the victim is using IE 11, the attacker can execute Javascript code under the victim user's session and potentially bypass CSRF protections. If an admin user has access to the underlying server OS/insfrastucture, he/she already has the power to modify another user's settings, files, etc; however, not all admin users necessarily have permission to the underlying Nextcloud server OS or infrastructure. For example, in deployments with many people several users may be given admin permissions in the web interface but that does not mean they all have access to the underlying file system; they should not be able to modify or view another user's data even though they are web admins. This vulnerability could allow for that to happen if the victim uses IE 11. I only tested with IE 11; I don't know if other IE versions behave the same.

## Mitigation
To mitigate this vulnerability, consider restricting the logo file to image files only (png, jpg, etc.) and reject non-image files.

</details>

---
*Analysed by Claude on 2026-05-24*
