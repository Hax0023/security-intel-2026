# Team Admin Privilege Escalation via Unauthorized Team Settings Modification

## Metadata
- **Source:** HackerOne
- **Report:** 46750 | https://hackerone.com/reports/46750
- **Submitted:** 2015-02-05
- **Reporter:** satishb3
- **Program:** Slack
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Privilege Escalation, Broken Access Control, Insufficient Authorization Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A team admin user can escalate privileges and modify the 'allow_message_deletion' setting, which should be restricted to team owners only. By directly calling the API endpoint /api/team.prefs.set with crafted parameters, an admin can bypass role-based access controls and enable message deletion permissions designated for owner-only management.

## Attack scenario
1. Attacker authenticates as a user with team admin role
2. Attacker identifies the /api/team.prefs.set endpoint through API reconnaissance or web traffic inspection
3. Attacker constructs a POST request with the allow_message_deletion parameter set to true in the prefs JSON payload
4. Attacker includes valid authentication token (xoxs-*) and team cookie in request headers
5. API endpoint processes request without validating role requirements for the specific setting
6. Setting is successfully modified despite user having insufficient privileges; owner-only restriction is bypassed

## Root cause
The /api/team.prefs.set endpoint implements insufficient authorization checks. While it may validate that the user is an admin, it fails to enforce granular permission controls that distinguish between admin-modifiable and owner-only settings. The backend does not properly validate that the allow_message_deletion setting requires owner role before applying changes.

## Attacker mindset
An insider threat with admin access seeking to expand control over team collaboration features, or a malicious admin attempting to alter message retention/deletion policies to cover tracks or disrupt team operations. The attacker methodically tests API endpoints with elevated requests to identify authorization gaps.

## Defensive takeaways
- Implement role-based access control (RBAC) at the API endpoint level with granular permission mappings for each team setting
- Enforce server-side authorization checks before processing any preference modifications, not just authentication
- Maintain a configuration matrix defining which roles can modify which settings (owner-only vs admin-modifiable)
- Log all attempts to modify team settings with user role, timestamp, and setting name for audit trails
- Validate that permission requirements are enforced for both UI and API interactions
- Implement consistency checks to prevent API endpoints from bypassing UI-enforced restrictions
- Use decorator-based authorization middleware to ensure consistent permission validation across all administrative endpoints

## Variant hunting
Test other team.prefs.set parameters for similar privilege escalation (msg_edit_window_mins, workspace restrictions, etc.)
Probe adjacent admin endpoints (/api/team.*, /api/admin.*) for insufficient authorization on owner-only features
Attempt to modify settings as non-admin user roles to identify missing baseline checks
Test with revoked/expired tokens to verify authentication state validation
Investigate if other Slack API endpoints have similar granular permission bypass issues
Check for time-of-check-time-of-use (TOCTOU) race conditions in permission validation

## MITRE ATT&CK
- T1190
- T1548.002
- T1078.001
- T1087

## Notes
This is a classic broken access control vulnerability where authorization logic is either missing or bypassed at the API layer. The vulnerability demonstrates that UI-level restrictions (checkboxes in admin panels) are insufficient without corresponding API-level enforcement. The use of direct API calls with valid tokens but insufficient role validation is a common pattern in privilege escalation attacks against multi-tenant platforms with role-based access models.

## Full report
<details><summary>Expand</summary>

Team admin can escalate his privileges and change 'allow_message_deletion' team setting, which can be changed only by a team owner.

Steps to reproduce:
1. Log in as team admin.
2. Send the below request using his cookie & token and notice that it changes 'allow_message_deletion' team setting to true.

POST /api/team.prefs.set?t=1423146704 HTTP/1.1
Host: teamname.slack.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: https://teamname.slack.com/admin/settings
Cookie: _ga=GA1.2.630936366.1423056192; a-3204538285=..

prefs=%7B%22msg_edit_window_mins%22%3A%221%22%2C%22allow_message_deletion%22%3Atrue%7D&token=xoxs-xxxx&set_active=true&_attempts=1

To confirm, login as team owner. Navigate to /admin/settings#permissions, expand message editing & deletion section. Notice that 'Only administrators may delete messages' checkbox is checked.

</details>

---
*Analysed by Claude on 2026-05-24*
