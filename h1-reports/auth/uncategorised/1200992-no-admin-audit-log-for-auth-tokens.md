# No admin audit log for auth tokens

## Metadata
- **Source:** HackerOne
- **Report:** 1200992 | https://hackerone.com/reports/1200992
- **Submitted:** 2021-05-18
- **Reporter:** rtod
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** auth
- **CVEs:** None
- **Category:** uncategorised

## Summary
There seems to be no audit trail for auth tokens.

* Creating tokens
* Revoking tokens
* Scope changes
* Renames
* Marking the token to be wiped

## Impact

As auth tokens are used to access your data having a track record when they are created helps a lot.
If you also take https://hackerone.com/reports/1193321 into account this would have been good information to track down what happened and by w

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

There seems to be no audit trail for auth tokens.

* Creating tokens
* Revoking tokens
* Scope changes
* Renames
* Marking the token to be wiped

## Impact

As auth tokens are used to access your data having a track record when they are created helps a lot.
If you also take https://hackerone.com/reports/1193321 into account this would have been good information to track down what happened and by who.

</details>

---
*Analysed by Claude on 2026-05-24*
