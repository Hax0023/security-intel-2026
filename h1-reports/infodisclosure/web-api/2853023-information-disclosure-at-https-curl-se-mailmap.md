# Information Disclosure at : https://curl.se/.mailmap

## Metadata
- **Source:** HackerOne
- **Report:** 2853023 | https://hackerone.com/reports/2853023
- **Submitted:** 2024-11-20
- **Reporter:** haithamzakaria
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
=================
During a security assessment, it was discovered that email addresses were exposed in a publicly accessible location. The data was retrieved using standard tools, such as curl, without requiring authentication or special permissions. This raises a concern regarding the confidentiality of sensitive user information.
## Steps To Reproduce:
==================
 The followi

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
=================
During a security assessment, it was discovered that email addresses were exposed in a publicly accessible location. The data was retrieved using standard tools, such as curl, without requiring authentication or special permissions. This raises a concern regarding the confidentiality of sensitive user information.
## Steps To Reproduce:
==================
 The following email addresses were disclosed:   
at : https://curl.se/.mailmap
1. Andy Alt: arch_stanton5995@protonmail.com
2. Ali Khodkar: 129806877+Alikhodkar@users.noreply.github.com


## Supporting Material/References:
=============
go to : https://curl.se/.mailmap
now add you payload

## Impact

Exposing email addresses can lead to phishing attacks, spam, or social engineering attacks targeting the affected individuals.

If these emails are linked to privileged accounts (e.g., administrative roles or GitHub contributors), this exposure increases the risk of further exploitation, such as impersonation or unauthorized account access.

</details>

---
*Analysed by Claude on 2026-05-24*
