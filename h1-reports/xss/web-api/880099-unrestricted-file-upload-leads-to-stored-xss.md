# Unrestricted File Upload Leading to Stored XSS via SVG in PNG Container

## Metadata
- **Source:** HackerOne
- **Report:** 880099 | https://hackerone.com/reports/880099
- **Submitted:** 2020-05-21
- **Reporter:** semsem123
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Unrestricted File Upload, Stored Cross-Site Scripting (XSS), Improper MIME Type Validation, SVG XML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A vulnerability in GitLab's wiki page file upload functionality allows attackers to upload SVG code disguised as PNG files, resulting in stored XSS execution. When users click the uploaded malicious image, JavaScript code embedded in the SVG is executed in their browser with full access to the wiki page context.

## Attack scenario
1. Attacker logs into GitLab and creates a project with public wiki visibility
2. Attacker creates a new wiki page and uploads a file with .png extension containing SVG payload with embedded JavaScript (onload event handler)
3. The file is stored on GitLab servers and served with incorrect MIME type (image/svg+xml instead of image/png)
4. Other users visiting the wiki page see the malicious image rendered as SVG content
5. When users click the image or it auto-loads, the onload handler triggers JavaScript execution
6. Attacker gains access to user's session cookies, CSRF tokens, and can perform actions on behalf of the victim

## Root cause
GitLab's file upload validation in wiki pages fails to properly validate file content against declared MIME types. The application trusts the file extension (.png) without validating actual file content. SVG files containing XML and JavaScript are treated as executable documents rather than static images, and proper Content-Security-Policy or X-Content-Type-Options headers are not enforced.

## Attacker mindset
An attacker would recognize that wiki pages are often viewed by multiple users and represent high-value targets for XSS attacks. By uploading a file with legitimate image extension containing malicious SVG, they bypass extension-based validation. The stored nature of the XSS means the payload persists and affects all users viewing the page, maximizing impact with minimal effort.

## Defensive takeaways
- Implement strict file type validation based on file content (magic bytes), not just extension
- Use whitelist-based file upload restrictions; only allow genuinely needed file types
- Serve uploaded files with correct, restrictive MIME types detected from actual content
- Implement X-Content-Type-Options: nosniff header to prevent MIME type sniffing
- Apply Content-Security-Policy headers to restrict script execution in uploaded content
- Consider serving user uploads from a separate domain to prevent session cookie access
- Sanitize SVG files or disable SVG uploads entirely if not required
- Implement comprehensive input validation on file metadata and content before storage
- Use security scanning tools to analyze uploaded files for malicious patterns

## Variant hunting
Similar vulnerabilities likely exist in other file upload functionality (project attachments, issue attachments, user avatars). Other XML-based formats (XML, XHTML, PDF with embedded JavaScript) may bypass similar validations. Check if other web-based document preview features suffer from similar issues. Polyglot files (valid PNG + valid SVG) may also bypass validation. Test upload functionality across all GitLab features that accept file uploads.

## MITRE ATT&CK
- T1190
- T1105
- T1566
- T1204
- T1547
- T1539

## Notes
The reporter demonstrated the vulnerability clearly with reproducible steps and a public example. The vulnerability requires user interaction (clicking the image) but affects all visitors to the page, making it a stored XSS with broad impact. The vulnerability was discoverable through basic security testing of file upload features and MIME type validation.

## Full report
<details><summary>Expand</summary>

### Summary

i found that i can upload png file with JavaScript code and execute it in wiki page.

### Steps to reproduce

(Step-by-step guide to reproduce the issue, including:)

1-login to gitlab account
2-open  your project
3-open Wiki page.
4-Click "New page" button.
5-attach png file which contain below code
 `<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg onload="alert(1)" xmlns="http://www.w3.org/2000/svg">
<polygon id="triangle" points="0,0 0,50 50,0" fill="#009900" stroke="#004400"/>
</svg>`
6-Click "Create page" button.
7-Click on green triangle 
8-if The alert dialog not appears from first time just click on it one more time 



### Impact

If wiki pages created by using this vulnerability are visible to everyone (Wiki Visibility setting is set to "Everyone With Access") in "Public" project, there is a possibility that a considerable number of GitLab users and visitors click a malicious link.

### Examples
gitlab.com

tested on Google Chrome

https://gitlab.com/semsemhacker123/semsemtest/-/wikis/ssaa-home
https://gitlab.com/semsemhacker123/semsemtest/-/wikis/uploads/1308853a75502f77b3e22a2f9b0cc88a/1111111.png

### What is the current *bug* behavior?

The alert dialog appears after clicking "green triangle " in created page.

### What is the expected *correct* behavior?

the png file it must be not executed as  `image/svg+xml`

## Impact

An attacker can use XSS to send a malicious script to an unsuspecting user. The end user’s browser has no way to know that the script should not be trusted, and will execute the script. Because it thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained by the browser and used with that site. These scripts can even rewrite the content of the HTML page

</details>

---
*Analysed by Claude on 2026-05-12*
