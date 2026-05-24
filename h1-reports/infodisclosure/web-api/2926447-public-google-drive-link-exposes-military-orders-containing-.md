# Public google drive link Exposes Military Orders Containing PII (Name, SSN etc..) and Operational Details

## Metadata
- **Source:** HackerOne
- **Report:** 2926447 | https://hackerone.com/reports/2926447
- **Submitted:** 2025-01-07
- **Reporter:** entropydrifter
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**
I found google drive link `https://drive.google.com/drive/folders/█████████`  at `https://████████.aspx?Mode=ReadOnly&Id=90dd0d3b-0ed1-e76b-128f-11ebc799ba55` contains pdfs at '/████ Internal/Orders' that discloses the following PII:

Full Name: ███████
Social Security Number (SSN): ███████
Home Address: ████, ██████
Marital Status: Married, 3 dependents (M03 in January 2021 order

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
I found google drive link `https://drive.google.com/drive/folders/█████████`  at `https://████████.aspx?Mode=ReadOnly&Id=90dd0d3b-0ed1-e76b-128f-11ebc799ba55` contains pdfs at '/████ Internal/Orders' that discloses the following PII:

Full Name: ███████
Social Security Number (SSN): ███████
Home Address: ████, ██████
Marital Status: Married, 3 dependents (M03 in January 2021 orders; S00 in earlier orders)
Security Clearance Level: ███

## How to reproduce 

1. Navigate to `https://██████.aspx?Mode=ReadOnly&Id=90dd0d3b-0ed1-e76b-128f-11ebc799ba55`.
2. Below the page you will find `https://drive.google.com/drive/folders/█████████`.
3. Go to `https://drive.google.com/drive/folders/███████`.
4. Open folder named `███████ Internal`.
5.Navigate to folder named `Orders`.
6. You will find the pdfs that discloses PII data as shown below in screen shots.

██████████

██████

## Impact

1. Privacy Violation: Exposes PII of personnel, violating privacy laws such as the U.S. Privacy Act of 1974.
2. Identity Theft and Fraud: Information like SSNs and home addresses can be used for malicious purposes.

## System Host(s)
██████

## Affected Product(s) and Version(s)
https://█████████.aspx?Mode=ReadOnly&Id=90dd0d3b-0ed1-e76b-128f-11ebc799ba55

## CVE Numbers


## Steps to Reproduce
1. Navigate to `https://██████.aspx?Mode=ReadOnly&Id=90dd0d3b-0ed1-e76b-128f-11ebc799ba55`.
2. Below the page you will find `https://drive.google.com/drive/folders/█████`.
3. Go to `https://drive.google.com/drive/folders/███`.
4. Open folder named `███ Internal`.
5.Navigate to folder named `Orders`.
6. You will find the pdfs that discloses PII data as shown below in screen shots.

█████

██████

## Suggested Mitigation/Remediation Actions
Remove the folder or make it private at least



</details>

---
*Analysed by Claude on 2026-05-24*
