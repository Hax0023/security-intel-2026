# Sensitive Information Disclosure Through Config File

## Metadata
- **Source:** HackerOne
- **Report:** 1397788 | https://hackerone.com/reports/1397788
- **Submitted:** 2021-11-10
- **Reporter:** dh0pe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cleartext Storage of Sensitive Information
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
An attacker could gain access to sensitive information about usernames, encrypted passwords, internal IP addresses and configuration data of internal services.

## Steps To Reproduce:
- Go to https://zik.mtncameroon.net/common/queryconfig.action

## Remediation
Configure the application to not reveal sensitive information to client.

## References
https://cwe.mitre.org/data/definitions

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
An attacker could gain access to sensitive information about usernames, encrypted passwords, internal IP addresses and configuration data of internal services.

## Steps To Reproduce:
- Go to https://zik.mtncameroon.net/common/queryconfig.action

## Remediation
Configure the application to not reveal sensitive information to client.

## References
https://cwe.mitre.org/data/definitions/200.html

## Impact

A malicious user is able to gain sensitive information usernames, encrypted passwords, internal IP addresses and configuration data of internal services.

</details>

---
*Analysed by Claude on 2026-05-24*
