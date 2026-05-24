# Reflected XSS on https://█████████html?url

## Metadata
- **Source:** HackerOne
- **Report:** 1071524 | https://hackerone.com/reports/1071524
- **Submitted:** 2021-01-04
- **Reporter:** nagli
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
##Vulnerable Website URL or Application:
https://███████html?url=javascript:alert("nagli")

##Description of Security Issue: (please limit to one site/app per submission)
Reflected XSS due to no input validation

█████████

##Remediation
Sanitize the input on the that parameter

##Best Regards
nagli

## Impact

Executing Javascript on behalf of the victim

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

##Vulnerable Website URL or Application:
https://███████html?url=javascript:alert("nagli")

##Description of Security Issue: (please limit to one site/app per submission)
Reflected XSS due to no input validation

█████████

##Remediation
Sanitize the input on the that parameter

##Best Regards
nagli

## Impact

Executing Javascript on behalf of the victim

</details>

---
*Analysed by Claude on 2026-05-24*
