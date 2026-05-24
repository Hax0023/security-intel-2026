# XSS during presentation

## Metadata
- **Source:** HackerOne
- **Report:** 112372 | https://hackerone.com/reports/112372
- **Submitted:** 2016-01-23
- **Reporter:** hogarth45
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
It is possible for a presenter to xss a viewer
Video attached:

## Recreation steps
Create publish lesson and start a presentation (join presentation in another browser)
Select "Quick question"
Open response
Insert the question 
asdf"><img src=x onerror=prompt(1)>

The Javascript will fire on the presenter's side and the viewers side.

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

It is possible for a presenter to xss a viewer
Video attached:

## Recreation steps
Create publish lesson and start a presentation (join presentation in another browser)
Select "Quick question"
Open response
Insert the question 
asdf"><img src=x onerror=prompt(1)>

The Javascript will fire on the presenter's side and the viewers side.

</details>

---
*Analysed by Claude on 2026-05-24*
