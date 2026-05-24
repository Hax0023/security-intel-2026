# Unauthorized Table Creation by Member in Restricted Data Spaces

## Metadata
- **Source:** HackerOne
- **Report:** 3101858 | https://hackerone.com/reports/3101858
- **Submitted:** 2025-04-20
- **Reporter:** mous_haxk
- **Program:** Unknown (HackerOne Report 3101858)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Insecure Direct Object References (IDOR), Client-Side Security Bypass, Missing Authorization Checks
- **CVEs:** None
- **Category:** uncategorised

## Summary
A member-level user can bypass UI restrictions to create tables in company data spaces designated for workspace builders only. The vulnerability exists because access control is enforced only on the frontend (disabled button), while backend API endpoints lack proper authorization validation. This allows lower-privileged users to manipulate organizational data structures despite lacking necessary permissions.

## Attack scenario
1. Attacker authenticates as a member user with limited permissions
2. Attacker navigates to a restricted data space (company database) where only builders should have write access
3. Attacker identifies the 'Add Data' button is visually disabled but analyzes the DOM/network requests
4. Attacker clicks the disabled button or directly calls the underlying API endpoint (bypassing frontend restrictions)
5. Attacker submits a table creation request with necessary parameters to the backend API
6. Backend processes the request without validating user role/permissions, creating the table successfully

## Root cause
Authorization checks are implemented exclusively at the UI layer (button disabled state) rather than on the backend API. The server-side endpoint for table creation does not validate whether the requesting user has the 'builder' role or write permissions to the target data space before processing the request.

## Attacker mindset
A disgruntled employee or opportunistic insider with member access looks to expand their capabilities. They observe UI restrictions but recognize these are cosmetic controls. By inspecting browser developer tools or intercepting network requests, they discover the backend API lacks corresponding permission checks and proceed to create unauthorized tables for data manipulation, sabotage, or reconnaissance.

## Defensive takeaways
- Implement server-side authorization checks for all sensitive operations before processing requests, regardless of UI state
- Validate user role and permissions on the backend API endpoint before allowing table creation in restricted data spaces
- Never rely solely on frontend controls (disabled buttons, hidden fields) to enforce security; these are user-experience measures, not security boundaries
- Use role-based access control (RBAC) framework consistently across all API endpoints with explicit permission validation
- Log and audit all table creation attempts, flagging requests from users lacking proper permissions
- Implement principle of least privilege: member users should not have access to endpoints that create data structures in admin-only spaces

## Variant hunting
Check for similar bypass vulnerabilities in other 'builder-only' features (delete space, modify permissions, export data, create dashboards)
Test if other member-restricted actions (modify workspace settings, manage users, change data space configurations) have the same frontend-only protection
Analyze if the API endpoint accepts alternative parameters or HTTP methods to create tables that frontend validation doesn't cover
Verify if role validation can be bypassed through header manipulation, token forgery, or request parameter tampering
Check for privilege escalation paths where a member could modify their own role/permissions through other endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (API endpoint exploitation)
- T1548 - Abuse Elevation Control Mechanism (bypassing authorization controls)
- T1078 - Valid Accounts (using legitimate member credentials)
- T1566 - Phishing (social engineering to learn about restricted spaces)
- T1087 - Account Discovery (enumerating accessible data spaces)

## Notes
This is a textbook example of insufficient authorization validation where frontend restrictions create a false sense of security. The vulnerability is straightforward to exploit and high-impact in collaborative data platforms where data integrity is critical. The report's recommendation to enforce server-side access control is correct and standard security practice. Organizations using this platform should immediately patch the backend API to validate user permissions before processing any data modification requests.

## Full report
<details><summary>Expand</summary>

## Summary:
A member user is able to create tables inside restricted company data spaces, despite the UI indicating that only workspace builders (admins) should be allowed. The “Add Data” button appears disabled in the UI, but it is still interactable and functional. Upon clicking it, the member can proceed to create and save a new table successfully.

## Steps To Reproduce:

1. Log in as a member user.
2. Navigate to the restricted data space where only builders should have write access.
3. Click the (visually disabled) “Add Data” button.
4. Select “Create Table.”
5. Fill in the required inputs and click “Save.”
6. Observe that the table is successfully created, despite the user lacking the proper permissions.

## Supporting Material/References:

█████████

## Impact

Unauthorized data manipulation by lower-privileged users. This could lead to data tampering, workspace clutter, or information leakage, depending on how the data is later handled and exposed.

**Recommendation:**  
Enforce access control server-side by validating user roles before allowing data creation. Never rely solely on front-end/UI restrictions to protect sensitive functionality.

</details>

---
*Analysed by Claude on 2026-05-24*
