# Reflected Xss bypass Content-Type: text/plain 

## Metadata
- **Source:** HackerOne
- **Report:** 472543 | https://hackerone.com/reports/472543
- **Submitted:** 2018-12-27
- **Reporter:** ahmed_alwardani
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Team:
--------------

1 - vulnerable subdomain : ci.cryptography.io
2 - after i tested this subdomain i found many payloads injected by me reflected but not executed
3 - so that i taked alook at the response and i found Content-Type: text/plain 
4 - so i searched about bypass Content-Type: text/plain and i found this book **cure53** page 73 tell me i can bypass it in IE browser before versio

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

Hello Team:
--------------

1 - vulnerable subdomain : ci.cryptography.io
2 - after i tested this subdomain i found many payloads injected by me reflected but not executed
3 - so that i taked alook at the response and i found Content-Type: text/plain 
4 - so i searched about bypass Content-Type: text/plain and i found this book **cure53** page 73 tell me i can bypass it in IE browser before version 10 

POC:
------

- go to https://ci.cryptography.io/adjuncts/20996283/hudsonyfm6u%3Cscript%3Ealert(document.domain)%3C/script%3Epub5j/plugins/favorite/assets.js
- you will see this {F397354}
- so let's try to install IE version 9 to try xss popup
- this is you will see {F397732}

something else ;
what is the java files main ?! {F397734}

## Impact

this method can affect victims that uses the IE browser before version 10 .

</details>

---
*Analysed by Claude on 2026-05-24*
