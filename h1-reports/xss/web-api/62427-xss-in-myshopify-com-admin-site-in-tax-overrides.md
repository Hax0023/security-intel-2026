# XSS in myshopify.com Admin site in TAX Overrides

## Metadata
- **Source:** HackerOne
- **Report:** 62427 | https://hackerone.com/reports/62427
- **Submitted:** 2015-05-14
- **Reporter:** nismo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
POC:
If you create a collection such as "><IMG SRC=x onerror=prompt(7)> and then go to Settings / Taxes and select "Add a tax override" then on the "Add Tax Override for Rest of World" select the previously created collection of "><IMG SRC=x onerror=prompt(7)> you can see it on the screen (addtax.png).

If you press the recycle bin "Delete Entire Override" (delete.png) then  XSS is happening (x

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

POC:
If you create a collection such as "><IMG SRC=x onerror=prompt(7)> and then go to Settings / Taxes and select "Add a tax override" then on the "Add Tax Override for Rest of World" select the previously created collection of "><IMG SRC=x onerror=prompt(7)> you can see it on the screen (addtax.png).

If you press the recycle bin "Delete Entire Override" (delete.png) then  XSS is happening (xss.png)

Thanks


</details>

---
*Analysed by Claude on 2026-05-31*
