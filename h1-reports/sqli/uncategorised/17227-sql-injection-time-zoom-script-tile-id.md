# SQL injection, time zoom script, tile ID

## Metadata
- **Source:** HackerOne
- **Report:** 17227 | https://hackerone.com/reports/17227
- **Submitted:** 2014-06-22
- **Reporter:** bitquark
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
The tile ID parameter to the tile zoom script is vulnerable to SQL injection.

The following will cause the script to run a benchmark, returning an error 8-10 seconds later:

https://staging.uzbey.com/zoom-image/BENCHMARK(10000000,SHA1(1))

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

The tile ID parameter to the tile zoom script is vulnerable to SQL injection.

The following will cause the script to run a benchmark, returning an error 8-10 seconds later:

https://staging.uzbey.com/zoom-image/BENCHMARK(10000000,SHA1(1))

</details>

---
*Analysed by Claude on 2026-05-24*
