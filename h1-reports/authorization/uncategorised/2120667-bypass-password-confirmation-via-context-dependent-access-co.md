# Bypass password confirmation via Context-dependent access control (CDCA) in Nextcloud Workflow Engine

## Metadata
- **Source:** HackerOne
- **Report:** 2120667 | https://hackerone.com/reports/2120667
- **Submitted:** 2023-08-22
- **Reporter:** st0nzy
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Broken Access Control, Missing Authentication, Context-Dependent Access Control Bypass
- **CVEs:** CVE-2023-49791
- **Category:** uncategorised

## Summary
A context-dependent access control bypass vulnerability exists in Nextcloud's workflow engine where password confirmation required for sensitive operations via the web UI can be bypassed by directly calling the OCS API endpoint. An authenticated attacker can delete workflows without providing password confirmation by sending a DELETE request to /ocs/v2.php/apps/workflowengine/api/v1/workflows/user/{id}.

## Attack scenario
1. Attacker logs into Nextcloud instance and authenticates successfully
2. Attacker navigates to /nextcloud/index.php/settings/user/workflow to identify target workflow IDs
3. Attacker observes that the UI requires password confirmation for deletion operations
4. Attacker bypasses the UI restriction by directly calling the OCS API endpoint DELETE /ocs/v2.php/apps/workflowengine/api/v1/workflows/user/{workflow_id}?format=json
5. Attacker successfully deletes the workflow without providing password confirmation
6. Administrative workflow configurations are modified/deleted without proper authentication verification

## Root cause
Insufficient authentication verification in the OCS API endpoint for workflow deletion. The API endpoint does not enforce the same password confirmation requirement that exists in the web UI, allowing direct API calls to bypass the CDCA security mechanism.

## Attacker mindset
An authenticated user seeks to perform privileged actions (deleting workflows) that the application flags as sensitive (requiring password confirmation). The attacker recognizes that multiple code paths exist (web UI vs API) and tests whether security controls are consistently applied across all access points.

## Defensive takeaways
- Implement password confirmation verification at the API layer, not just the UI layer
- Ensure all sensitive operations require re-authentication regardless of the endpoint or request type used
- Apply consistent security controls across all access paths (web UI, API, OCS endpoints)
- Validate authentication context at the service layer rather than only at presentation layer
- Implement server-side checks to verify sensitive operations include proper confirmation tokens
- Audit all API endpoints for similar CDCA bypass vulnerabilities
- Consider implementing confirmation tokens that must be passed with sensitive requests

## Variant hunting
Check other Nextcloud API endpoints for similar password confirmation bypasses
Test other OCS v2 API endpoints that require sensitive confirmations in the UI
Examine if other delete/modify operations in /apps endpoints bypass CDCA
Test WebDAV endpoints for workflow-related operations
Check if the bypass applies to other user-modifiable resources beyond workflows

## MITRE ATT&CK
- T1190
- T1548
- T1562

## Notes
This is a classic example of broken access control where security controls are applied inconsistently across different access paths. The vulnerability requires prior authentication but allows circumvention of an additional security confirmation step. The report lacks specific Nextcloud version information and impact severity assessment. No remediation details provided by researcher.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi Team,
After some testing in nextcloud server, i found  Context-dependent access control when i delete workflow at ``` /nextcloud/index.php/settings/user/workflow ``` the server ask for password confirmation but it can be bypassed if i directly request the delete endpoint.

CDCA is a security mechanism that restricts access to resources based on the context of the request. If CDCA is broken, an attacker can exploit this flaw to gain unauthorized access to resources. This can have serious consequences, such as data breaches, theft of credentials, and denial of service attacks.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

- go to /nextcloud/index.php/settings/user/workflow and create workflow.

{F2626834}

- now click on Delete button, the Password require for confirmation

{F2626842}

- A Broken Context-dependent access control happen when user can bypass password confirmation by send the folowing request 

``` DELETE /nextcloud/ocs/v2.php/apps/workflowengine/api/v1/workflows/user/3?format=json```

{F2626845}

- as you can see, user bypass password confirmation and the workflow succssufilly deleted.

{F2626858}

## Supporting Material/References:

https://www.geeksforgeeks.org/how-to-prevent-broken-access-control

## Impact

bypass password confirmation

delete workflow without password confirmation

</details>

---
*Analysed by Claude on 2026-05-24*
