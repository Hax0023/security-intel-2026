# Authorization Bypass: Unauthorized Board Creation via Clone Function

## Metadata
- **Source:** HackerOne
- **Report:** 2388183 | https://hackerone.com/reports/2388183
- **Submitted:** 2024-02-23
- **Reporter:** hakuna
- **Program:** Nextcloud Deck
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Authorization Bypass, Access Control, Permission Enforcement Logic Flaw
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Nextcloud Deck application implements board creation restrictions based on group membership, but fails to enforce the same restrictions on the board cloning functionality. Users belonging to unauthorized groups can bypass the creation restriction by cloning existing boards they have access to, effectively creating new boards without proper authorization.

## Attack scenario
1. Administrator configures group-based board creation restrictions, limiting board creation to specific groups only
2. Non-privileged user verifies they cannot create boards directly, as the UI button is hidden and API requests return 403 errors
3. User identifies an existing board they have access to (e.g., 'Personal' board or shared board)
4. User accesses the board's options menu and selects 'Clone board' feature
5. System creates a complete copy of the board without validating group-based creation restrictions
6. User renames and configures the cloned board as a new board, effectively circumventing access control policies

## Root cause
The authorization check for board creation (`POST /boards`) was not replicated in the board cloning endpoint (`POST /boards/{boardId}/clone`). The clone operation performs a direct duplication without invoking or respecting the same permission validation logic that applies to direct board creation requests.

## Attacker mindset
A disgruntled employee or user seeks to circumvent administrative controls. Rather than attempting complex exploits, they recognize that cloning is a documented feature and deduce that authorization checks may not be consistently applied across similar operations. This represents a common pattern where convenience features bypass security controls.

## Defensive takeaways
- Enforce authorization checks consistently across all operations that produce the same result (creation parity principle)
- Apply permission validation at the service layer rather than just the API/UI layer to prevent feature-specific bypasses
- Use a centralized authorization service for sensitive operations to ensure uniform policy enforcement
- Implement integration tests that verify restricted operations cannot be achieved through alternative flows
- Review all clone/duplicate/copy operations to ensure they enforce the same restrictions as direct creation
- Log and audit board creation attempts regardless of method (direct vs. clone) for security monitoring

## Variant hunting
Check if other duplication features (export/import, snapshot restore) bypass creation restrictions
Verify if moving or copying boards between folders circumvents group restrictions
Test whether sharing a board template allows unauthorized users to instantiate new boards
Examine if API endpoints for board templates or board presets have similar bypass vectors
Investigate whether admin-to-user board transfers or delegation features can be exploited
Check if archived boards can be unarchived to create unauthorized board instances

## MITRE ATT&CK
- T1190
- T1548
- T1556

## Notes
This is a classic authorization bypass vulnerability resulting from incomplete feature-specific permission enforcement. The vulnerability is straightforward to exploit requiring minimal technical knowledge. The fix likely requires adding a single authorization check to the clone endpoint before executing board duplication logic. The 403 error message on direct creation attempts suggests developers were aware of the restriction requirement but failed to apply it consistently across all board creation pathways.

## Full report
<details><summary>Expand</summary>

## Summary:
Admins can decide which groups are allowed to create boards. But a user who is part of an unauthorized group can easily create a new board by cloning an existing one and renaming it. 

## Steps To Reproduce:
 1. As an admin, create user1, group1 and group2, then assign group1 to user1
 2. In "Decks" app > "Deck settings", add group2 to the "Limit board creation to some groups" input. It is indicated that 
>*Users outside of those groups will not be able to create their own boards, but will still be able to work on boards that have been shared with them.*
				
 3. As user1, in "Decks" app, see that the button "+ Add board" is not displayed, which is expected. Sending the request directly will also fail with a 403 error and a message ""Creating boards has been disabled for your account.".
4. Now click on the "Personal" board options, and choose "Clone board". A copy of the board will be created. You can rename it, and you just created a new board with all "classic" options available. You could also directly send the request `POST /nextcloud/apps/deck/boards/board_number/clone`. 

{F3076346}

## Impact

Creating boards without permission.

</details>

---
*Analysed by Claude on 2026-05-24*
