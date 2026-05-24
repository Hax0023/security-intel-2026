# Ability to access all user authentication tokens, leads to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 158330 | https://hackerone.com/reports/158330
- **Submitted:** 2016-08-11
- **Reporter:** jobert
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
# Vulnerability details
The project export feature serializes the user objects of team members and stores it in the `project.json` file. This object contains the `authentication_token` for every user, meaning that an attacker can simply go ahead and create a project on GitLab.com, add one of the admins of GitLab.com, create an export, and obtain the authentication token for that user.

# Proof of 

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

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
