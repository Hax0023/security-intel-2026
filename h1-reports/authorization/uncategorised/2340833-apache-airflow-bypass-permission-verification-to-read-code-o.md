# Apache Airflow: Authentication Bypass to Read Unauthorized DAG Source Code

## Metadata
- **Source:** HackerOne
- **Report:** 2340833 | https://hackerone.com/reports/2340833
- **Submitted:** 2024-01-31
- **Reporter:** timon8
- **Program:** Apache Airflow
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Broken Access Control, Information Disclosure, Authorization Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
Apache Airflow versions before 2.8.1 allow authenticated users to bypass permission verification and access source code of DAGs they are not authorized to view. This information disclosure vulnerability requires valid authentication credentials but no elevated privileges to exploit.

## Attack scenario
1. Attacker authenticates to Apache Airflow with a regular user account
2. Attacker identifies the name or ID of a DAG they should not have access to
3. Attacker crafts a direct API request or constructs a URL to access the DAG source code endpoint
4. Permission verification logic fails to properly validate user authorization for that specific DAG
5. Attacker receives the source code of the restricted DAG, exposing business logic and potentially sensitive information
6. Attacker could use exposed code to identify further vulnerabilities or extract hardcoded credentials

## Root cause
Insufficient authorization checks in the DAG source code retrieval endpoint. The application likely validates that a user is authenticated but fails to verify they have explicit permission to view a specific DAG's code before returning it.

## Attacker mindset
Lateral information gathering - an authenticated user seeks to access resources beyond their privilege level to understand other workflows, extract business logic, or find security weaknesses in other teams' DAGs.

## Defensive takeaways
- Implement role-based access control (RBAC) checks at the endpoint level for all DAG-related operations
- Verify user permissions before returning any DAG metadata or source code, not just at the page load level
- Use consistent authorization framework across all API endpoints and code retrieval paths
- Log and audit access attempts to DAG source code for compliance and security monitoring
- Apply principle of least privilege - restrict DAG visibility by default unless explicitly granted
- Perform security testing on all API endpoints with various user roles and permission levels

## Variant hunting
Check other DAG-related endpoints (execution logs, configurations, task details) for similar authorization bypasses
Test if unauthenticated users can access DAG code through alternative endpoints or API paths
Verify if the vulnerability exists in other code retrieval features (import errors, parsing results)
Test if cached or historical versions of DAGs bypass current permission checks
Check if direct file system access through path traversal can circumvent the authorization logic
Investigate if permissions are checked only at UI level but not at API/backend level

## MITRE ATT&CK
- T1190
- T1526
- T1557
- T1555
- T1087

## Notes
The vulnerability is classified as low severity because it requires prior authentication, limiting the attack surface. However, in multi-tenant or complex organizational deployments, this could be significant for lateral movement and information gathering. The fix in version 2.8.1 likely added proper permission checks at the DAG code retrieval point.

## Full report
<details><summary>Expand</summary>

Apache Airflow, versions before 2.8.1, have a vulnerability that allows an authenticated user to access the source code of a DAG to which they don't have access. This vulnerability is considered low since it requires an authenticated user to exploit it. Users are recommended to upgrade to version 2.8.1, which fixes this issue.

**Email form the project maintainer**
██████████

## Impact

Apache Airflow<2.8.1

</details>

---
*Analysed by Claude on 2026-05-24*
