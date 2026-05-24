# Cross-Site Scripting via URL on ███████

## Metadata
- **Source:** HackerOne
- **Report:** 3351408 | https://hackerone.com/reports/3351408
- **Submitted:** 2025-09-20
- **Reporter:** jonasdiasrebelo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Description:

Hi, team!
I discovered a Cross-Site Scripting (XSS) vulnerability on ████████, specifically through the GET method via URL. This vulnerability allows an attacker to inject malicious scripts that could be executed, potentially leading to cookie theft, session hijacking, and other malicious actions.

██████████ is an official campaign and website from the U.S. Department of Defense 

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

## Description:

Hi, team!
I discovered a Cross-Site Scripting (XSS) vulnerability on ████████, specifically through the GET method via URL. This vulnerability allows an attacker to inject malicious scripts that could be executed, potentially leading to cookie theft, session hijacking, and other malicious actions.

██████████ is an official campaign and website from the U.S. Department of Defense (DoD) to promote responsible drinking among Service members. The campaign is aligned with the Defense Health Agency and aims to provide Service members with the information and resources they need to make responsible alcohol choices, thereby supporting military readiness and resilience

## References

█████████

## Impact

Exploitation of this vulnerability can lead to severe consequences, including but not limited:
Session Hijacking: Attackers can steal cookies and impersonate legitimate users.

## System Host(s)
███████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Open the link:

███

## Suggested Mitigation/Remediation Actions
Apply context-dependent encoding and/or validation to user input rendered on a page.



</details>

---
*Analysed by Claude on 2026-05-24*
