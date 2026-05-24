# Store Deletion or Sell without authentication

## Metadata
- **Source:** HackerOne
- **Report:** 1087382 | https://hackerone.com/reports/1087382
- **Submitted:** 2021-01-26
- **Reporter:** fr4via
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
In order for an owner to "close or sell" the store,  a password is required in order to confirm the decision, when the action is applied in the web application.  
It was identified that  the mobile application doesn't require credentials in order to perform the same action, thus by navigating to the Settings->Plan and Permissions -> Sell or Close [bottom of the page] , the user may 'close' the sho

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

In order for an owner to "close or sell" the store,  a password is required in order to confirm the decision, when the action is applied in the web application.  
It was identified that  the mobile application doesn't require credentials in order to perform the same action, thus by navigating to the Settings->Plan and Permissions -> Sell or Close [bottom of the page] , the user may 'close' the shop without issuing a password.
- The flow in the first case is shown in the screenshots  close1.png, close2.png, close3.png (see attachments)
- The flow in the second case is shown in the screenshot cloceAccountMobile1.png

## Impact

By the time that the physical access requirement is satisfied and since the application is not protected by any kind of user verification (e.g. login pin), as a first place, an unauthorised entity may access the options mentioned above add Sell or Delete a shop without providing any authentication.

</details>

---
*Analysed by Claude on 2026-05-24*
