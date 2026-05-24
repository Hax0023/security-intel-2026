# SQLi | in URL paths

## Metadata
- **Source:** HackerOne
- **Report:** 2958619 | https://hackerone.com/reports/2958619
- **Submitted:** 2025-01-26
- **Reporter:** almuntadhar0x01
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
A SQL Injection vulnerability was discovered in the customerId parameter of the URL path:
`███████`
We can observe this by adding a little quote in the customerId:
█████████
which will show the following error, indicating that its vulnerable to SQL Commands Injection:
███████

## Steps To Reproduce:
We can use any SQL Commend here, by just closing the Statement ( putting `')` and then 

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
A SQL Injection vulnerability was discovered in the customerId parameter of the URL path:
`███████`
We can observe this by adding a little quote in the customerId:
█████████
which will show the following error, indicating that its vulnerable to SQL Commands Injection:
███████

## Steps To Reproduce:
We can use any SQL Commend here, by just closing the Statement ( putting `')` and then use a command and also we make sure to make the rest as a comment, here is a basic SQL command i used:
███████
or we can use tools like SQLmap to get access to the database, here is the command i used:
```
sqlmap -u "██████
```
██████

## Impact

## Summary:

An attacker can exploit this to dump and download the database, Which will give them access to user informations.

</details>

---
*Analysed by Claude on 2026-05-24*
