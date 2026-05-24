# Group admin can remove user from all his groups via API

## Metadata
- **Source:** HackerOne
- **Report:** 199286 | https://hackerone.com/reports/199286
- **Submitted:** 2017-01-18
- **Reporter:** nickvergessen
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** api
- **CVEs:** None
- **Category:** uncategorised

## Summary
### Steps
1. As admin make user1 group admin for group1 and group2
2. As user1 create a new user user2
3. As user1 try to remove the user from both groups via the UI
4. Take the first `togglegroup.php` request and replay it with `group2` on curl

### Expected
Should not work

### Actual
The group-admin can escape his groups and create users that are not part of his groups.

Also possible via the p

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

### Steps
1. As admin make user1 group admin for group1 and group2
2. As user1 create a new user user2
3. As user1 try to remove the user from both groups via the UI
4. Take the first `togglegroup.php` request and replay it with `group2` on curl

### Expected
Should not work

### Actual
The group-admin can escape his groups and create users that are not part of his groups.

Also possible via the provisioning_api.

Either the restriction should be enforced on the api endpoints (not only in the UI), or the restriction in the UI should be removed.


</details>

---
*Analysed by Claude on 2026-05-24*
