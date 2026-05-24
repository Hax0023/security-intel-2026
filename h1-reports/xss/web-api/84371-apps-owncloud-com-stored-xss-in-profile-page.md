# apps.owncloud.com: Stored XSS in profile page

## Metadata
- **Source:** HackerOne
- **Report:** 84371 | https://hackerone.com/reports/84371
- **Submitted:** 2015-08-24
- **Reporter:** enderun07
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Owncloud,

I've found  A XSS vulnerability on apps.owncloud.com

When I add a comment to add any comment field,My profile page shows my latest comment

When I add a comment starts with "><img src=x onerror=confirm(2)> the page show this comment 

so XSS alert occurs in profile page.

Even if a victim is not authenticated,vulnerability occurs on page



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

Hi Owncloud,

I've found  A XSS vulnerability on apps.owncloud.com

When I add a comment to add any comment field,My profile page shows my latest comment

When I add a comment starts with "><img src=x onerror=confirm(2)> the page show this comment 

so XSS alert occurs in profile page.

Even if a victim is not authenticated,vulnerability occurs on page



</details>

---
*Analysed by Claude on 2026-05-24*
