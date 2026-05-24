# Authorization bypass -> IDOR -> PII Leakage

## Metadata
- **Source:** HackerOne
- **Report:** 1489470 | https://hackerone.com/reports/1489470
- **Submitted:** 2022-02-23
- **Reporter:** lubak
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi team!
During testing ████ I found  javascript file containing administrative panel functionality.
It is accessible at: 
https://████/█████████
In this file I found an end point responsible for returning data about applications of the website users to the website administrators.
The returned data contains PII data (Full name, phone and email) of military personnel, and or their family members.



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

Hi team!
During testing ████ I found  javascript file containing administrative panel functionality.
It is accessible at: 
https://████/█████████
In this file I found an end point responsible for returning data about applications of the website users to the website administrators.
The returned data contains PII data (Full name, phone and email) of military personnel, and or their family members.


## References
Steps to reproduce:

Run following curl command to retrieve data:
curl https://███/███ -X POST -data="url=%2F████████" -k

Modifying ██████████ parameter result in different Application being returned.
I have tested retrieving following ids: █████.

Trying to retrieve record 60000 returns no information, so maybe ~50000 applications are accessible.

## Impact

PII leak of military personnel and family members

## System Host(s)
█████████

## Affected Product(s) and Version(s)
/█████████

## CVE Numbers


## Steps to Reproduce
Run following command to retrieve data:
curl https://███████/███ -X POST -data="url=%2F████████" -k

Modifying ██████ parameter result in different Application being returned.
I have tested retrieving following ids: ███.
Trying to retrieve record 60000 returns no information, so maybe ~50000 applications are accessible.

## Suggested Mitigation/Remediation Actions
1. admin.js should be available only after Administrator successfully logs in
2. all administrative end points must check if authorized administrator is requesting them



</details>

---
*Analysed by Claude on 2026-05-24*
