# XSS in invite approval

## Metadata
- **Source:** HackerOne
- **Report:** 7887 | https://hackerone.com/reports/7887
- **Submitted:** 2014-04-17
- **Reporter:** nahamsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
If a translator's name is set as “><svg onload="prompt(/xss/);"> and requests to join a project, and the project admin clicks on the review to accept it, it results in an xss.

Screen:
attacker/translator:
http://prntscr.com/3ax1ca

contributor/admin:
http://prntscr.com/3ax1ix

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

If a translator's name is set as “><svg onload="prompt(/xss/);"> and requests to join a project, and the project admin clicks on the review to accept it, it results in an xss.

Screen:
attacker/translator:
http://prntscr.com/3ax1ca

contributor/admin:
http://prntscr.com/3ax1ix

</details>

---
*Analysed by Claude on 2026-05-24*
