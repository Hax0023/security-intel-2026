# Read-only User Can Modify Device Names in Admin Account via Organization ID Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 865115 | https://hackerone.com/reports/865115
- **Submitted:** 2020-05-03
- **Reporter:** error___404
- **Program:** Helium
- **Bounty:** not specified
- **Severity:** medium
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** uncategorised

## Summary
A read-only invited user can modify device names associated with an admin account by exploiting missing authorization validation on the device update endpoint. The attacker leverages the organization ID obtained from another request to escalate privileges and perform unauthorized modifications to resources outside their permission scope.

## Attack scenario
1. Attacker creates or obtains access to two accounts (A as admin, B as read-only invited user)
2. Account B is invited with read-only permissions to Account A's organization
3. Attacker initiates a device deletion request from Account B and intercepts it to extract the organization ID
4. Attacker adds a new device in their own account (B) and attempts to rename it
5. Attacker intercepts the device name update request during submission
6. Attacker modifies the request payload to inject the target organization ID from step 3, then submits the modified request which successfully updates the device name in Account A's organization

## Root cause
The application performs insufficient authorization validation on the device update endpoint. The API likely validates that the user is authenticated and checks basic resource existence, but fails to properly verify that the user has write permissions for the specific organization ID being modified. The endpoint accepts organization_id as a parameter without properly enforcing the user's role-based permissions against that specific organization.

## Attacker mindset
The attacker demonstrated methodical reconnaissance by examining multiple requests to identify organizational identifiers, then combined this knowledge with permission escalation logic. The approach shows understanding of how API endpoints handle authorization and the willingness to test parameter manipulation across organizational boundaries.

## Defensive takeaways
- Implement granular authorization checks on every modifiable resource endpoint, not just at the retrieval level
- Enforce role-based access control (RBAC) for all write operations with explicit permission validation against the target organization/resource
- Validate that the authenticated user's organization membership and role align with the organization_id parameter in every request
- Log and alert on cross-organization modification attempts
- Use security testing to verify authorization is enforced consistently across all CRUD operations
- Implement principle of least privilege by default-denying access unless explicitly permitted

## Variant hunting
Test all CRUD operations (create, read, update, delete) with read-only user accounts across different organization contexts
Attempt to modify resources in sibling organizations or organizations you have minimal access to
Fuzzing organization_id, user_id, and other identifiers in write operation payloads with values from other accounts
Test permission boundaries during account invitation with various role levels (read-only, editor, admin)
Check if similar authorization bypasses exist in other device management endpoints (firmware updates, settings, configurations)
Test cross-team or cross-workspace privilege escalation if multi-tenancy structures exist

## MITRE ATT&CK
- T1190
- T1548
- T1566

## Notes
This is a classic horizontal and vertical privilege escalation vulnerability. The fix requires the backend to validate that the authenticated user has the appropriate permissions (write access) to the organization_id being modified, not just that they are authenticated. The vulnerability demonstrates how parameter tampering combined with weak authorization checks can lead to unauthorized modifications. The attack is relatively simple to execute once the organization ID is discovered, making this a high-impact, low-complexity vulnerability.

## Full report
<details><summary>Expand</summary>

Invited user with only the read-only permission can change the device name in admin account

1.create two account 'A 'and 'B ' in  console.helium
2.Invited the account 'B' with 'A' by giving the read-only permission
3.In account 'B' trying to delete the organization created by admin account 'A' and intercept the request then you got the organization id in request
4.Then in account 'B' add the device name and click on it and update the name which you want to display in the admin account(victim account)
5.And intercept the request while clicking the update button
6.In the request add the organization id which you got in step 3
7.then forward the request then the device name in admin account will be changed

## Impact

attacker with only the read-only permission can change the device name in the admin account

</details>

---
*Analysed by Claude on 2026-05-24*
