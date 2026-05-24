# Access Control: Inject tasks into other users decks

## Metadata
- **Source:** HackerOne
- **Report:** 867052 | https://hackerone.com/reports/867052
- **Submitted:** 2020-05-06
- **Reporter:** dedoc
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Broken Access Control, Missing Authorization Check, Privilege Escalation
- **CVEs:** CVE-2020-8179
- **Category:** uncategorised

## Summary
The Nextcloud Deck application fails to validate that a user has authorization to move tasks to stacks belonging to other users. By modifying the stackId parameter in a PUT request to /apps/deck/cards/*, an attacker can inject tasks into any user's deck, causing data pollution and potential disruption.

## Attack scenario
1. Attacker creates a task in their own deck (stackId: 1)
2. Attacker intercepts the PUT request when moving the task to another stack
3. Attacker modifies the stackId parameter from an authorized stack (e.g., 2) to a target stack owned by another user (e.g., 6)
4. Server processes the request and returns HTTP 200 OK without verifying ownership
5. Task is successfully added to the victim's deck without their knowledge or consent
6. Victim's deck is polluted with unwanted tasks from the attacker

## Root cause
The backend endpoint /apps/deck/cards/{id} performs a PUT operation without verifying that the requesting user has ownership or write permissions on the target stack (stackId). The authorization check only validates that the user can modify the card itself, not that they can move it to the specified destination.

## Attacker mindset
An attacker could exploit this to disrupt collaboration workflows by injecting spam, misleading tasks, or malicious content into colleagues' project management boards. This could damage team productivity, trust, and data integrity.

## Defensive takeaways
- Implement explicit authorization checks on the destination resource (stack) before allowing any modification
- Validate that the requesting user has write permissions on the target stackId
- Use role-based access control (RBAC) to determine which stacks a user can modify
- Log all cross-user resource access attempts for audit trails
- Consider implementing a two-step validation: verify card ownership AND verify stack write permissions
- Apply the principle of least privilege - default deny unless explicitly permitted

## Variant hunting
Check for similar IDOR vulnerabilities in other move/transfer operations (e.g., file sharing, calendar events)
Test other Nextcloud apps for missing destination authorization checks
Examine batch operations that move multiple items to see if authorization is checked per-item
Look for race conditions between ownership verification and actual move operation
Test moving items to deleted or archived stacks
Verify if users can move items to stacks they've been granted view-only access to

## MITRE ATT&CK
- T1190
- T1548

## Notes
This is a straightforward authorization bypass affecting a collaboration tool. The vulnerability requires low complexity to exploit - simply intercepting and modifying a single parameter. The impact is data integrity rather than confidentiality. Similar vulnerabilities are common in project management and collaboration platforms where resources are organized hierarchically and authorization checks are not consistently applied across operations.

## Full report
<details><summary>Expand</summary>

When moving a task to another deck a request is made to /apps/deck/cards/XXXX. in the request the destination stackId parameter is used. When a user changes the parameter to that of a stack not belonging to him the task is still added.

### PoC

Create a card:
```
POST /apps/deck/cards HTTP/1.1
[...]

{"title":"SOME_TEST","stackId":1,"type":"plain"}
```
Move the Card:
```
PUT /apps/deck/cards/13 HTTP/1.1
[...]

{"title":"SOME_TEST","description":"","stackId":2,"type":"plain","lastModified":1588755341,"lastEditor":null,"createdAt":1588755341,"labels":null,"assignedUsers":null,"attachments":null,"attachmentCount":null,"owner":"test1","order":999,"archived":false,"duedate":null,"deletedAt":0,"commentsUnread":0,"id":13,"overdue":0}
```

When now intercepting and changing the `stackId` to `6` (that of another user) the server responds with a `200 OK` and the card is added to the stack of the receiving user.

## Impact

Deck of other users can be polluted.  Missing authorization check.

</details>

---
*Analysed by Claude on 2026-05-24*
