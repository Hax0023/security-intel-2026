# Apache Airflow Sql injection by authenticated user

## Metadata
- **Source:** HackerOne
- **Report:** 3078856 | https://hackerone.com/reports/3078856
- **Submitted:** 2025-04-05
- **Reporter:** nxczje
- **Program:** Unknown
- **Bounty:** $505
- **Severity:** low
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Apache Airflow, versions 2.10.5, is affected by a vulnerability that allows an attacker can manipulate query construction, leading to an SQL Injection vulnerability that may result in remote code execution.

## Impact

The DAGS that use the SQLColumnCheckOperator in the system will remote code execution.

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

Apache Airflow, versions 2.10.5, is affected by a vulnerability that allows an attacker can manipulate query construction, leading to an SQL Injection vulnerability that may result in remote code execution.

## Impact

The DAGS that use the SQLColumnCheckOperator in the system will remote code execution.

</details>

---
*Analysed by Claude on 2026-05-24*
