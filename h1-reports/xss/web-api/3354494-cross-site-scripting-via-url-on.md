# Cross-Site Scripting via URL on ███████

## Metadata
- **Source:** HackerOne
- **Report:** 3354494 | https://hackerone.com/reports/3354494
- **Submitted:** 2025-09-23
- **Reporter:** jonasdiasrebelo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Description:

I discovered a Cross-Site Scripting (XSS) vulnerability on ███ , specifically through the GET method. This vulnerability allows an attacker to inject malicious scripts that could be executed, potentially leading to cookie theft, session hijacking, and other malicious actions.

Payload: <image src=1 onerror=confirm(9706)>

████████ is an official domain from DoD.
██████████
██████


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

I discovered a Cross-Site Scripting (XSS) vulnerability on ███ , specifically through the GET method. This vulnerability allows an attacker to inject malicious scripts that could be executed, potentially leading to cookie theft, session hijacking, and other malicious actions.

Payload: <image src=1 onerror=confirm(9706)>

████████ is an official domain from DoD.
██████████
██████

## References

█████

## Impact

Exploitation of this vulnerability can lead to severe consequences, including but not limited:
Session Hijacking: Attackers can steal cookies and impersonate legitimate users.

## System Host(s)
█████

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
