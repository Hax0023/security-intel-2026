# Ability to access all user authentication tokens, leads to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 158330 | https://hackerone.com/reports/158330
- **Submitted:** 2016-08-11
- **Reporter:** jobert
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Sensitive Data Exposure, Insecure Deserialization, Information Disclosure, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
GitLab's project export feature serializes and includes user authentication tokens in the exported project.json file, allowing any user to obtain admin tokens by inviting them to a project and downloading the export. An attacker can use these tokens to gain unauthorized admin access to the GitLab instance, leading to remote code execution and access to all private repositories.

## Attack scenario
1. Attacker creates a test account on the target GitLab instance
2. Attacker creates a temporary repository and invites a GitLab admin as a team member
3. Attacker navigates to repository settings and initiates a project export
4. Attacker receives export file via email after processing completes
5. Attacker downloads the exported file and extracts project.json to recover the admin's authentication_token
6. Attacker uses the stolen token to authenticate as admin via URL parameter, gaining full administrative access and RCE

## Root cause
The project export feature failed to implement proper data sanitization when serializing user objects. Authentication tokens, which are highly sensitive credentials, were included in the exported data without filtering or redaction. The application also likely trusts authentication tokens passed as URL parameters without proper validation of token ownership.

## Attacker mindset
An attacker would recognize that project export functionality often contains more data than intended. By strategically inviting high-privilege users to a project they control, they can access their credentials through a feature normally intended for legitimate data portability. This represents a classic privilege escalation through feature abuse.

## Defensive takeaways
- Never include authentication tokens, API keys, or other credentials in exported data; implement token field filtering/exclusion
- Avoid serializing entire user objects - use explicit allowlisting of safe fields only
- Implement proper authentication validation that doesn't rely solely on URL parameters or tokens without verifying session context
- Apply principle of least privilege to export functionality - exported data should reflect only what the requesting user should see
- Sanitize sensitive fields at the serialization layer, not as an afterthought
- Implement export audit logging to detect suspicious export patterns (e.g., inviting admins followed by immediate export)
- Use security reviews specifically targeting serialization code paths for credential leakage

## Variant hunting
Check other export features (user exports, group exports, system backups) for similar token leakage
Examine API endpoints that return user objects to verify tokens aren't exposed in API responses
Test other serialization formats (CSV, XML, YAML) in export functions for similar issues
Look for other sensitive fields like session tokens, SAML credentials, or OAuth tokens in exports
Investigate whether other high-privilege resources (API keys, deployment tokens, runner tokens) are similarly exposed
Test if archived projects or deleted projects maintain sensitive data in exports
Check if admin/system-level exports expose tokens from all users

## MITRE ATT&CK
- T1190
- T1078
- T1526
- T1552
- T1557
- T1555

## Notes
This is a high-impact vulnerability affecting GitLab.com with clear proof-of-concept. The attack requires minimal interaction (just creating a project and inviting an admin) and yields maximum privilege escalation and data access. The vulnerability demonstrates how well-intentioned features (data portability/export) can become security disasters through inadequate data sanitization. The report references CVE-2016-3083 era GitLab, indicating this was a historical but severe issue in GitLab's architecture.

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
*Analysed by Claude on 2026-05-11*
