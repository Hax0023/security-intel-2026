# PII leakage due to scrceenshot of health records

## Metadata
- **Source:** HackerOne
- **Report:** 693933 | https://hackerone.com/reports/693933
- **Submitted:** 2019-09-12
- **Reporter:** alyssa_herrera
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Document shows a screenshot of a medical record for a soldier 
**Description:**
One of the slides describes the CIV# and PAD DSN# along with some information relating to the soldier such as their name, the information appears to be old but could be still be an issue if they're in service
## Impact
High? maybe critical? Unsure on impact 
## Step-by-step Reproduction Instructions
Check 

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

**Summary:**
Document shows a screenshot of a medical record for a soldier 
**Description:**
One of the slides describes the CIV# and PAD DSN# along with some information relating to the soldier such as their name, the information appears to be old but could be still be an issue if they're in service
## Impact
High? maybe critical? Unsure on impact 
## Step-by-step Reproduction Instructions
Check slide 13 specifically but there's other slides that are suspect too
https://███████/wp-content/uploads/2018/12/HR_TECH_WOBC_Perform_eMILPO_Functions_eMILPO_Brief.pptx

## Product, Version, and Configuration (If applicable)
N/A
## Suggested Mitigation/Remediation Actions
Purge Doc

## Impact

An attacker could assume soldier identities and learn more about possible health information related to them

</details>

---
*Analysed by Claude on 2026-05-24*
