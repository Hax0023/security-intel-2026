# Unrestricted File Upload Leading to Stored XSS via SVG in PNG Container

## Metadata
- **Source:** HackerOne
- **Report:** 880099 | https://hackerone.com/reports/880099
- **Submitted:** 2020-05-21
- **Reporter:** semsem123
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Unrestricted File Upload, Stored Cross-Site Scripting (XSS), Improper Content-Type Validation, SVG/XML Execution in Browser
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's wiki page file upload functionality fails to properly validate file contents, allowing attackers to upload SVG payloads disguised as PNG files. When users interact with the uploaded file, the browser executes embedded JavaScript code within the SVG, resulting in stored XSS accessible to all users with wiki access.

## Attack scenario
1. Attacker authenticates to GitLab and navigates to a project wiki
2. Attacker creates a new wiki page and uploads a malicious SVG file with .png extension containing JavaScript in onload/onclick event handlers
3. GitLab's upload mechanism fails to validate actual file content, accepting the SVG as a PNG based on extension alone
4. The file is stored on GitLab's servers and embedded in the wiki page with image references
5. When legitimate users view the wiki page and click the rendered triangle graphic, the browser executes the malicious JavaScript
6. The XSS payload executes in the context of the user's authenticated GitLab session, potentially stealing session tokens or performing actions on behalf of the user

## Root cause
GitLab's file upload validation in wiki pages relies on file extension (.png) rather than validating actual MIME type or file content. SVG files embedded with executable JavaScript are accepted and served with incorrect Content-Type headers, allowing browsers to interpret and execute the embedded scripts.

## Attacker mindset
An opportunistic attacker seeking to compromise multiple GitLab users with minimal effort. By creating a public wiki page in a public project, the attacker achieves maximum exposure. The attack requires minimal technical skill—simply wrapping malicious SVG code in a .png extension—making it attractive for low-sophistication threat actors.

## Defensive takeaways
- Implement server-side file content validation that checks magic bytes and actual file structure, not just extensions
- Validate uploaded file MIME types against expected types and verify content matches declared type
- Serve user-uploaded files with restrictive Content-Type headers (e.g., 'application/octet-stream') to prevent browser interpretation
- Implement Content-Security-Policy headers on wiki pages to restrict script execution from uploaded content
- Scan uploaded files for embedded scripts, SVG event handlers, and other executable content before storage
- Use dedicated storage domains (not same-origin) for user uploads to limit XSS scope
- Sanitize SVG files by stripping event handlers and potentially restricting SVG entirely in user uploads

## Variant hunting
Test other image formats (.jpg, .gif, .webp) for similar bypass techniques using polyglot files
Attempt uploading HTML files with image extensions to wiki and other file upload endpoints
Test profile picture uploads, project avatars, and other file upload features in GitLab with SVG payloads
Investigate whether uploaded files are served from a separate domain and if CSP policies differ
Test polyglot files combining valid PNG headers with SVG/JavaScript content
Attempt XXE attacks through SVG uploads with external entity references
Check if other markup injection techniques work (XHTML, MathML, embedded objects)

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1059.007
- T1071.001

## Notes
This vulnerability demonstrates a common bypass pattern where attackers exploit separation between validation layers. The attacker only needed to change file extension while preserving SVG content—a simple but effective technique. The wiki visibility setting exacerbates impact by potentially exposing the payload to thousands of users. The report's impact assessment correctly identifies this as particularly dangerous in public projects. GitLab's response would likely involve implementing proper content validation and Content-Security-Policy headers specifically for wiki content.

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
*Analysed by Claude on 2026-05-24*
