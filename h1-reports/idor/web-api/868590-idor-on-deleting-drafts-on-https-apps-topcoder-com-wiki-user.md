# IDOR on deleting drafts on https://apps.topcoder.com/wiki/users/viewmydrafts.action via discardDraftId parameter

## Metadata
- **Source:** HackerOne
- **Report:** 868590 | https://hackerone.com/reports/868590
- **Submitted:** 2020-05-07
- **Reporter:** meryem0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi :)

On https://apps.topcoder.com/wiki/users/viewmydrafts.action, you can see your drafts, edit or delete them. Users can delete their own drafts on `https://apps.topcoder.com/wiki/users/viewmydrafts.action?discardDraftId=<DRAFT_ID>`. 
But there is no check and an attacker can change `discardDraftId` and delete all drafts.

## Impact

An attacker can delete other user's drafts.

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

Hi :)

On https://apps.topcoder.com/wiki/users/viewmydrafts.action, you can see your drafts, edit or delete them. Users can delete their own drafts on `https://apps.topcoder.com/wiki/users/viewmydrafts.action?discardDraftId=<DRAFT_ID>`. 
But there is no check and an attacker can change `discardDraftId` and delete all drafts.

## Impact

An attacker can delete other user's drafts.

</details>

---
*Analysed by Claude on 2026-05-24*
