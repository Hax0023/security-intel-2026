# Unauthorized Managed Store Creation via Permission Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1167753 | https://hackerone.com/reports/1167753
- **Submitted:** 2021-04-18
- **Reporter:** jmp_35p
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Access Control, Insufficient Permission Validation, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A staff member with limited permissions to manage development stores (add, archive, unarchive only) can exploit an unprotected API endpoint to create new managed stores without proper authorization. The endpoint /organizationID/stores/create_managed_store lacks adequate permission checks, allowing privilege escalation beyond the intended scope.

## Attack scenario
1. Attacker identifies that they have been granted limited store management permissions (development store operations only)
2. Attacker discovers the POST endpoint /organizationID/stores/create_managed_store is accessible with their current credentials
3. Attacker crafts a POST request with JSON payload containing store configuration and permissions array
4. Attacker sends the request with valid CSRF token and session credentials
5. Server processes the request without verifying if the user has permission to create managed stores specifically
6. New managed store is created, granting attacker capabilities beyond their intended permission scope

## Root cause
The backend API endpoint for creating managed stores performs insufficient authorization checks. The system validates that a user is logged in and has some store-related permissions, but fails to verify the specific permission required for managed store creation. The endpoint likely checks for a broad 'store_management' permission rather than verifying the explicit 'create_managed_store' permission.

## Attacker mindset
An insider with legitimate staff access explores permission boundaries to identify gaps. They notice they can access the create_managed_store endpoint despite lacking explicit permission grants, indicating permission checks are not granular enough. They attempt to exploit this by directly calling the API endpoint.

## Defensive takeaways
- Implement explicit permission checks for each privileged action rather than relying on broad permission categories
- Separate development store operations from managed store operations with distinct permission nodes
- Validate permissions at the API endpoint level before processing requests, not just at the UI level
- Conduct permission matrix audit to ensure action-to-permission mappings are correctly enforced
- Use allowlist approach for API endpoints accessible to different permission levels
- Log and monitor creation of managed stores to detect unauthorized attempts
- Consider implementing role-based access control (RBAC) with explicit grant/deny rules

## Variant hunting
Check if other /organizationID/stores/* endpoints have similar permission bypass issues (archive, unarchive, delete operations)
Test if the collaborator_access_code parameter can be modified to grant additional permissions
Verify if the permissions array in the JSON payload is validated server-side or if it can be manipulated
Check if other API endpoints for resource creation (applications, extensions, etc.) have similar permission validation gaps
Test if staff with different permission combinations can bypass other protected operations
Verify if the endpoint properly validates the store_domain parameter against organization scope

## MITRE ATT&CK
- T1190
- T1548
- T1078

## Notes
Reporter mentions potential relationship to issue #1167453, suggesting this may be part of a broader permission validation pattern in the codebase. The specific organization ID (100808) used in the example should be replaced with actual org ID during testing. The endpoint requires CSRF token but lacks proper authorization logic, representing a classic broken access control vulnerability. The inclusion of collaborator_access_code parameter being empty suggests it may be optional, which could indicate incomplete validation logic.

## Full report
<details><summary>Expand</summary>

Details
A staff member who has permission to add, archive and unarchive development stores as shown in managedStoreA.png  can also add new managed stores. I can't tell if the issue I pointed out in #1167453 has the same root cause as this. A staff member with the said permission can access /organizationID/stores/create_managed_store endpoint as seen in managedStoreB.png. The POST request below can be used to reproduce the described issue.

```
POST /100808/stores/create_managed_store HTTP/1.1
Host: partners.shopify.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:86.0) Gecko/20100101 Firefox/86.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://partners.shopify.com/100808/stores/new?store_type=managed_store
Content-Type: application/json
X-Requested-With: XMLHttpRequest
X-CSRF-Token: ...

{"message":"","permissions":["applications","customers","dashboard","domains","draft_orders","edit_orders","gift_cards","links","locations","marketing","marketing_section","orders","overviews","pages","products","reports","themes","preferences","view_shopify_payments_payouts","view_billing_details","view_private_apps","edit_private_apps"],"store_domain":"myStore1","collaborator_access_code":""}

```

## Impact

Staff member can perform action that requires permission

</details>

---
*Analysed by Claude on 2026-05-24*
