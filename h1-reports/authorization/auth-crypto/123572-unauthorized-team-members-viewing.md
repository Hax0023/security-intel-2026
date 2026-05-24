# Unauthorized Team Members Viewing via JSON Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 123572 | https://hackerone.com/reports/123572
- **Submitted:** 2016-03-16
- **Reporter:** temmyscript
- **Program:** HackerOne
- **Bounty:** Not specified in provided content
- **Severity:** Medium
- **Vuln:** Authorization Bypass, Information Disclosure, Broken Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Non-admin team members can bypass authorization controls to view all team members by accessing the .json API endpoint directly, despite the web UI restricting this functionality to administrators only. This allows unauthorized information disclosure of team composition and member details.

## Attack scenario
1. Attacker creates or joins a HackerOne team as a non-admin member
2. Attacker observes that the web UI at /team_members restricts viewing to admin users only
3. Attacker discovers the JSON API endpoint at /team_members.json
4. Attacker makes a direct HTTP GET request to /team_members.json with their authentication token
5. Server returns complete JSON listing of all team members despite requester lacking admin privileges
6. Attacker gains visibility into sensitive team composition, member roles, and personal information

## Root cause
Authorization checks were implemented on the HTML web interface but not enforced on the underlying API endpoint, creating an inconsistency. The server trusted client-side or UI-level access controls without validating permissions at the API layer.

## Attacker mindset
Reconnaissance-focused; searching for alternative access vectors when direct UI access is denied. Recognizes that web applications often expose API endpoints in standard formats (.json, .xml) and tests whether authorization boundaries apply consistently across interfaces.

## Defensive takeaways
- Enforce authorization checks server-side at the API endpoint level, not just the UI presentation layer
- Apply consistent permission validation across all interface formats (HTML, JSON, XML, etc.)
- Conduct access control testing for both UI and API endpoints separately
- Implement integration tests that verify authorization policies work across all response formats
- Use framework-level authorization middleware to prevent bypassing controls through endpoint variations
- Review all API endpoints that expose the same data as UI views for consistency

## Variant hunting
Test other admin-only endpoints with .json, .xml, .api suffixes
Check if other data export formats bypass authorization (CSV, PDF exports)
Verify if different API versions have the same authorization gap
Test if query parameters like ?format=json bypass checks
Check GraphQL endpoints for similar authorization inconsistencies
Attempt accessing other admin-restricted resources via alternative representations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Gather Victim Identity Information
- T1592 - Gather Victim Host Information

## Notes
Classic case of authorization bypass through API endpoint discovery. Common vulnerability pattern where developers implement security controls on primary UI path but forget to apply same checks to API endpoints or alternative data formats. Demonstrates importance of treating API endpoints as primary security boundaries rather than secondary interfaces.

## Full report
<details><summary>Expand</summary>

In a Team, a user that does not have an admin permission at https://hackerone.com/[team_name]/team_members can view the list of users in the Program by visiting 
https://hackerone.com/[team_name]/team_members.json
Although it is only a user with an admin permission that can view the Team members and modify their permission, but other members that do not have such right can view ALL the members in the Team.


</details>

---
*Analysed by Claude on 2026-05-24*
