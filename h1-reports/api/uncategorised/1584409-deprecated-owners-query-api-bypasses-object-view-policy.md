# Deprecated owners.query API bypasses object view policy

## Metadata
- **Source:** HackerOne
- **Report:** 1584409 | https://hackerone.com/reports/1584409
- **Submitted:** 2022-05-28
- **Reporter:** dyls
- **Program:** Unknown
- **Bounty:** $300
- **Severity:** unknown
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** uncategorised

## Summary
The deprecated owners.query API does not check object view policy. A user is able to view some information about an owner package which they do not have permission to see by calling this API. Since the API is deprecated, it could just be removed.

## Impact

An attacker is able to view some information about an owner package that they should not be able to see. Including, name, description, owner 

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

The deprecated owners.query API does not check object view policy. A user is able to view some information about an owner package which they do not have permission to see by calling this API. Since the API is deprecated, it could just be removed.

## Impact

An attacker is able to view some information about an owner package that they should not be able to see. Including, name, description, owner PHIDs, and repository PHIDs, and a path (which may be a path that belongs to a restricted repository).

</details>

---
*Analysed by Claude on 2026-05-24*
