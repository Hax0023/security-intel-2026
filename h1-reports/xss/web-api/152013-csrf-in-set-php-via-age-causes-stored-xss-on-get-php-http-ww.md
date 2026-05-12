# CSRF in set.php via age parameter causes Stored XSS on get.php

## Metadata
- **Source:** HackerOne
- **Report:** 152013 | https://hackerone.com/reports/152013
- **Submitted:** 2016-07-18
- **Reporter:** nahamsec
- **Program:** Rockstar Games
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF), Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Insecure Cookie Handling
- **CVEs:** None
- **Category:** web-api

## Summary
The set.php endpoint accepts unsanitized age parameter via POST without CSRF protection and stores it in a cookie, which is then reflected unsanitized in get.php. An attacker can craft a malicious HTML page that auto-submits a CSRF form to set.php with an XSS payload, which gets stored and executed when the victim visits get.php.

## Attack scenario
1. Attacker crafts a malicious HTML page containing a hidden form targeting set.php with JavaScript payload in the age parameter
2. Victim visits attacker's page while logged into Rockstar Games
3. Auto-submit script triggers POST request to set.php using victim's authenticated session
4. set.php stores the XSS payload in age cookie without validation or sanitization
5. Attacker redirects victim to get.php or victim visits it later
6. get.php retrieves and renders the age cookie value without HTML encoding, executing the stored XSS payload in victim's browser

## Root cause
Combination of three security failures: (1) Missing CSRF tokens on set.php POST endpoint, (2) No input validation or output encoding of age parameter before cookie storage, (3) No output encoding when rendering cookie value in get.php

## Attacker mindset
Attacker recognized that the age parameter flows from set.php into a cookie and then reflected into get.php without sanitization. By chaining CSRF with stored XSS, a single malicious page could compromise multiple victims without individual interaction, enabling session hijacking, credential theft, or malware distribution at scale.

## Defensive takeaways
- Implement CSRF tokens (synchronizer tokens, double-submit cookies, or SameSite) on all state-changing endpoints
- Validate and sanitize all user input before storing in cookies or databases
- Apply context-appropriate output encoding (HTML entity encoding, JavaScript encoding) when rendering user-controlled data
- Use Content Security Policy (CSP) to restrict script execution sources
- Implement HttpOnly and Secure flags on cookies to prevent JavaScript access
- Apply strict input validation for age parameter (numeric only, range validation)
- Use templating engines with auto-escaping enabled by default

## Variant hunting
Check other parameters in set.php for similar CSRF+XSS chains
Test get.php for DOM-based XSS if JavaScript processes cookie values
Audit other endpoints accepting cookie-stored user data
Look for similar patterns in other Rockstar Games properties
Test if other reflected parameters in get.php are also vulnerable
Check for second-order XSS through database storage mechanisms
Test for CSRF on other POST endpoints lacking token validation

## MITRE ATT&CK
- T1190
- T1566.002
- T1539
- T1598

## Notes
This is a classic example of chained vulnerabilities creating critical impact. The CSRF enables injection without user interaction, while stored XSS enables persistence. The use of base64-encoded data URI in POC demonstrates sophistication to bypass basic filters. Discovery date appears to be 2016 based on HackerOne report structure. The videoplayer_cache endpoint suggests potential for affecting multiple users accessing video content.

## Full report
<details><summary>Expand</summary>

Hello,

#Background:
Sending a POST request to set.php with age='PAYLOAD' will cause a stored XSS on the GET.php file (most likely caused by the cookie, since that's what the `age` is based on). For this vulnerability and in order to demonstrate BOTH CSRF and XSS I have written a simple script (tested on firefox)  that automatically sends the request to set.php and redirects you to the vulnerable file:

#POC:

````
<iframe style="display:none" name="csrf-frame" id="csrf-frame"></iframe><form method="POST" action="http://www.rockstargames.com/php/videoplayer_cache/set.php" target="csrf-frame" id="csrf-form" encType="application/x-www-form-urlencoded"><input type="text" name="age" value='<a href=data:text/html;base64,PHNjcmlwdD5hbGVydChkb2N1bWVudC5jb29raWUpOzwvc2NyaXB0Pg==>CLICK ME</a>' /></form><script>document.getElementById("csrf-form").submit();</script><script>var xssframe = document.getElementById('csrf-frame');xssframe.addEventListener("load", function() { window.location='http://www.rockstargames.com/php/videoplayer_cache/get.php'; }); </script>
````

Thanks,
Ben

</details>

---
*Analysed by Claude on 2026-05-12*
