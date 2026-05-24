# Lack of Access Control on Edit Packing Slip Template

## Metadata
- **Source:** HackerOne
- **Report:** 417839 | https://hackerone.com/reports/417839
- **Submitted:** 2018-10-02
- **Reporter:** fisher
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Authorization, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A staff user with minimal permissions (Home only) can access and modify the packing slip template endpoint (/admin/settings/packing_slip_template) that should be restricted to administrators only. This allows unauthorized users to alter order fulfillment documents, potentially redirecting shipments or exfiltrating sensitive data through Liquid template injection.

## Attack scenario
1. Attacker creates or compromises a staff account with minimal permissions (Home access only)
2. Attacker navigates to /admin/settings/packing_slip_template endpoint which should be admin-restricted
3. Attacker modifies the packing slip template to change shipping addresses to their own location
4. Attacker injects malicious Liquid code to exfiltrate order variables containing customer PII or financial data
5. Attacker saves changes which persist across all future orders
6. Legitimate admin reviews orders finding incorrect shipping addresses or discovers unauthorized template modifications

## Root cause
Missing or improperly implemented authorization checks on the packing slip template edit endpoint. The application validates that a user is authenticated but fails to verify they have sufficient permissions (admin role) before allowing access to sensitive configuration features.

## Attacker mindset
An insider threat or compromised staff account holder seeking to redirect merchandise, commit fraud, or exfiltrate customer data through template manipulation. The low barrier to entry (needing only basic staff access) makes this an attractive attack vector.

## Defensive takeaways
- Implement role-based access control (RBAC) checks on all administrative endpoints, not just authentication checks
- Require explicit admin permissions for any endpoint that modifies order processing, fulfillment, or customer data
- Use middleware or decorators to enforce authorization rules consistently across similar administrative features
- Audit Liquid template processing to prevent injection attacks and limit available variables in user-editable templates
- Log all template modifications with user identity for forensic analysis
- Test authorization with minimal-permission accounts during security testing phases
- Implement least-privilege principle for staff roles with granular permission controls

## Variant hunting
Check other /admin/settings/* endpoints for similar authorization bypasses
Review all Liquid template editing features (invoices, email templates, notification templates) for access control issues
Test other user-modifiable fulfillment-related settings with minimal-permission accounts
Inspect any endpoint allowing document or template generation/modification for authorization gaps
Review API endpoints backing these admin UI features for identical authorization flaws

## MITRE ATT&CK
- T1190
- T1548
- T1087
- T1566

## Notes
The vulnerability is particularly dangerous because: (1) packing slips are business-critical documents, (2) Liquid template engines can leak sensitive variables if not properly restricted, (3) the low permission requirement makes it accessible to many compromised accounts, and (4) changes would be subtle and difficult to detect immediately. This is a classic case of authorization bypass where authentication is present but insufficient authorization checks exist.

## Full report
<details><summary>Expand</summary>

**Summary:**

An admin is able to edit the Edit packing slip template at [/admin/settings/packing_slip_template](https://fisher-hackerone.myshopify.com/admin/settings/packing_slip_template). However, a staff user with only "Home" permission (and none other) can view and also make edits to this template. 

**Description:** 

The Edit packing slip feature exists so an admin user can customize the packing slip added to an order after fulfilment, without the need of external apps (such as Print Order). As mentioned, the problem here arises that any staff user in that Shop can access this endpoint and actually make edits to the template.

## Steps To Reproduce:

1. Create and login a user without permissions (Home only): 
{F354374}

2. As the user without permissions access [/admin/settings/packing_slip_template](https://fisher-hackerone.myshopify.com/admin/settings/packing_slip_template) and make any edits in the template file:
{F354375}

3. Login as other user with adequate permissions, e.g. admin and refresh the same endpoint to confirm that the changes were saved:

{F354377}

## Impact

Having control of the packing slip a malicious staff user can e.g. change the shipping address for his own, potentially receiving orders at some time in the future.

More importantly, besides any disruption of the service (by erasing the template) or manipulation, it can lead to further attacks targeting the exfiltration/disclosure of liquid variables.

</details>

---
*Analysed by Claude on 2026-05-24*
