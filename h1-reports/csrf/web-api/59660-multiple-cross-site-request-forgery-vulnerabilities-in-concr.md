# Multiple Cross Site Request Forgery Vulnerabilities in Concrete5 version 5.7.3.1

## Metadata
- **Source:** HackerOne
- **Report:** 59660 | https://hackerone.com/reports/59660
- **Submitted:** 2015-05-05
- **Reporter:** egix
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Concrete5 implements a Synchronizer Token Pattern in order to provide anti-CSRF capabilities, which is done within the Concrete\Core\Validation\CSRF\Token class. However, the application fails to properly use this feature in every block or dashboard page which makes a system state change, such as settings modification. As a result, the application is vulnerable to some Cross Site Request Forgery (

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

Concrete5 implements a Synchronizer Token Pattern in order to provide anti-CSRF capabilities, which is done within the Concrete\Core\Validation\CSRF\Token class. However, the application fails to properly use this feature in every block or dashboard page which makes a system state change, such as settings modification. As a result, the application is vulnerable to some Cross Site Request Forgery (CSRF) attacks.

</details>

---
*Analysed by Claude on 2026-05-24*
