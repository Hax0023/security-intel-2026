# Improper Access Control in BuddyPress Core Allows Reply/Delete Any User's Activity

## Metadata
- **Source:** HackerOne
- **Report:** 837256 | https://hackerone.com/reports/837256
- **Submitted:** 2020-04-02
- **Reporter:** hoangkien1020
- **Program:** BuddyPress
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Insecure Direct Object References (IDOR)
- **CVEs:** None
- **Category:** uncategorised

## Summary
BuddyPress core lacks proper access control validation when replying to or deleting user activities, allowing attackers to modify or delete activities from groups they haven't joined by directly referencing activity IDs. An authenticated attacker can capture legitimate requests and modify activity identifiers to perform unauthorized actions on arbitrary user activities across different groups.

## Attack scenario
1. Attacker creates account and joins or observes public groups to gather valid activity IDs
2. Attacker performs a legitimate reply or delete action on their own activity in a group they belong to
3. Attacker intercepts the HTTP request using a proxy tool (e.g., Burp Suite)
4. Attacker modifies the activity ID parameter to target a victim's activity from a different group
5. Attacker replays the modified request, bypassing access control checks
6. System processes request and allows unauthorized reply/deletion of victim's activity without membership validation

## Root cause
BuddyPress fails to validate whether the authenticated user has proper group membership and permissions before allowing activity modifications. The application likely uses only the activity ID as the authorization parameter without cross-referencing group membership, role, or activity ownership, creating an IDOR vulnerability.

## Attacker mindset
An authenticated user seeks to disrupt community discussions or damage reputation by vandalizing other users' activities without detection. The attacker recognizes that direct object reference attacks bypass business logic checks and exploits the assumption that group membership restricts access.

## Defensive takeaways
- Implement multi-factor access control: verify user authentication, group membership, and appropriate role before allowing activity modifications
- Use indirect object references (tokens/hashes) instead of sequential IDs for sensitive operations
- Enforce authorization checks at API/controller level for all activity operations (reply, delete, edit)
- Validate group membership context for every activity request, not just presence of activity ID
- Implement rate limiting and audit logging for activity modifications to detect suspicious patterns
- Add permission checks that validate user role within the specific group (admin, moderator, member)
- Use capability-based access control system where permissions are verified before database operations

## Variant hunting
Check edit/update operations on activities for similar IDOR vulnerabilities
Test other group-based features (documents, photos, messages) for group membership validation bypasses
Verify whether the vulnerability extends to private groups or restricted content
Examine activity permission checks when activities are shared across multiple groups
Test whether the vulnerability allows cross-group activity visibility beyond just modification
Investigate related BuddyPress components like notifications and activity streams for similar issues

## MITRE ATT&CK
- T1190
- T1557
- T1555

## Notes
This is a classic IDOR vulnerability in a community platform context. The severity is high because it allows unauthorized content modification and deletion affecting user-generated content integrity. The attack requires only network-level interception tools and an active account. Public groups increase exposure as attackers can easily discover valid activity IDs. The vulnerability likely affects production environments where activity IDs are predictable or enumerable.

## Full report
<details><summary>Expand</summary>

## Description:

Improper Access Control in Buddypress core allows reply,delete any user's activity in other public group,which they don't join.

## Steps To Reproduce:
Step 1: Create two account A, B with two public groups
Step 2: In group A-account A, create a new activity [id_A]
Step 3: In group B-account B, create a new activity [id_B]
Step 4: In group A-account A select reply/delete action, use proxy to capture this request
Step 5: Change id_A by id_B
Step 6: Done, you deleted or reply user's activity without joining group
## Recommendations
Valid access control with their roles 

PoC with video

## Impact

Attacker without joining to group performs to reply,delete any activities without permission.

</details>

---
*Analysed by Claude on 2026-05-24*
