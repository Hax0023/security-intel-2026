# Authentication Tokens Exposed in Project Export Feature Leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 158330 | https://hackerone.com/reports/158330
- **Submitted:** 2016-08-11
- **Reporter:** jobert
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Sensitive Data Exposure, Insecure Serialization, Authentication Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
GitLab's project export feature serialized complete user objects including authentication tokens into the exported project.json file, allowing any user to invite administrators to their project, export it, and extract their credentials. This enabled direct authentication bypass and remote code execution through the admin panel.

## Attack scenario
1. Attacker creates a test account on GitLab instance and sets up a temporary repository
2. Attacker invites an administrative user as a team member to the repository
3. Attacker navigates to repository settings and initiates a project export
4. Attacker downloads the generated export file and extracts the project.json
5. Attacker locates the authentication_token within the project_members user object
6. Attacker uses the stolen token to authenticate as the admin via the admin panel URL parameter, gaining administrative access and RCE

## Root cause
Insufficient data sanitization during project export serialization. The application exported complete user objects without filtering sensitive fields like authentication_token, storing them in an accessible archive that users could download.

## Attacker mindset
Low-skill opportunistic attacker could exploit this systematically. The attack requires no special knowledge—just understanding basic GitLab features. Attackers could target known admin accounts, making this a high-impact vulnerability suitable for supply chain or insider threats.

## Defensive takeaways
- Never serialize sensitive security credentials (tokens, passwords, keys) in data exports
- Implement explicit allowlist for exportable user fields—only include non-sensitive attributes
- Strip authentication tokens and secrets before any data serialization or export operations
- Sanitize all user-generated exports and backups before delivery to users
- Implement strict authentication token validation with rate limiting and anomaly detection
- Add audit logging for authentication token usage, especially from unexpected locations
- Consider token expiration windows and implement token rotation policies
- Validate that token-based admin access comes from expected administrative interfaces only

## Variant hunting
Check for similar serialization issues in: backup/snapshot features, data migration tools, API responses returning user objects, team member listing exports, audit log exports, any feature allowing users to download/share data containing other user information. Test whether other sensitive fields (password_hash, api_keys, oauth_tokens, ssh_keys) are similarly exposed in exports.

## MITRE ATT&CK
- T1190
- T1078
- T1552
- T1555
- T1134

## Notes
This represents a fundamental design flaw in treating export functionality as safe for users with access to sensitive data. The vulnerability violates the principle of least privilege in data exposure. The fact that authentication tokens could be used directly in URLs as query parameters compounds the severity. This likely affected all GitLab instances running vulnerable versions, making it a critical infrastructure risk.

## Full report
<details><summary>Expand</summary>

# Vulnerability details
The project export feature serializes the user objects of team members and stores it in the `project.json` file. This object contains the `authentication_token` for every user, meaning that an attacker can simply go ahead and create a project on GitLab.com, add one of the admins of GitLab.com, create an export, and obtain the authentication token for that user.

# Proof of concept
Follow these steps to reproduce the issue:

 - create a test account on a GitLab instance and create a temporary repository
 - invite an admin of the GitLab instance as a team member to the repository
 - go to the repository settings and create an export
 - wait a few minutes until you received the export email
 - now go to http://gitlab-instance/account/repo/download_export
 - unzip the downloaded file and examine `projects.json` - the `project_members` will contain the user object that contains the `authentication_token`

Here's the first few bytes of `rspeicher` (sorry Robert) his authentication token on GitLab.com: `ZyhqJr4XJZ...`. Someone could get access to GitLab's admin panel by extracting the token of an admin and go to https://gitlab.com/admin/users?authentication_token=<token>. From what I've seen on my own GitLab instance, this leads to RCE and gives me access to all code in private repositories. Let me know if you need more information!

</details>

---
*Analysed by Claude on 2026-05-24*
