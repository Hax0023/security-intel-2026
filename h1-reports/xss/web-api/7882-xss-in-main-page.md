# XSS in main page

## Metadata
- **Source:** HackerOne
- **Report:** 7882 | https://hackerone.com/reports/7882
- **Submitted:** 2014-04-17
- **Reporter:** nahamsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
If a project name is saved with a XSS string such as: 
“><svg onload="prompt(/xss/);"><!--

and a translator visits it, it'll result in the xss executing in the main page, due to the fact that it shows your recent visits.

Screen:
http://prntscr.com/3awwuv

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

If a project name is saved with a XSS string such as: 
“><svg onload="prompt(/xss/);"><!--

and a translator visits it, it'll result in the xss executing in the main page, due to the fact that it shows your recent visits.

Screen:
http://prntscr.com/3awwuv

</details>

---
*Analysed by Claude on 2026-05-24*
