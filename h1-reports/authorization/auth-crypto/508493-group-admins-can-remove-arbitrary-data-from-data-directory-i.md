# Group Admins Can Remove Arbitrary Data from Data Directory

## Metadata
- **Source:** HackerOne
- **Report:** 508493 | https://hackerone.com/reports/508493
- **Submitted:** 2019-03-12
- **Reporter:** leonklingele
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Arbitrary File Deletion, Path Traversal, Insecure Direct Object References, Privilege Escalation
- **CVEs:** CVE-2019-15624
- **Category:** auth-crypto

## Summary
Group administrators can create users with specially crafted usernames that map to system directories (e.g., 'files_external', 'appdata_*') and then delete these users to remove arbitrary data from the data directory, including critical system and admin data. This vulnerability allows privilege escalation from group admin to system-wide data destruction.

## Attack scenario
1. Attacker obtains group admin privileges in a Nextcloud instance
2. Attacker creates a new user with username 'files_external' or 'appdata_{random}' mapping to existing system directories
3. System creates user directory at data/{malicious-username} which overwrites or references existing sensitive directories
4. Attacker deletes the malicious user account
5. User deletion triggers recursive deletion of data/{username} directory
6. Arbitrary system data is permanently removed from the Nextcloud installation

## Root cause
The user creation and deletion functions lack validation to prevent creating users whose uid maps to existing directories or reserved system paths. When a user is deleted, the system recursively removes data/{user} without checking if this directory contains unexpected content beyond standard user files.

## Attacker mindset
Exploit administrative capabilities in a privileged role to achieve unauthorized system-level destructive actions. Use directory naming conventions to bypass access controls by mapping user creation to protected paths.

## Defensive takeaways
- Validate user identifiers against reserved/existing directory names before creation
- Implement whitelist of allowed characters in user creation
- Verify user data directory contains only expected user files before deletion
- Add integrity checks and backups for critical system directories
- Log user creation/deletion operations with detailed directory information
- Implement directory ownership verification before recursive deletion
- Use separate namespacing for system directories vs user data
- Restrict group admin permissions from creating certain user patterns

## Variant hunting
Test creation of users with names matching other system directories: 'cache', 'temp', 'config', 'uploads'
Attempt user creation with path traversal sequences: '../', '..%2f'
Test deletion of users where data directory symlinks to sensitive paths
Check if other admin-level operations have similar directory validation gaps
Verify if organization/group deletion has similar vulnerabilities
Test with unicode or encoded characters in usernames to bypass validation

## MITRE ATT&CK
- T1190
- T1499
- T1531
- T1485

## Notes
This is a critical Nextcloud vulnerability (CVE likely assigned). The vulnerability chains user creation privileges with unrestricted deletion capabilities. The suggested fix is sound: validate usernames against existing paths and verify directory contents before deletion. Group admin role should have more restricted scope.

## Full report
<details><summary>Expand</summary>

Steps to reproduce:

1. Create a new user and make him an admin of an arbitrary group
2. Log in as this new user
3. Create a new user "files_external", "appdata_{random-data}", ..
4. Delete this user

Result: The data/files_external / data/appdata{..} folder is removed.

Solution: Prevent creation of users if data/{new-user-uid} is either
a file or a folder. In addition, prevent deletion of users where the
user data directory (data/{user}) contains other files and folders
than "files" (where the user data is stored).

## Impact

Group admin can remove arbitrary data from "data" directory

</details>

---
*Analysed by Claude on 2026-05-24*
