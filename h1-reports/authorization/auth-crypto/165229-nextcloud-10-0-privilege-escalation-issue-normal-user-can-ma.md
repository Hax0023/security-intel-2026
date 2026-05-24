# Nextcloud 10.0 Privilege Escalation - Normal User Can Mask Admin's External Storage

## Metadata
- **Source:** HackerOne
- **Report:** 165229 | https://hackerone.com/reports/165229
- **Submitted:** 2016-09-02
- **Reporter:** egrep
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Privilege Escalation, Access Control, Storage Masking/Shadowing, Information Disclosure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A non-privileged user in Nextcloud 10.0 can create an external storage with an identical name to one shared by an administrator, effectively masking the admin's storage from other users in shared groups. This allows attackers to intercept access to legitimate shared resources and potentially redirect users to malicious storage configurations.

## Attack scenario
1. Attacker identifies an external storage shared by admin with a specific name (e.g., 'localstrg') within a shared group
2. Attacker creates their own external storage using the identical name 'localstrg' with different backend configuration (e.g., SFTP instead of Local)
3. Attacker configures their malicious storage with attacker-controlled credentials and shares it with the same group
4. When legitimate users access the storage name 'localstrg', the system resolves to the attacker's storage instead of the admin's due to naming collision
5. Users see only attacker's files/resources, believing they are accessing the legitimate admin-shared storage
6. Attacker gains ability to intercept, monitor, or redirect access to what users expected to be trusted administrative resources

## Root cause
Nextcloud lacks proper storage namespace isolation and naming conflict resolution. The system allows multiple external storages with identical names from different users to coexist without enforcing uniqueness constraints or implementing proper precedence/shadowing detection. The sharing mechanism does not verify if a storage name collision exists before displaying resources to users.

## Attacker mindset
An attacker seeks to impersonate trusted administrative resources to gain user trust or intercept access. By exploiting the naming collision, they can perform man-in-the-middle attacks on storage access, harvest credentials when users attempt authentication, or deliver malicious content masquerading as legitimate shared resources. The low barrier to entry (any group member can exploit this) makes it an attractive attack vector.

## Defensive takeaways
- Implement globally unique storage naming constraints or enforce user-scoped namespacing (e.g., 'username:storagename')
- Add storage name collision detection and alert administrators when naming conflicts occur
- Implement storage precedence rules based on privilege level (admin-owned storage takes priority) or creation timestamp
- Add visual indicators and audit trails showing which user owns/shares each storage resource
- Validate and verify storage backend connectivity and configuration before sharing with groups
- Implement proper RBAC controls where only administrators can create external storages
- Audit shared resources regularly to detect suspicious duplicates

## Variant hunting
Check if group-based resource shadowing exists in other Nextcloud features (shared calendars, contacts, etc.)
Test whether file/folder names can be shadowed similarly within shared namespaces
Investigate if this affects other collaborative tools integrating with Nextcloud
Examine whether app-level storage mounting has similar collision issues
Test cross-group storage sharing for privilege escalation opportunities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts
- T1199 - Trusted Relationship
- T1556 - Modify Authentication Process

## Notes
This vulnerability is particularly dangerous in multi-user enterprise Nextcloud deployments where users trust admin-shared resources. The attack requires minimal privileges (just group membership) and leaves minimal forensic traces. The fix likely requires database schema changes to enforce storage uniqueness and application logic updates to handle naming conflicts appropriately. Report demonstrates good attack scenario documentation but lacks PoC code or timeline information.

## Full report
<details><summary>Expand</summary>


Normal user(Non-privileged) can mask external storage shared by admin.
 
 
Scenario :
Created three users "admin", "attacker", "victim"
Created group "samplegroup" containing all the three users with "victim" as group admin
 
 
Steps:
1) User "admin" created external storage named "localstrg"(note: name is the attack vector) with properties:
 
Folder Name : localstrg
External Storage : Local
Authentication : None
Configuration : /
Available for : "samplegroup","admin" - groups
Settings : Enable sharing
 
2) On seeing this , user "attacker" created one more external storage with the same name "localstrg" with properties:
 
Folder Name : localstrg
External Storage : SFTP
Authentication : Username and Password
Configuration : Fill "Host", "Root" ," Username" ,"Password"
Settings : Enable sharing
 
3) After that, user "attacker" shared created external storage with group "samplegroup" which is having other two users
 
4) If suppose, user "victim" visits the external storage "localstrg" in his profile, he is only shown with files shared by user "attacker"
 
Prerequisite : Both attacker and victim should be in the same group
 
Using this vulnerability, non-privilged user can mask the external storage shared by admin to other users
 
 

</details>

---
*Analysed by Claude on 2026-05-24*
