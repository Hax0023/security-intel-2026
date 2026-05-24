# Broken Authentication

## Metadata
- **Source:** HackerOne
- **Report:** 409237 | https://hackerone.com/reports/409237
- **Submitted:** 2018-09-12
- **Reporter:** websecnl
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
**Summary:** IDOR

**Description:** It is possible to access other user account by changing the parameter 'email' to another valid e-mail, i managed to guess an existing user '███████@███.com' which discloses the ███ 
Name and Surname.

## Impact
Information Disclosure

## Step-by-step Reproduction Instructions

1.Visit: https://██████
2. Register for an account
3. Follow the steps like in the att

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

**Summary:** IDOR

**Description:** It is possible to access other user account by changing the parameter 'email' to another valid e-mail, i managed to guess an existing user '███████@███.com' which discloses the ███ 
Name and Surname.

## Impact
Information Disclosure

## Step-by-step Reproduction Instructions

1.Visit: https://██████
2. Register for an account
3. Follow the steps like in the attached pictures

## Product, Version, and Configuration (If applicable)
Web Application

## Suggested Mitigation/Remediation Actions
https://www.owasp.org/index.php/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet

## Impact

Information Disclosure

</details>

---
*Analysed by Claude on 2026-05-24*
