# Phabricator Diffusion Unauthorized Mirror Deletion via Missing Access Controls

## Metadata
- **Source:** HackerOne
- **Report:** 38965 | https://hackerone.com/reports/38965
- **Submitted:** 2014-12-10
- **Reporter:** nullsub
- **Program:** Phabricator
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The DiffusionMirrorDeleteController in Phabricator's Diffusion application fails to enforce proper authorization checks before allowing mirror deletion. An unauthenticated or unprivileged guest user can delete repository mirrors by directly accessing the mirror deletion endpoint, even when denied access to the repository itself.

## Attack scenario
1. Attacker authenticates to Phabricator as a guest/unprivileged user with minimal permissions
2. Attacker discovers they lack access to a target repository through normal UI navigation (/diffusion/TEST/edit/)
3. Attacker constructs direct URL to mirror deletion endpoint: /diffusion/TEST/mirror/delete/1/
4. Attacker sends request to delete endpoint without being challenged by authorization logic
5. Mirror is successfully deleted due to missing permission validation in DiffusionMirrorDeleteController.php
6. Repository mirroring functionality is disrupted for legitimate users

## Root cause
DiffusionMirrorDeleteController.php does not implement proper authorization checks to verify user permissions before processing mirror deletion requests. The controller appears to trust that access control is enforced elsewhere, creating a security bypass through direct endpoint access.

## Attacker mindset
An attacker with limited privileges seeks to disrupt repository operations by enumerating administrative endpoints. By bypassing UI-level restrictions and accessing endpoints directly, they discover that backend controllers lack redundant authorization checks, enabling denial-of-service through resource deletion.

## Defensive takeaways
- Implement authorization checks in every controller action, not just UI entry points
- Use a centralized permission-checking mechanism applied consistently across all sensitive operations
- Verify user capabilities (canEdit, canAdmin, etc.) before processing deletions
- Apply principle of least privilege to all endpoints, including those accessed via direct URLs
- Conduct security testing on all administrative/destructive endpoints with unprivileged users
- Use framework-level access control decorators or middleware to prevent controller bypass
- Validate not only existence of resources but user's right to modify them

## Variant hunting
Check other DiffusionController actions for similar missing authorization (commit operations, push permissions, configuration changes)
Audit other Phabricator applications (Maniphest, Differential) for endpoint-level authorization bypass via direct URL access
Test other resource deletion endpoints (/mirror/delete/, /branch/delete/, /commit/delete/) with guest accounts
Verify whether parent class DiffusionController provides any authorization that subclass bypasses

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1134 - Access Token Manipulation
- T1526 - Exposure Through Query Parameters

## Notes
This is a classic broken access control vulnerability where authorization is only checked at the UI/routing layer rather than enforced at the controller/business logic layer. Direct endpoint access circumvents UI-level protections. The vulnerability demonstrates the importance of defense-in-depth: UI restrictions alone are insufficient without corresponding server-side authorization checks.

## Full report
<details><summary>Expand</summary>

I have succesfully reproduced this issue following these steps:
 
- Creating a repository with an administrator user
 
- Checking that my "guest" user hasn't access to the newly created repository:
 
  http://phabricator/diffusion/TEST/edit/
 
- However, the guest user does have access to delete the mirror:
 
  http://phabricator/diffusion/TEST/mirror/delete/1/
 
 You can review the lack of permission-checks in the file: applications/diffusion/controller/DiffusionMirrorDeleteController.php

</details>

---
*Analysed by Claude on 2026-05-24*
