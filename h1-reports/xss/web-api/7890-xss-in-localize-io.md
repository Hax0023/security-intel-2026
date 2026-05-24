# XSS in Localize.io

## Metadata
- **Source:** HackerOne
- **Report:** 7890 | https://hackerone.com/reports/7890
- **Submitted:** 2014-04-17
- **Reporter:** siddiki
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
During signup I used "></code><svg/onload=prompt(1)> as my password.Just after pressing sign up I was forwarded to a new page,where that page was showing my username and asked to click to view my password.When I clicked the javascript executed.
Attachment: xss.png

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

During signup I used "></code><svg/onload=prompt(1)> as my password.Just after pressing sign up I was forwarded to a new page,where that page was showing my username and asked to click to view my password.When I clicked the javascript executed.
Attachment: xss.png

</details>

---
*Analysed by Claude on 2026-05-24*
