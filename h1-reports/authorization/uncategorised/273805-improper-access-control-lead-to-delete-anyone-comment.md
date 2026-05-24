# Improper Access Control Allows Unauthorized Comment Deletion

## Metadata
- **Source:** HackerOne
- **Report:** 273805 | https://hackerone.com/reports/273805
- **Submitted:** 2017-10-02
- **Reporter:** ranjit_p
- **Program:** Unknown/Private Program
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Improper Access Control, Broken Object Level Authorization, Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application fails to verify comment ownership before allowing deletion, permitting any authenticated user to delete comments created by other users. The vulnerability exists in the comment deletion endpoint which does not validate that the requesting user is the comment's original creator.

## Attack scenario
1. Attacker logs into the application with their account
2. Attacker identifies a comment created by another user in the blog comments section
3. Attacker navigates to the comment management interface at /blog/comments
4. Attacker selects the victim's comment and clicks 'Hide Comment' to unapprove it
5. Attacker proceeds to delete the hidden comment without authorization checks
6. The system successfully deletes the comment despite the attacker not being the original creator

## Root cause
The backend comment deletion handler lacks ownership verification logic. The application only validates that a comment exists and can be deleted by its ID, without cross-referencing the current user's identity against the comment's creator field before processing the deletion request.

## Attacker mindset
Malicious user seeking to suppress, censor, or sabotage other users' contributions by removing their comments without administrative privileges. Could be used for competitive interference, harassment, or content manipulation.

## Defensive takeaways
- Implement authorization checks on all state-modifying operations by verifying user identity against resource ownership
- Use role-based access control (RBAC) where admins can delete any comment, but users can only delete their own
- Validate that the authenticated user ID matches the comment creator ID before processing deletions
- Add audit logging for all comment deletions including who deleted what and when
- Consider implementing soft-deletes (marking as deleted) rather than permanent removal for audit trails
- Apply consistent access control validation across all comment operations (delete, edit, hide, unhide)
- Implement principle of least privilege - deny by default unless explicitly authorized

## Variant hunting
Check comment editing functionality for similar authorization bypass
Test comment approval/unapproval endpoints for IDOR vulnerabilities
Verify user profile/account deletion doesn't have similar authorization issues
Examine blog post deletion and modification endpoints
Test whether users can modify comment content belonging to others
Check if comment restoration/recovery functions have the same flaw
Investigate other content management endpoints (articles, replies, etc.) for authorization bypass patterns

## MITRE ATT&CK
- T1190
- T1021
- T1078

## Notes
This is a classic broken object-level authorization (BOLA) vulnerability affecting data integrity. The fix is straightforward - add server-side ownership validation before deletion. The writeup demonstrates good vulnerability reporting with clear reproduction steps, though the URL referenced (localhost:8080) suggests this may be from a private or test program. Severity is medium rather than high because the impact is limited to comment deletion with potential for abuse through harassment or censorship rather than credential compromise or data exfiltration.

## Full report
<details><summary>Expand</summary>

SUMMURY
========================
Here server dont check the owner of any comment.
During Comment deletion it does not check whether the comment is  created by user or not.
so i can delete a comment of others user.

STEP TO REPRODUCE
=======================
1. goto https://localhost:8080/blog/comments .

2. select any commnet which is already aproved.

3.Unaprove it by clicking "Hide Comment".

4. Now delete that commnet and see comment is deleted which is not created by himself.

FIX
========
implement proper access control mechanism so that when user try to delete a comment first check the comment is belongs to that user or not.

</details>

---
*Analysed by Claude on 2026-05-24*
