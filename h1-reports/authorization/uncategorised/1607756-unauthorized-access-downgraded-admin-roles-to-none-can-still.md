# Unauthorized Access - Downgraded Admin Roles Can Still Edit Projects via Burp Suite

## Metadata
- **Source:** HackerOne
- **Report:** 1607756 | https://hackerone.com/reports/1607756
- **Submitted:** 2022-06-20
- **Reporter:** irwanjugabro
- **Program:** Omise
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Privilege Escalation, Insecure Direct Object References (IDOR), Missing Authorization Checks
- **CVEs:** None
- **Category:** uncategorised

## Summary
A privilege escalation vulnerability exists where users with admin roles can continue to edit projects and create links even after their role has been downgraded to 'none' by the owner. The vulnerability allows bypassing client-side role validation by replaying previously intercepted requests via Burp Suite, indicating missing server-side authorization enforcement.

## Attack scenario
1. Attacker receives admin role invitation to a team project at https://dashboard.omise.co/team
2. Attacker intercepts legitimate admin requests (e.g., edit/add link requests to https://dashboard.omise.co/v2/links) using Burp Suite proxy
3. Owner revokes attacker's admin privileges and downgrades role to 'none'
4. Attacker observes that UI no longer displays the create/edit link features, indicating client-side enforcement
5. Attacker replays the previously captured requests via Burp Suite with identical parameters and headers
6. Server processes requests successfully and allows project modifications despite downgraded role, granting unauthorized access

## Root cause
Server-side authorization validation is missing or insufficient. The application relies on client-side role checks to restrict functionality and only validates user roles against cached or stale session data. Backend API endpoints (e.g., /v2/links) do not re-verify the current user's role permissions before processing modification requests, allowing replayed requests to bypass revoked access.

## Attacker mindset
An insider threat or compromised user account holder recognizing that role downgrades only affect UI rendering. The attacker understands that intercepting requests with Burp Suite allows replaying authenticated API calls that server-side code fails to properly authorize. This represents opportunistic privilege escalation to maintain unauthorized access to project data.

## Defensive takeaways
- Implement server-side authorization checks on every API endpoint that modifies data, verifying the user's current role in real-time before processing requests
- Maintain session-level role caching with expiration/invalidation mechanisms; invalidate cached permissions immediately upon role changes
- Use token-based authorization (JWT with short expiration, or server-validated session tokens) that reflects current user permissions
- Log all authorization failures and privilege changes with user/timestamp/action details for audit trails
- Implement rate limiting and anomaly detection on API endpoints to identify replay attacks or unusual access patterns
- Add CSRF tokens to state-changing requests to prevent request replay attacks
- Perform regular security testing including authorization bypass scenarios and role downgrade testing
- Use API gateway or middleware to enforce authorization policies centrally, preventing bypasses at individual endpoint level

## Variant hunting
Test if downgraded users can perform DELETE operations on resources via replayed requests
Check if role downgrades to 'viewer' or 'editor' (not just 'none') still allow unauthorized modifications
Attempt to modify other users' projects through object references (IDOR) with downgraded roles
Test if adding new team members with downgraded roles but replayed admin requests creates privilege escalation chains
Verify if API responses include cached permission data that doesn't reflect current role state
Check if session tokens/cookies are invalidated on role downgrade or if old tokens remain valid

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1548 - Abuse Elevation Control Mechanism
- T1550 - Use Alternate Authentication Material
- T1110 - Brute Force

## Notes
This is a classic broken access control vulnerability combining weak client-side validation with missing server-side authorization checks. The use of Burp Suite highlights that the application fails at the API layer to validate permissions. The vulnerability affects dashboard.omise.co (payment processing platform), making unauthorized project/link modifications a significant risk. The PoC content was redacted in the original report but the attack steps are clear. Severity should be High due to the ability to maintain unauthorized access post-downgrade and the financial transaction context of Omise.

## Full report
<details><summary>Expand</summary>

hi team,
I found that your site is vulnerable to Unauthorized Access lead to  privilege escalation, where when the owner invites a user with admin roles, the user can still edit anything with admin access, via brupsuite, it should get an error message because the admin role has been removed.


production step:
1. The `owner `invites `user` with admin roles at https://dashboard.omise.co/team
2. Then the `user`, intercept any request using brupsuite, for example edit/add link at https://dashboard.omise.co/v2/links
3. then the `owner` lowers the role to `none`
4. then you will see, the user does not see the create link feature because the role is lost
5. but when the `user` repeats the request step#2 via brupstuite. then it will be valid.

PoC :
██████

## Impact

Unauthorized Access lead to  privilege escalation, downgraded admin roles to none can still edit projects through brupsuite

</details>

---
*Analysed by Claude on 2026-05-24*
