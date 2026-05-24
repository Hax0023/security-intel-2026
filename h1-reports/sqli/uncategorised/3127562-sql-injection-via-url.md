# SQL Injection via URL

## Metadata
- **Source:** HackerOne
- **Report:** 3127562 | https://hackerone.com/reports/3127562
- **Submitted:** 2025-05-05
- **Reporter:** jonasdiasrebelo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Description:**
Hi!
I discovered a SQL Injection vulnerability  via URL on the website ██████████. The vulnerability allows for the manipulation of SQL queries executed by the backend database, which could potentially lead to unauthorized data access or manipulation.

If you edit the sleep() value from 6 to another number, you will see that the page will have a longer/shorter delay to load. Thus 

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
Hi!
I discovered a SQL Injection vulnerability  via URL on the website ██████████. The vulnerability allows for the manipulation of SQL queries executed by the backend database, which could potentially lead to unauthorized data access or manipulation.

If you edit the sleep() value from 6 to another number, you will see that the page will have a longer/shorter delay to load. Thus proving SQLi.

██████████thank-you0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z
████████=sysdate(),sleep(6),0))XOR'Z
█████locations0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z/
██████careers0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z

## Impact

The ability to manipulate SQL queries can lead to:
Unauthorized access to sensitive data.
Potential data leakage.
Data manipulation or corruption.
Full database compromise if administrative permissions are accessible.

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
I found these directories vulnerable, try changing the value '6'.

████thank-you0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z
████=sysdate(),sleep(6),0))XOR'Z
██████████locations0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z/
██████careers0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z

## Suggested Mitigation/Remediation Actions
Use parameterized queries when dealing with SQL queries that contain user input. Parameterized queries allow the database to understand which parts of the SQL query should be considered as user input, therefore solving SQL injection.



</details>

---
*Analysed by Claude on 2026-05-24*
