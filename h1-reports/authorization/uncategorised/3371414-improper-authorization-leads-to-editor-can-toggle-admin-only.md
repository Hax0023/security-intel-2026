# Improper Authorization Leads to Editor can toggle admin-only workspace features

## Metadata
- **Source:** HackerOne
- **Report:** 3371414 | https://hackerone.com/reports/3371414
- **Submitted:** 2025-10-05
- **Reporter:** longlivedoma
- **Program:** Lovable Cloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Improper Authorization, Vertical Privilege Escalation, Missing Server-Side Role Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
An Editor-role user can call admin-only API endpoints to disable workspace-wide Lovable Cloud features due to missing server-side authorization checks. This allows a non-admin user to toggle critical infrastructure features, causing potential workspace-wide outages affecting all users and projects.

## Attack scenario
1. Attacker creates or joins a workspace with an Editor role account
2. Attacker observes or intercepts an admin disabling Lovable Cloud feature via POST /workspaces/<ID>/tool-preferences/supabase/enable
3. Attacker replaces the admin JWT in the request with their own Editor JWT token
4. Attacker sends the modified request with Editor credentials
5. API accepts the request without validating the Editor's role authorization
6. Lovable Cloud feature is disabled, causing service disruption for all workspace members

## Root cause
The API endpoint `/workspaces/<WORKSPACE_ID>/tool-preferences/supabase/enable` performs client-side or insufficient authorization checks, relying on JWT authentication alone without validating the user's role/permissions on the server-side before allowing the action.

## Attacker mindset
A disgruntled Editor user or competitor with workspace access seeks to disrupt operations by disabling critical infrastructure. The attack requires minimal effort—simple JWT substitution—making it an attractive low-effort attack vector.

## Defensive takeaways
- Implement mandatory server-side role/permission validation for all privileged operations, not just authentication
- Apply role-based access control (RBAC) checks before processing admin-only endpoints
- Use attribute-based access control (ABAC) to enforce granular permissions tied to workspace roles
- Audit all API endpoints for missing authorization checks, particularly those affecting workspace-wide settings
- Log and monitor privilege escalation attempts and authorization failures
- Enforce least privilege principle—Editor role should never have access to toggle infrastructure features
- Implement API gateway or middleware for consistent authorization enforcement across all endpoints

## Variant hunting
Check other `/tool-preferences/*` endpoints for similar authorization bypasses
Audit all workspace-level configuration endpoints for missing role checks
Test other admin-only features (billing, member management, integrations) with Editor JWT
Examine other API endpoints handling critical infrastructure toggles across different modules
Review all POST/PUT/DELETE operations on workspace resources for authorization validation gaps
Test horizontal privilege escalation (Editor accessing Admin resources in different workspaces)

## MITRE ATT&CK
- T1190
- T1548
- T1134

## Notes
The vulnerability represents a classic broken access control issue where authentication (JWT validation) is present but authorization (role checking) is absent. The impact is severe due to the critical nature of the affected feature (database, auth, storage, serverless functions). The fix requires adding server-side role validation before processing the request, likely a simple conditional check on the user's workspace role.

## Full report
<details><summary>Expand</summary>

## Summary:
An account with the Editor role can successfully call the API endpoint `/workspaces/<WORKSPACE_ID>/tool-preferences/supabase/enable` that disables workspace-wide admin-only features (Lovable Cloud). The API does not enforce server-side role checks for this action, allowing a vertical privilege escalation (Broken Access Control).

## Steps To Reproduce:

Preconditions

- Two accounts are members of the same workspace `Victim-Workspace`:

    - Account A (Owner/Admin) - Owner role in `Victim-Workspace`.
    - Account B (Editor) - Editor role in the same `Victim-Workspace`.

1. Sign in as Account A (Admin) and toggle the Cloud feature off inside the workspace.

2. Capture this endpoint (Responsible for Disabling Cloud Feature).

```HTTPS
POST /workspaces/<WORKSPACE_ID>/tool-preferences/supabase/enable HTTP/2
Host: lovable-api.com
Authorization: Bearer <OWNER-JWT>
Content-Type: application/json


{"approval_preference":"disable"}
```
Note: <WORKSPACE_ID> is the workspace id for Victim-Workspace.

4. Modify request to use Editor JWT Token
- Replace the Authorization header with Account B (Editor) JWT:

```HTTPS
POST /workspaces/<WORKSPACE_ID>/tool-preferences/supabase/enable HTTP/2
Host: lovable-api.com
Authorization: Bearer <EDITOR_JWT>
Content-Type: application/json

{"approval_preference":"disable"}
```

5. When the request is sent again with the Editor's JWT , the request succeeds and the Lovable Cloud setting is switched off for the workspace.

## Proof of Concept :

{F4859059}

## Impact

An Editor can disable the Lovable Cloud feature, which powers the workspace’s backend as mentioned in documentation (database, auth, storage, and serverless functions).
This can lead to workspace-wide downtime and broken functionality for all projects and users, making the impact High due to the potential service disruption and business damage.

</details>

---
*Analysed by Claude on 2026-05-24*
