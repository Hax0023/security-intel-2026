# Limited Privilege User Can Create Unauthorized Referrals on partners.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 1457471 | https://hackerone.com/reports/1457471
- **Submitted:** 2022-01-21
- **Reporter:** samux
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Authorization Bypass, Broken Access Control, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A user with limited privileges can bypass authorization checks to create POS Leads/referrals by directly accessing the endpoint URL, despite not having the necessary permissions assigned by an administrator. The vulnerability exists because access control is not properly enforced at the endpoint level, only at the UI level.

## Attack scenario
1. Administrator creates a partner user account with limited privileges that excludes referral/lead functionality access
2. Limited privilege user authenticates to partners.shopify.com portal
3. User observes they cannot access /partner_id/referrals/ page due to UI-level restrictions
4. User discovers the underlying endpoint pattern by examining administrator access or through reconnaissance
5. User directly navigates to https://partners.shopify.com/partner_id/partner_leads/pos endpoint
6. Server accepts request without validating user privileges and allows creation of POS Lead

## Root cause
Client-side or UI-level authorization checks without corresponding server-side validation. The referrals feature implements permission checks in the user interface but fails to enforce these same checks on the backend endpoints, allowing direct URL access to bypass restrictions.

## Attacker mindset
An insider threat or limited-privilege user seeking to exceed their assigned role capabilities. The attacker recognizes that UI restrictions can be circumvented by direct API/endpoint access and exploits the lack of server-side authorization enforcement.

## Defensive takeaways
- Always implement server-side authorization checks before processing any privileged action, never rely solely on client-side or UI-level restrictions
- Use a consistent authorization/permission model across all endpoints and ensure every sensitive operation validates user permissions
- Implement implicit deny by default - if a user lacks explicit permission, the action should be rejected regardless of how the request is made
- Log and monitor direct endpoint access attempts, especially unauthorized ones, to detect privilege escalation attempts
- Conduct regular access control audits across all endpoints to identify cases where UI-level controls exist without corresponding backend enforcement

## Variant hunting
Check other features in partners.shopify.com portal that may have similar UI/backend authorization mismatches
Test all role-based features with limited privilege accounts to see if endpoint-level restrictions exist
Review other administrative portals for similar patterns where privileged endpoints lack proper authorization validation
Search for other /partner_id/* endpoints that may suffer from the same authorization bypass
Test permission inheritance and role escalation patterns across the partner ecosystem

## MITRE ATT&CK
- T1190
- T1578
- T1548

## Notes
This is a classic authorization bypass resulting from incomplete security implementation. The vulnerability highlights the importance of defense-in-depth - UI-level restrictions provide UX but not security. The attacker had legitimate access to the system but exploited missing backend validation. This type of vulnerability is common in multi-tenant systems where privilege levels must be strictly enforced.

## Full report
<details><summary>Expand</summary>

###Summary

I have been working on the partner web portal and have noticed the referrals feature contains an issue where a user with limited privileges can create referrals in an unauthorized manner.

###Steps to Reproduce

First you must authenticate with an administrator user and then invite another with limited privileges

{F1587397}

You may notice that the invited user does not have any privileges on the referral functionality.

When you authenticate with the user with limited privileges and then go to the referral functionality

`https://partners.shopify.com/partner_id/referrals/`

███████

You may notice that the user does not have the appropriate privileges to access this functionality.

Now, when the administrator accesses this same functionality.

███

It can be seen that the administrator can do several things, including `Submit a POS Lead`. Entering this url generates the following endpoint:


`https://partners.shopify.com/partner_id/partner_leads/pos`

In this way if the user with limited privileges accesses this URL.

█████

Instead of getting an error, the user can create a new POS Lead within the referrals. By completing the information.


████


It is observed that he was able to complete it with success.

Thanks.

## Impact

Through this vulnerability, an attacker can bypass the implemented restriction in order to perform an action without authorization.

</details>

---
*Analysed by Claude on 2026-05-24*
