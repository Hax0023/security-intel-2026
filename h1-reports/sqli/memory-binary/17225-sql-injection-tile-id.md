# SQL injection, tile ID

## Metadata
- **Source:** HackerOne
- **Report:** 17225 | https://hackerone.com/reports/17225
- **Submitted:** 2014-06-22
- **Reporter:** bitquark
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Command Injection - Generic
- **CVEs:** None
- **Category:** memory-binary

## Summary
The tile ID parameter to the tile image script is vulnerable to SQL injection.

The following will cause the script to run a benchmark, returning 8-10 seconds later:

https://staging.uzbey.com/tiles1600/693/sleep(10)

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

The tile ID parameter to the tile image script is vulnerable to SQL injection.

The following will cause the script to run a benchmark, returning 8-10 seconds later:

https://staging.uzbey.com/tiles1600/693/sleep(10)

</details>

---
*Analysed by Claude on 2026-05-24*
