# Stored XSS via SVG File Upload with Format Spoofing in Inbox

## Metadata
- **Source:** HackerOne
- **Report:** 765679 | https://hackerone.com/reports/765679
- **Submitted:** 2019-12-29
- **Reporter:** homai
- **Program:** Outpost (HackerOne Report #765679)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper File Upload Validation, MIME Type Mismatch, Insufficient File Format Verification
- **CVEs:** None
- **Category:** web-api

## Summary
The application's file upload functionality in the Inbox feature lacks proper file format validation, allowing attackers to upload SVG files disguised with image extensions (png, gif, bmp). When victims open these files, embedded JavaScript executes in their browser context, enabling cookie theft and account takeover. The vulnerability stems from trusting file extensions rather than validating actual file content or MIME types.

## Attack scenario
1. Attacker creates a valid SVG file containing malicious JavaScript payload with onload event handler (e.g., alert(document.cookie))
2. Attacker renames the SVG file to have a benign image extension (.png, .gif, or .bmp) to bypass basic validation checks
3. Attacker logs into their account and initiates a new conversation with the victim through the Inbox feature
4. Attacker attaches the disguised SVG file and sends it to the victim
5. Victim opens/clicks the malicious file attachment, triggering the browser to render it as SVG
6. JavaScript payload executes in victim's browser context with access to cookies, enabling session hijacking and account takeover

## Root cause
The application validates file uploads based solely on file extension rather than inspecting actual file content, MIME type headers, or magic bytes. SVG files contain executable JavaScript that browsers will parse and execute when rendered, but the application treats them as harmless image formats if the extension suggests so.

## Attacker mindset
Exploit trust-based file validation to bypass security controls. Leverage browser's automatic file type detection and rendering capabilities to execute code in victim's trusted context. Target communication features where users are likely to open shared files, and abuse the implicit trust between conversation participants.

## Defensive takeaways
- Validate file uploads using magic bytes/file signatures rather than extensions
- Enforce strict MIME type validation on server-side with whitelist of allowed types
- Serve uploaded files with proper Content-Disposition: attachment headers to prevent rendering in browser
- Implement Content-Security-Policy headers to restrict inline script execution
- Consider re-encoding image files to strip embedded metadata and potentially malicious content
- Disable SVG uploads entirely if not required by application functionality
- Use sandboxed iframes or separate domains for displaying user-uploaded content
- Implement file type detection libraries that check actual file structure, not extension

## Variant hunting
Check if other file upload endpoints (profile pictures, documents, etc.) have similar validation issues
Test uploading HTML files with image extensions to see if stored XSS occurs
Attempt uploading polyglot files (valid as multiple formats) to bypass whitelists
Investigate if PDF uploads are properly validated, as PDFs can embed JavaScript
Test if XML/XXE payloads in image extensions trigger file inclusion vulnerabilities
Check if animated GIF or WebP files with embedded scripts are properly handled
Verify if file preview/thumbnail generation triggers code execution on the server

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1566 Phishing
- T1566.001 Phishing: Spearphishing Attachment
- T1204 User Execution
- T1059 Command and Scripting Interpreter
- T1185 Traffic Signaling
- T1539 Steal Web Session Cookie

## Notes
The vulnerability is particularly dangerous in a messaging/collaboration context where users have natural tendency to open shared files. The use of SVG format is noteworthy as it's a legitimate image format but inherently capable of executing scripts, creating a security paradox. Browsers' automatic content-type detection based on file content rather than extensions increases the attack surface. The report demonstrates proof-of-concept with cookie theft, which can directly lead to account compromise if HttpOnly flag is not set on session cookies.

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
*Analysed by Claude on 2026-05-12*
