# Improper Authorization Allows Editor to Toggle Admin-Only Workspace Features

## Metadata
- **Source:** HackerOne
- **Report:** 3371448 | https://hackerone.com/reports/3371448
- **Submitted:** 2025-10-05
- **Reporter:** longlivedoma
- **Program:** Lovable AI
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Improper Authorization, Vertical Privilege Escalation, Missing Server-Side Role Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
An Editor-role user can call the `/workspaces/<WORKSPACE_ID>/tool-preferences/ai_gateway/enable` API endpoint to disable the Lovable AI feature, which should be restricted to Admin/Owner roles only. The backend fails to enforce role-based access control, allowing a lower-privileged user to toggle an admin-only workspace setting and disrupt AI functionality for all workspace members.

## Attack scenario
1. Attacker creates or joins a workspace with Editor role privileges
2. Attacker observes the Admin disabling the Lovable AI feature and captures the POST request to `/tool-preferences/ai_gateway/enable`
3. Attacker modifies the captured request to use their own Editor JWT token instead of the Admin token
4. Attacker sends the modified request with Editor credentials, which is accepted by the server
5. The Lovable AI feature is disabled workspace-wide despite the attacker lacking authorization
6. All workspace members lose access to AI-driven features, prompt integrations, and content generation capabilities

## Root cause
The backend API endpoint `/workspaces/<WORKSPACE_ID>/tool-preferences/ai_gateway/enable` lacks server-side role-based access control validation. The application trusts the client to enforce authorization restrictions and does not verify that only Admin/Owner-role users can modify this setting before processing the request.

## Attacker mindset
An Editor-role user seeking to sabotage or disrupt workspace operations discovers that authorization checks are missing on critical admin endpoints. They recognize that by replaying an admin's API request with their own credentials, they can toggle features intended to be admin-exclusive, enabling denial-of-service or disruption attacks against the entire workspace without detection.

## Defensive takeaways
- Implement server-side role-based access control (RBAC) checks on all sensitive endpoints, verifying user role before processing requests
- Validate authorization at the application layer, not relying on client-side enforcement or token presence alone
- Use a consistent authorization framework across all API endpoints handling privileged operations
- Log and alert on authorization failures and role-based access attempts by lower-privileged users
- Conduct security code review of endpoints that modify workspace-level or organization-wide settings
- Implement automated testing that verifies each endpoint correctly rejects requests from unauthorized roles
- Apply principle of least privilege: Editor role should only have permissions to edit content, not modify feature flags

## Variant hunting
Search for other endpoints handling workspace feature toggles, preference settings, or configuration changes. Test all admin-panel endpoints with Editor/Viewer tokens. Check for similar issues in billing settings, member management, security policies, data retention settings, integration toggles, and plugin management endpoints. Look for patterns where role validation is missing from POST/PUT/DELETE endpoints modifying workspace-level resources.

## MITRE ATT&CK
- T1190
- T1548
- T1078

## Notes
This is a straightforward broken access control vulnerability with high practical impact. The fix is straightforward but critical: add role validation on the backend. The attacker requires valid workspace membership but only Editor privileges, making exploitation low-friction. The impact is workspace-wide denial of service affecting all members' access to AI features.

## Full report
<details><summary>Expand</summary>

## Summary:
An account with the Editor role can successfully call the API endpoint `/workspaces/<WORKSPACE_ID>/tool-preferences/ai_gateway/enable`that disables workspace-wide admin-only feature (Lovable AI). The API does not enforce server-side role checks for this action, allowing a vertical privilege escalation (Broken Access Control).

## Steps To Reproduce:

Preconditions

- Two accounts are members of the same workspace `Victim-Workspace`:

    - Account A (Owner/Admin) - Owner role in `Victim-Workspace`.
    - Account B (Editor) - Editor role in the same `Victim-Workspace`.

1. Sign in as Account A (Admin) and toggle the AI feature off inside the workspace.

2. Capture this endpoint (Responsible for Disabling AI Feature).

```HTTPS
POST /workspaces/<WORKSPACE_ID>/tool-preferences/ai_gateway/enable HTTP/2
Host: lovable-api.com
Authorization: Bearer <OWNER-TOKEN>
Content-Type: application/json


{"approval_preference":"disable"}
```
Note: <WORKSPACE_ID> is the workspace id for Victim-Workspace.

4. Modify request to use Editor JWT Token
- Replace the Authorization header with Account B (Editor) JWT:

```HTTPS
POST /workspaces/<WORKSPACE_ID>/tool-preferences/ai_gateway/enable HTTP/2
Host: lovable-api.com
Authorization: Bearer <EDITOR_JWT>
Content-Type: application/json

{"approval_preference":"disable"}
```

5. When the request is sent again with the Editor's JWT , the request succeeds and the Lovable AI setting is switched off for the workspace.

## Proof of Concept: 

{F4859179}

## Impact

Based on the Lovable AI documentation, this feature powers all the AI-driven parts of a workspace like prompt integrations, content generation, and other model-based actions.

If an Editor disables it, all those AI features stop working across the workspace, breaking functionality for every member. Since only admins are supposed to control this setting, the bug lets an unauthorized user disrupt how the workspace operates and remove core features that teams rely on.

</details>

---
*Analysed by Claude on 2026-05-24*
