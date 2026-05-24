# Unauthorized Access to PII via Faulty Access Control on User Enumeration Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 904659 | https://hackerone.com/reports/904659
- **Submitted:** 2020-06-22
- **Reporter:** z32
- **Program:** HackerOne Report #904659
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln:** Broken Access Control, Insecure Direct Object References (IDOR), Information Disclosure, Insufficient Authorization Checks
- **CVEs:** None
- **Category:** web-api

## Summary
An authenticated user can access personally identifiable information (PII) of all site users through an insufficiently protected endpoint that lacks proper authorization checks. The /██████ endpoint fails to validate user permissions, allowing any logged-in user to enumerate and view sensitive user data.

## Attack scenario
1. Attacker creates or logs into a standard user account on the target website
2. Attacker navigates to the /███████/████████ endpoint directly via browser
3. Endpoint fails to perform authorization checks, returning user list data to unauthorized user
4. Attacker iterates through usernames or IDs to access individual user profiles
5. Attacker retrieves sensitive PII (email, phone, address, etc.) for all enumerated users
6. Attacker exfiltrates or weaponizes the collected PII for identity theft, phishing, or social engineering

## Root cause
Missing or inadequate authorization middleware/checks on the /██████ endpoint. The application authenticates users (verifies they are logged in) but fails to authorize their access to administrative or privileged user enumeration functions. Authorization logic either does not exist or does not verify admin role requirements.

## Attacker mindset
An attacker with basic web application knowledge recognizes that authenticated access often opens attack surface for privilege escalation. By probing common administrative paths and endpoints, they discover that user enumeration functionality lacks proper access controls. The low barrier to entry (just needing to login) makes this highly exploitable. Mass PII collection enables downstream attacks with higher impact.

## Defensive takeaways
- Implement explicit role-based access control (RBAC) on all endpoints; default-deny for administrative functions
- Separate user roles clearly (admin, moderator, user) and enforce authorization checks at controller/middleware level
- Audit all endpoints that expose user data or system information for missing authorization logic
- Use security testing frameworks to verify that unauthorized users receive 403 Forbidden responses, not data
- Log and monitor access attempts to sensitive endpoints for anomalous enumeration patterns
- Implement rate limiting on user enumeration endpoints to mitigate bulk data harvesting
- Conduct threat modeling specifically around IDOR and authorization bypass scenarios
- Use automated security scanning and code review to detect missing authorization checks before deployment

## Variant hunting
Check adjacent endpoints (/users, /admin, /api/users) for similar authorization bypasses
Test parameter manipulation (e.g., /users?role=admin) to escalate privileges
Attempt unauthenticated access to the same endpoint to identify authentication vs. authorization gaps
Test API versions or alternate URLs (e.g., /api/v1/users vs /users) for inconsistent access control
Check export/reporting functions that might aggregate user data without proper authorization
Test batch operations or admin functions that expose user PII in error messages or responses
Review other modules accessible after login for similar missing authorization checks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate External Targets
- T1087 - Account Discovery
- T1589 - Gather Victim Identity Information
- T1566 - Phishing (post-collection exploitation)

## Notes
This is a critical severity finding because PII exposure enables identity theft, social engineering, and downstream compromise. The low complexity of exploitation (unauthenticated is not even required—just logged-in user) and high impact (all user data exposed) make this a priority remediation. The writeup indicates the fix is straightforward (add admin role check), suggesting this was a development oversight rather than a design flaw. HackerOne report number 904659 indicates this was a real vulnerability on a major platform.

## Full report
<details><summary>Expand</summary>

**Summary:**
The ██████████ website allows access to PII of all site users via faulty access control to the /██████ endpoint.

## Step-by-step Reproduction Instructions

1. Browse to ████████ and login or create an account.
2. Browse to ███████/████████. You will be able to access PII of all site users (click a username to view the PII).

## Suggested Mitigation/Remediation Actions
Restrict access to the /██████████ module to only administrative users.

## Impact

An adversary can gain access to PII of all ███████ users.

</details>

---
*Analysed by Claude on 2026-05-24*
