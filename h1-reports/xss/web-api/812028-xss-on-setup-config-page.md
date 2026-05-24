# xss on setup config page 

## Metadata
- **Source:** HackerOne
- **Report:** 812028 | https://hackerone.com/reports/812028
- **Submitted:** 2020-03-06
- **Reporter:** jackzhou
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Nextcloud version: 18.0.1
In setup config page，setting `mysql Username` with payload`<script>alert(1)</script>`, and set others. F739076
then submit . F739077
this gif will show poc: F739069

## Impact

This is because the code does not filter dangerous characters. so dangerous characters need to be escaped.

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

Nextcloud version: 18.0.1
In setup config page，setting `mysql Username` with payload`<script>alert(1)</script>`, and set others. F739076
then submit . F739077
this gif will show poc: F739069

## Impact

This is because the code does not filter dangerous characters. so dangerous characters need to be escaped.

</details>

---
*Analysed by Claude on 2026-05-24*
