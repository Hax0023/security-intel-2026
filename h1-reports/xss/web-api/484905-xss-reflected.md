# XSS Reflected 

## Metadata
- **Source:** HackerOne
- **Report:** 484905 | https://hackerone.com/reports/484905
- **Submitted:** 2019-01-24
- **Reporter:** manshum12
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Team ,

I found that https://████████/████/household/updateProfileInfo.action has vulnerability by XSS Reflected in household.householdID parameter .

I can verify it with following URL: https://█████████/██████/household/updateProfileInfo.action?household.householdID=%27;alert(document.domain)//

## Impact

XSS Reflected Attack

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

Hi Team ,

I found that https://████████/████/household/updateProfileInfo.action has vulnerability by XSS Reflected in household.householdID parameter .

I can verify it with following URL: https://█████████/██████/household/updateProfileInfo.action?household.householdID=%27;alert(document.domain)//

## Impact

XSS Reflected Attack

</details>

---
*Analysed by Claude on 2026-05-24*
