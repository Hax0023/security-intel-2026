# WordPress 4.8.1 - Rogue Editor RCE via Same-Origin Frame Scripting

## Metadata
- **Source:** HackerOne
- **Report:** 263718 | https://hackerone.com/reports/263718
- **Submitted:** 2017-08-27
- **Reporter:** skansing
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Stored XSS, Privilege Escalation, Remote Code Execution, Clickjacking/Frame Scripting, Insufficient Access Control
- **CVEs:** None
- **Category:** memory-binary

## Summary
A WordPress editor can inject unfiltered content containing XSS payloads that, when visited by an administrator, enables same-origin frame scripting to perform arbitrary actions including plugin file modification and RCE. The vulnerability demonstrates how editor-level XSS can be trivially escalated to RCE through manipulating admin iframe contexts without additional user interaction beyond the initial admin visit.

## Attack scenario
1. Attacker with editor role crafts malicious HTML/JavaScript payload containing invisible iframe pointing to wp-admin/plugin-editor.php
2. Payload is uploaded as content or HTML file accessible to administrators (post, page, or uploaded file)
3. Administrator visits page containing the payload (via direct link, dashboard, or content review)
4. JavaScript executes in same-origin context, gaining access to plugin-editor iframe's DOM via contentWindow.document
5. Script automatically fills plugin file editor with PHP code (phpinfo or malicious code) and submits the form
6. Modified plugin file is saved to server and executed when accessed, achieving remote code execution

## Root cause
WordPress editor role permits unfiltered HTML/JavaScript content posting without sanitization, combined with lack of frame-busting headers (X-Frame-Options) and authentication re-verification on sensitive admin actions. Same-origin policy allows frame content manipulation when both parent and iframe share origin.

## Attacker mindset
A compromised or malicious editor account holder seeks to escalate to full system compromise by exploiting the trust administrators place in the editor role. The attacker leverages the fact that administrators will likely visit content posted by editors, making the exploitation transparent to the victim. The technique demonstrates that XSS in WordPress is not merely an information disclosure risk but a direct RCE vector.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN headers on all admin pages to prevent iframe embedding
- Require re-authentication and CSRF tokens for sensitive operations (plugin editing, file modification, user creation)
- Restrict editor role from posting unfiltered HTML content; sanitize or disable dangerous HTML tags even for editors
- Implement Content-Security-Policy headers to restrict script execution within admin context frames
- Apply HTML/JavaScript sanitization to all user-submitted content regardless of user role
- Use SameSite cookie attribute (Strict/Lax) to limit cookie transmission in cross-origin contexts
- Consider implementing frame-breaking JavaScript to prevent being embedded in potentially hostile pages
- Educate administrators on risks of editor role and implement role-based access controls more granularly

## Variant hunting
Search for XSS in themes and plugins that lack proper sanitization, as these inherit the same frame-scripting escalation potential
Identify all admin pages lacking X-Frame-Options headers that manipulate sensitive data (user management, settings, file operations)
Review other roles (contributor, author) for unfiltered content posting capabilities that could enable similar chains
Test custom post types and custom fields for XSS with admin iframe context manipulation
Examine AJAX endpoints exposed to editors that perform admin-level actions without re-authentication
Check for stored XSS in comments, user metadata, or plugin settings accessible to lower-privileged users

## MITRE ATT&CK
- T1190
- T1199
- T1021
- T1548
- T1059
- T1566

## Notes
This report highlights a critical systemic issue in WordPress security model: the assumption that XSS is contained to information disclosure is invalidated by same-origin frame scripting. The editor role's ability to post unfiltered content is intentional per WordPress design, but the security implications were underestimated. The PoC is particularly elegant because it requires no user interaction beyond the initial page visit. The researcher correctly identifies that all future XSS vulnerabilities in WordPress ecosystem should be re-evaluated for RCE potential through this vector, fundamentally changing severity assessments. The suggested fix of X-Frame-Options: DENY would be breaking change but necessary; window.open() bypass mentioned is valid but requires additional user interaction.

## Full report
<details><summary>Expand</summary>

#Background
This report is mainly about how a user with the role of editor, expectedly can post unfiltered content
but unexpectedly can pwn an administrator with a RCE chain due to same origin frame scripting.

Secondarily the report wants to highlight the technique used and the severity of it.

#Description
During my research I found that a XSS can, in the majority of cases, trivially be turned
into a RCE, by abusing same origin frame scripting in the XSS payload.

I demonstrated this "technique" in #263058 and #263109 (no need to read, there a POC in this report).
It can be used to do *almost* any action from the victims perspective, like adding an administrator or editing a plugin file.
This adds to the severity of XSS in core wp, themes and especially plugins.

It affect the understanding of the user role 'editor' and the ability to post unfiltered content
https://make.wordpress.org/core/handbook/testing/reporting-security-vulnerabilities/#why-are-some-users-allowed-to-post-unfiltered-html

An editor is a copy-paste and a administrator visit from RCE or performing any action.
Editors users / accounts them self are more attractive for cracking and social engineering.
Administrators are not aware of the risk associated with giving a user editor role or being a editor.
All future reports with XSS can be escalated to RCE resulting in increased severity.


# POC
This POC explores a rogue editor planting payload to RCE.

- Login as editor
- Upload a .html or plant the POC payload in content
- Login as administrator visit a link containing the payload

# POC Payload
The payload opens the plugin editor, edits a file and redirects to the edited file afterwards

```
<iframe src="http://127.0.0.1:8090/wp-admin/plugin-editor.php?file=hello.php" style="opacity:0">
</iframe>
<script>
setTimeout(function() {
  var p = "<?php phpinfo();"
  // full read/write control over dom, do anything(!)
  var d = document.querySelector("iframe").contentWindow.document;
  var c = d.querySelector("#newcontent")
  var s = d.querySelector("#submit")
  c.value = p
  s.click();
}, 2000);
setTimeout(function() {
  window.location.href = "http://127.0.0.1:8090/wp-content/plugins/hello.php"
}, 4000);
</script>
```

# Suggested Fix
the role editor should loose all privileges that can lead to scripting

consideration on hardening could be doing a BC break and switching to `x-frame-options: deny`.
However that can by bypassed by using `window.open(...)` instead of an iframe, but requires
the victim to click on the page after opening it. so this will only harden a bit.

another hardening option could be requiring password on critical actions such as
plugin install, file edit, etc. it will however have an impact on accessibility and
it might take time to find all the loop holes.


</details>

---
*Analysed by Claude on 2026-05-12*
