# Unauthorized Access to Payment Gateways API Endpoint via Broken Access Control

## Metadata
- **Source:** HackerOne
- **Report:** 96908 | https://hackerone.com/reports/96908
- **Submitted:** 2015-10-30
- **Reporter:** brakhane
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Broken Access Control, Unauthorized Information Disclosure, Privilege Escalation, API Authorization Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An administrator lacking the 'Settings' permission could access the payment gateways endpoint via direct API call, bypassing UI-level access controls. The REST API endpoint `/admin/payment_gateways.json` failed to enforce proper authorization checks, allowing unauthorized information disclosure of sensitive payment gateway configurations.

## Attack scenario
1. Attacker with administrative access but without 'Settings' permission attempts to view payment gateways through the admin UI
2. UI correctly denies access and does not display payment gateway information
3. Attacker discovers or guesses the REST API endpoint `/admin/payment_gateways.json`
4. Attacker makes direct HTTP GET request to the endpoint with their existing authentication token
5. API endpoint processes request without verifying 'Settings' permission requirement
6. Endpoint returns complete payment gateway configuration data to unprivileged administrator

## Root cause
Authorization checks were implemented at the UI/view layer but not enforced at the API endpoint layer. The backend API endpoint failed to validate that the authenticated user possessed the required 'Settings' permission before returning sensitive data. This represents inconsistent security implementation between frontend and backend components.

## Attacker mindset
A disgruntled employee or contractor with limited admin privileges could systematically probe API endpoints to discover information they shouldn't access. Once the UI denies access, probing the corresponding JSON endpoint is a natural escalation technique. The attacker seeks to gather payment processing information for competitive intelligence, fraud, or other malicious purposes.

## Defensive takeaways
- Implement authorization checks at the API/controller layer, not just in UI/view rendering logic
- Use consistent permission validation across all endpoints serving the same resource
- Apply principle of least privilege - ensure all API endpoints validate user permissions before returning data
- Conduct security testing on both UI and direct API access paths separately
- Use centralized authorization middleware/decorators to enforce permissions consistently
- Document all API endpoints and their required permissions explicitly
- Implement automated tests that verify permission enforcement on API endpoints
- Review all `.json` endpoints for similar authorization bypass vulnerabilities

## Variant hunting
Check other `.json` API endpoints for missing permission validation (e.g., `/admin/settings.json`, `/admin/staff.json`)
Test whether similar permissions (Accounts, Products, Orders) are enforced on their respective API endpoints
Probe for other admin endpoints that might be accessible through direct API calls despite UI restrictions
Test deprecated or undocumented API endpoints for authorization bypass
Check if permission bypass exists for other administrative roles beyond administrators
Examine `/admin/api/graphql` for similar authorization gaps in payment gateway queries

## MITRE ATT&CK
- T1190
- T1548
- T1526
- T1087

## Notes
This is a classic example of authorization being implemented inconsistently across application layers. The vulnerability demonstrates that security must be enforced at trust boundaries (API endpoints) rather than relying on UI-level restrictions. The attacker's authentication was valid - the issue was lack of proper authorization (permission check) at the resource level. This type of vulnerability is common when API endpoints are added or modified without security review, or when authorization logic is not centralized.

## Full report
<details><summary>Expand</summary>

Description
====
An administrator who lacks the 'Settings' permission is not able to see the shops payment gateways through the UI.  But the endpoint `shop.myshopify.com/admin/payment_gateways.json` does disclose payment gateways to the unprivileged user.

Mitigation
====
Restrict the endpoint in question to be only accessible with the correct permission set.

</details>

---
*Analysed by Claude on 2026-05-24*
