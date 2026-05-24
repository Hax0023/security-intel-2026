# Unauthorized Access to Team Members' Personal Information via API - Leaderboard Teams

## Metadata
- **Source:** HackerOne
- **Report:** 244781 | https://hackerone.com/reports/244781
- **Submitted:** 2017-06-30
- **Reporter:** hackedbrain
- **Program:** WakaTime
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The WakaTime API endpoint for retrieving leaderboard team members lacked proper authorization validation, allowing users with 'Member' role to access sensitive personal information (email addresses, roles) of all team members despite policy restricting this to Owners and Admins only. The vulnerability existed in the `/api/v1/users/current/leaderboards/<team_id>/members` endpoint which performed insufficient permission checks before returning member details.

## Attack scenario
1. Attacker joins a target Leaderboard team by getting invited with a 'Member' role
2. Attacker identifies and copies the team_id of the leaderboard
3. Attacker crafts a direct API request to `/api/v1/users/current/leaderboards/<team_id>/members`
4. API endpoint executes the request without verifying the attacker's role/permissions
5. Endpoint returns complete list of all team members with their email addresses and roles
6. Attacker harvests personal information of all team members for further attacks or data compilation

## Root cause
The API endpoint implementation performed insufficient authorization checks, likely only verifying that the user belongs to the team without validating their specific role (Owner/Admin vs Member). The code probably checked membership existence but did not enforce role-based access control (RBAC) rules that were enforced in the web UI.

## Attacker mindset
An attacker with basic member access could enumerate sensitive user data (emails) from teams they join, enabling targeted phishing campaigns, social engineering, or competitive intelligence gathering against organization members.

## Defensive takeaways
- Always enforce consistent authorization checks across all access points (UI and API) - never trust that UI restrictions alone protect data
- Implement explicit role-based access control (RBAC) checks before returning sensitive user information
- Apply principle of least privilege: verify user role/permissions for each resource access, not just team membership
- Audit API endpoints for authorization gaps by testing with lower-privilege accounts
- Use centralized authorization middleware/functions to prevent inconsistent permission enforcement across endpoints
- Never return PII (emails, phone numbers) to users lacking explicit authorization, even if they're team members
- Implement comprehensive API security testing including role-based access control validation

## Variant hunting
Check other team/organization management endpoints for similar authorization bypasses
Test other sensitive endpoints (team settings, member roles, billing info) with member-level accounts
Investigate whether other role-based data (admin logs, activity feeds) is similarly exposed
Check for authorization bypass in bulk member operations or export functions
Test whether member-level users can modify team settings or member roles via API
Audit other leaderboard-related endpoints for similar information disclosure

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1590

## Notes
This is a classic example of authorization/permission bypass where business logic constraints enforced in the UI were not replicated in API code. The vulnerability required low effort to exploit and had clear attack surface (direct URL with team_id parameter). WakaTime likely fixed this by adding role verification to the API endpoint to match UI restrictions. The use of generic 'current' user endpoint suggests it may have checked authentication but not authorization.

## Full report
<details><summary>Expand</summary>

**Description:** According to the rules of Leaderboard Teams only Owners and admins have access to other team members' personal information like email address, roles etc.

Users whose role set as "Member" can't see other users' details.

But through API it is possible for a user with member role to reveal personal information of all team members.

**Vulnerable URL: `https://wakatime.com/api/v1/users/current/leaderboards/<team_id>/members`**

**Steps to reproduce:**

1. Join a Leaderboard team as a member.
2. Copy the team id.
3. Visit the vulnerable url.

You'll find that emails of all members being disclosed.

</details>

---
*Analysed by Claude on 2026-05-24*
