# SQL injextion via vulnerable doctrine/dbal version

## Metadata
- **Source:** HackerOne
- **Report:** 1390331 | https://hackerone.com/reports/1390331
- **Submitted:** 2021-11-03
- **Reporter:** nickvergessen
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** SQL Injection
- **CVEs:** CVE-2021-43608
- **Category:** uncategorised

## Summary
## Summary:
SQL injection via limit parameter on user facing APIs

## Steps To Reproduce:
Run security scanner:

  1. REPORT /remote.php/dav/comments/files/1985
  1. XML input oc:filter-comments.oc:limit#text was set to 1'"
  1. You have an error in your SQL syntax

## Supporting Material/References:
For more details see:
https://github.com/nextcloud-gmbh/h1/issues/197

## Impact

Full flexed SQL 

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
SQL injection via limit parameter on user facing APIs

## Steps To Reproduce:
Run security scanner:

  1. REPORT /remote.php/dav/comments/files/1985
  1. XML input oc:filter-comments.oc:limit#text was set to 1'"
  1. You have an error in your SQL syntax

## Supporting Material/References:
For more details see:
https://github.com/nextcloud-gmbh/h1/issues/197

## Impact

Full flexed SQL injection via user provided input

</details>

---
*Analysed by Claude on 2026-05-24*
