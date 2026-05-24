# Information Disclosure of Garbage Collection Cycle

## Metadata
- **Source:** HackerOne
- **Report:** 981796 | https://hackerone.com/reports/981796
- **Submitted:** 2020-09-14
- **Reporter:** ahmd_halabi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

Upon enumerating a subdomain content I found a directory that discloses the duration of the garbage collection cycles.
I think that these information should be kept private because public should not know information about the target application and how it operates or do its garbage collection process.

##Steps To Reproduce
1. Navigate to the target url: https://gopher.hey.com/metrics
2. Se

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

Hello,

Upon enumerating a subdomain content I found a directory that discloses the duration of the garbage collection cycles.
I think that these information should be kept private because public should not know information about the target application and how it operates or do its garbage collection process.

##Steps To Reproduce
1. Navigate to the target url: https://gopher.hey.com/metrics
2. See the data.

███

## Impact

This information may help attackers understand more things about the target application which may help in further investigation and exploitation.

Kind Regards.

</details>

---
*Analysed by Claude on 2026-05-24*
