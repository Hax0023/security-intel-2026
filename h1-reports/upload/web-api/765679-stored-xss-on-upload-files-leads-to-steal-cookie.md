# Stored XSS via SVG File Upload Bypass - Cookie Theft and Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 765679 | https://hackerone.com/reports/765679
- **Submitted:** 2019-12-29
- **Reporter:** homai
- **Program:** Outpost (app.outpost.co)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), File Upload Validation Bypass, Insufficient File Type Validation, Session Hijacking
- **CVEs:** None
- **Category:** web-api

## Summary
The application fails to properly validate uploaded file formats in the Inbox messaging feature, allowing attackers to upload SVG files disguised as image formats (PNG, BMP, GIF) by renaming extensions. When victims open these files, embedded JavaScript payloads execute in the browser context, enabling cookie theft and potential account takeover.

## Attack scenario
1. Attacker creates an SVG file containing malicious JavaScript payload (e.g., onload handler stealing document.cookie)
2. Attacker renames the SVG file with a benign image extension (e.g., .png, .bmp, .gif) to bypass client-side validation
3. Attacker logs into victim account and sends a message with the disguised SVG file as attachment
4. Victim receives message and clicks on the file attachment, opening it in browser
5. Browser renders SVG content and executes embedded JavaScript payload in victim's security context
6. Attacker receives victim's session cookies and uses them to hijack the account

## Root cause
The application relies on file extension-based validation without verifying actual file content type (MIME type). Server-side validation is absent or insufficient, allowing SVG files (which are XML-based and executable in browsers) to be treated as inert image files.

## Attacker mindset
An attacker recognizes that SVG is a valid XML format executable as markup in browsers and exploits lenient file upload validation by simply changing file extensions. The attacker understands that victims will interact with attachments, making this a effective delivery mechanism for XSS. Cookie theft enables account takeover without requiring credential compromise.

## Defensive takeaways
- Implement server-side file type validation using MIME type detection (magic bytes) rather than relying on file extensions
- Maintain a whitelist of allowed MIME types and reject all others, especially blocking SVG uploads in contexts where they pose XSS risk
- Serve uploaded files with Content-Disposition: attachment and appropriate Content-Type headers to prevent inline execution
- Consider disallowing SVG uploads entirely in messaging/inbox features or serve them from isolated sandbox domains
- Implement Content Security Policy (CSP) headers to restrict script execution from uploaded content
- Sanitize or re-encode image files on the server to strip any embedded scripts or metadata
- Apply security headers like X-Content-Type-Options: nosniff to prevent browser content-type sniffing
- Perform regular security audits of file upload functionality and test with various file format bypass techniques

## Variant hunting
Test other XML-based formats (SVGZ, XDR, MathML) disguised with image extensions
Attempt uploading files with double extensions (.svg.png) or null byte injection (.svg%00.png)
Test polyglot files combining valid image data with SVG/script payloads
Check if other file types accepting JavaScript (HTML, XHTML, PDF with embedded scripts) can be uploaded
Verify if uploaded files can be accessed directly via predictable paths for XSS exploitation
Test whether Content-Type response headers can be manipulated via file metadata
Attempt uploading scripts in other image formats (WebP, HEIF) that may support embedded scripts

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1056.001
- T1539
- T1548
- T1021.006

## Notes
This is a classic file upload validation vulnerability chain leading to stored XSS. The severity is high because it affects messaging/communication features where users implicitly trust attachments, and the impact includes account takeover. The fix is straightforward (proper MIME validation) but the vulnerability is common due to developers underestimating SVG security risks. The report demonstrates good proof-of-concept methodology with clear reproduction steps and affected browser versions. Consider this a priority fix given the direct path to account compromise.

## Full report
<details><summary>Expand</summary>

## Summary:
There isn't a check mechanism on file format in Inbox which an attacker can send an SVG file as other formats such as png, gif or bmp by rename and change file format leads XSS attack and steal victim cookies.

## Steps To Reproduce:
You should create 2 accounts :
First account for the attacker and second one for the victim.

The attacker in my scenario: seq@seq.teamoutpost.com
The victim in my scenario: seq1@seq1.teamoutpost.com

  1. Please log in to the first account via this [link] (https://app.outpost.co/sign-in) 
  1. From Inbox create New Conversation and attached following files (Attached on this report) and send 
       These files are an SVG file which changes file format to png, bmp, gif
       If you want to see payload open file by notepad. you'll see payload like the following code :

```
<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
 width="2560.000000pt" height="1600.000000pt" viewBox="0 0 2560.000000 1600.000000"
 preserveAspectRatio="xMidYMid meet" onload="alert(document.cookie)">
```
  1. Whenever victim clicks on each file, open a new tab and XSS attack occurs and steal the victim's cookie.

## Supporting Material/References:

Browsers :
Mozilla Firefox 71.0
Google Chrome 79.0.3945.88

  * [attachment / reference]

For clarification, you can watch POC file (Attached on this report)

If you have any questions, let me know.

Best regards.

## Impact

Attacker can send malicious files to victims and steals victim's cookie leads to account takeover.

</details>

---
*Analysed by Claude on 2026-05-24*
