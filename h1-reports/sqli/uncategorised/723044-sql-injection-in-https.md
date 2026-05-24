# SQL INJECTION  in https://████/██████████ 

## Metadata
- **Source:** HackerOne
- **Report:** 723044 | https://hackerone.com/reports/723044
- **Submitted:** 2019-10-25
- **Reporter:** mido0x0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Bug is : Sql injection in https://██████████/████████  via Referer
I've confirmed the vulnerability using sleep SQL queries with various arithmetic operations. The sleep command combined with the arithmetic operations will cause the server to sleep for various amounts of time depending on the result of the arithmetic operation.

##Proof of concept :
1- go to https://██████████/████████  and captur

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

Bug is : Sql injection in https://██████████/████████  via Referer
I've confirmed the vulnerability using sleep SQL queries with various arithmetic operations. The sleep command combined with the arithmetic operations will cause the server to sleep for various amounts of time depending on the result of the arithmetic operation.

##Proof of concept :
1- go to https://██████████/████████  and capture Request 
2- put this payload in Referer '+(select*from(select(sleep(6*6)))a

## Impact

##Impact :
An attacker can manipulate the SQL statements that are sent to the MySQL database and inject malicious SQL statements. The attacker is able to change the logic of SQL statements executed against the database.

</details>

---
*Analysed by Claude on 2026-05-24*
