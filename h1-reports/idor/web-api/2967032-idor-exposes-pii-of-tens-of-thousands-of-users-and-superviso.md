# IDOR Exposes PII of Tens of Thousands of Users and Supervisors

## Metadata
- **Source:** HackerOne
- **Report:** 2967032 | https://hackerone.com/reports/2967032
- **Submitted:** 2025-01-30
- **Reporter:** tacnull
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**
While using the system as intended (submitting a SAAR), I noticed there is an insure direct object Reference vulnerability in the application. Users can modify the URL parameter `saarnId` to view and possibly edit other user's SAARs.
**CAC Required**

## References
https://cwe.mitre.org/data/definitions/639.html
https://cwe.mitre.org/data/definitions/284.html

## Impact

This vuln

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
While using the system as intended (submitting a SAAR), I noticed there is an insure direct object Reference vulnerability in the application. Users can modify the URL parameter `saarnId` to view and possibly edit other user's SAARs.
**CAC Required**

## References
https://cwe.mitre.org/data/definitions/639.html
https://cwe.mitre.org/data/definitions/284.html

## Impact

This vulnerability leaks the following information on tens of thousands of users:
* Address
* Full Name
* Email
* Phone Number
* DoB
* Supervisor
* DODID Number
* Controlled Unclassified Information
* Clearance Level
* User ID

## System Host(s)
███████

## Affected Product(s) and Version(s)
N/A

## CVE Numbers


## Steps to Reproduce
1. Navigate to the following endpoint: █████
2. Change the parameter value: saarnid to a lower number. 
3. View the information associated with the SAAR another user's SAAR.

## Suggested Mitigation/Remediation Actions
You can prevent Insecure Direct Object References (IDOR) by using secure identifiers (e.g., UUIDs) and verifying permissions.



</details>

---
*Analysed by Claude on 2026-05-24*
