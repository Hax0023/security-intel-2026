# LDAP Server NULL Bind Connection Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 1937235 | https://hackerone.com/reports/1937235
- **Submitted:** 2023-04-06
- **Reporter:** 0xmaruf
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**
The remote LDAP server allows anonymous access

## References
  - https://www.tenable.com/plugins/nessus/10723
  - https://ldap.com/ldapv3-wire-protocol-reference-bind

## Impact

information  disclosure

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. run $ `nmap -n -sV --script "ldap* and not brute" -p 389 ██████████`

ch

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

**Description:**
The remote LDAP server allows anonymous access

## References
  - https://www.tenable.com/plugins/nessus/10723
  - https://ldap.com/ldapv3-wire-protocol-reference-bind

## Impact

information  disclosure

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. run $ `nmap -n -sV --script "ldap* and not brute" -p 389 ██████████`

check the response
## POC
██████

## Suggested Mitigation/Remediation Actions
Configure the service to disallow NULL BINDs.



</details>

---
*Analysed by Claude on 2026-05-24*
