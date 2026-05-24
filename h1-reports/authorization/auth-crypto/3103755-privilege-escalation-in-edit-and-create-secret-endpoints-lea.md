# Privilege Escalation in Edit and Create Secret Endpoints Leads to Unauthorized Secret Modification

## Metadata
- **Source:** HackerOne
- **Report:** 3103755 | https://hackerone.com/reports/3103755
- **Submitted:** 2025-04-22
- **Reporter:** 0xsom3a
- **Program:** Dust
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Privilege Escalation, Broken Access Control, Insecure Direct Object References (IDOR), Unauthorized Data Modification
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A user with the Builder role can enumerate all secret names in a workspace, create new secrets, and silently overwrite existing secrets by reusing their names, violating permission boundaries. This privilege escalation vulnerability allows unauthorized tampering with sensitive configurations, API keys, and credentials used throughout the workspace. The lack of proper role-based access control on secret management endpoints enables an attacker to compromise application integrity and potentially escalate to higher privileges.

## Attack scenario
1. Attacker with Builder role authenticates to the workspace and gains initial session access
2. Attacker sends GET request to /api/w/[workspace_id]/dust_app_secrets to enumerate all existing secret names without viewing values
3. Attacker identifies critical secrets (e.g., API_KEY, DATABASE_CREDENTIALS, AUTH_TOKEN) used by admin users or sensitive applications
4. Attacker crafts POST request to create/overwrite secret with same name as existing critical secret, replacing legitimate value with malicious payload
5. Legitimate users and applications unknowingly use the compromised secret, leading to data theft, unauthorized access, or lateral movement
6. Attacker repeats process to compromise multiple secrets across workspace, establishing persistent access and control

## Root cause
The application implements insufficient role-based access control (RBAC) on secret management endpoints. The POST endpoint for creating/updating secrets lacks proper authorization checks to verify if the requesting user's Builder role has permission to modify secrets. The GET endpoint exposes secret names without enforcing role restrictions. The API silently overwrites existing secrets without requiring additional confirmation or admin approval, further bypassing security controls.

## Attacker mindset
An insider threat or compromised Builder account would systematically enumerate secrets to identify high-value targets. The attacker would methodically overwrite critical secrets used in sensitive workflows, either to establish persistence, exfiltrate data, or disrupt operations. The silent overwrite behavior is exploited as a feature—no audit trail or warning alerts defenders to the tampering.

## Defensive takeaways
- Implement strict role-based access control (RBAC) on all secret management endpoints; Builder role should have zero permissions on secrets API
- Enforce principle of least privilege: only Admin/Owner roles should list, create, read, or modify secrets
- Require explicit confirmation and optional approval workflows for secret modification operations, especially overwrites of existing secrets
- Audit and log all secret access attempts and modifications with full context (user, role, timestamp, action, old/new values)
- Separate read and write endpoints; never allow simultaneous list + modify permissions for non-admin roles
- Implement rate limiting on secret creation/modification endpoints to detect batch operations
- Use content security policies to prevent secrets from being transmitted to untrusted contexts
- Validate that secret names are not user-controllable for overwrite scenarios; use unique identifiers instead
- Implement secrets rotation and integrity verification mechanisms to detect tampering
- Conduct regular permission audits across all user roles to identify similar misconfigurations

## Variant hunting
Check if other sensitive resource endpoints (API keys, tokens, webhooks, integrations) have similar RBAC bypasses for non-admin roles
Test if Builder role can delete secrets or perform other write operations beyond creation/overwrite
Verify if the vulnerability extends to workspace-level settings, user management, or billing endpoints
Check for similar silent overwrite behavior in other create/update endpoints that should require confirmation
Test if unauthenticated or guest users can access secret enumeration endpoints
Investigate if secret names are predictable or follow patterns that facilitate targeted attacks
Review other workspace roles (Contributor, Viewer, etc.) for similar secret access violations
Test if bulk secret operations or import features have similar permission bypasses
Check if API endpoints for secrets differ in their permission checks compared to UI-based operations

## MITRE ATT&CK
- T1190
- T1548
- T1087
- T1078
- T1556
- T1552
- T1199

## Notes
This is a classic example of broken access control where authorization checks are either missing entirely or implemented inconsistently across endpoints. The vulnerability is particularly dangerous because secrets are foundational to application security—compromise of the secret management layer cascades into compromise of all downstream systems relying on those credentials. The silent overwrite behavior suggests no defensive monitoring was in place to detect suspicious secret modifications. The report demonstrates good reproduction steps and clear impact articulation, though specific program/bounty details were not provided in the source content.

## Full report
<details><summary>Expand</summary>

#Summary

A user with the **Builder** role — a role that is **not expected** to manage secrets — can:

- ✅ **List all existing secret names** in the workspace.
- ✅ **Create new secrets**.
- ✅ **Overwrite existing secrets** simply by using the same name.

This behavior **violates permission boundaries** and  leads to **privilege escalation**, **tampering with app configurations**, or **unauthorized access to sensitive data**.

---

# Steps to Reproduce

##Step-1 :  Get All Secret Names in the Workspace

As a **Builder**, send a `GET` request to the secrets endpoint to enumerate all existing secret names.

```http
GET /api/w/[workspace_id]/dust_app_secrets HTTP/2  
Host: dust.tt  
Cookie: [appSession]
```

This returns a list of secrets with their `id`, `name`, `created_at`, etc. — but without showing the secret `value`.

```json
{
  "secrets": [
    { "name": "NAME-1", "value": "•••••••" },
    { "name": "NAME-2", "value": "•••••••" }
  ]
}

```


##**Step-2 :** Create or Overwrite a Secret

Now, send a `POST` request to create a new secret.


```json
POST /api/w/[workspace_id]/dust_app_secrets HTTP/2  
Host: dust.tt  
Content-Type: application/json  
Cookie: [appSession]

{
  "name": "NAME-1",
  "value": "malicious-value"
}
```

#### Behavior:
- If the `name` used in the request **already exists** in the workspace (as returned from step 1), the system will **overwrite the existing secret's value**.
- If the `name` is **new**, a new secret will be created.

-  No error or warning is shown — overwrite happens silently.

---

#POC Video:

██████


---

# Expected Behavior

The **Builder** role should:

-  Not be able to access the list of secret names.
-  Not be able to create or update any secrets.

---

# Suggested Fix

- Enforce strict permission checks on all secret-related endpoints.
- Ensure only users with elevated roles (e.g., Admin, Owner) can list, create, or update secrets.

## Impact

This vulnerability allows users with the **Builder** role to:

-  Discover all secret names in the workspace.
-  Tamper with or overwrite secrets used by other users or apps.
-  Create new secrets and potentially trick other users into using them.
-  Escalate privileges by modifying secrets used in sensitive flows (e.g., API keys, tokens, credentials).

This could lead to:

- Configuration manipulation  
- Account compromise  
- Supply chain attacks on internal tooling  
- Loss of integrity of secret data

</details>

---
*Analysed by Claude on 2026-05-24*
