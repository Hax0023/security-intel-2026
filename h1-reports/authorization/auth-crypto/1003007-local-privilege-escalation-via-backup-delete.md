# Local Privilege Escalation via Backup Folder Rename and Symlink Attack in Acronis True Image 2021

## Metadata
- **Source:** HackerOne
- **Report:** 1003007 | https://hackerone.com/reports/1003007
- **Submitted:** 2020-10-08
- **Reporter:** z3ron3
- **Program:** Acronis True Image 2021
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Privilege Escalation, Symlink Attack (TOCTOU), Insufficient Access Control, Incomplete Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image 2021's AntiRansomware Protection fails to monitor folder rename operations on backup directories, allowing attackers to bypass protection by renaming the backup folder and creating symlinks to arbitrary system files. When Acronis attempts to delete the backup via UI, the symlink redirects deletion to protected system files, enabling unprivileged users to delete privileged files like system drivers.

## Attack scenario
1. Attacker creates a backup in Acronis True Image to establish a .tib backup file in a monitored directory
2. Attacker renames the backup folder (e.g., backup_acronis to not_backup_acronis) - this rename operation bypasses AntiRansomware monitoring
3. Attacker creates a new folder with the original name (backup_acronis) that is unprotected by AntiRansomware
4. Attacker creates a symlink at the expected .tib file location pointing to a privileged target file (e.g., C:\Windows\System32\drivers\pci.sys)
5. Attacker uses Acronis UI to delete the backup, triggering the backup deletion routine
6. Acronis attempts to delete the .tib file from the symlinked path, resulting in deletion of the privileged target file without permission checks

## Root cause
AntiRansomware protection monitoring logic has a gap: it monitors file modifications and most folder operations but fails to monitor or block rename operations on backup directories. This creates a TOCTOU (Time-of-Check-Time-of-Use) window where an attacker can rename the folder out of protection, create an unprotected replacement, and insert symlinks. Additionally, the backup deletion routine does not validate that the target path is the expected .tib file and fails to dereference symlinks before deletion.

## Attacker mindset
Identify edge cases in security controls - specifically operations that monitoring might overlook (rename vs. write/delete). Exploit TOCTOU vulnerabilities by moving targets between protected and unprotected states. Use symlink attacks to redirect privileged operations to unintended targets. Recognize that backup management typically runs with elevated privileges, making it a privilege escalation vector.

## Defensive takeaways
- Monitor ALL file system operations on protected paths including rename, move, and attribute changes, not just write/delete
- Implement path canonicalization and symlink resolution before performing file operations to prevent TOCTOU attacks
- Validate that file handles and paths remain unchanged between security checks and actual file operations
- Use file system namespaces or isolation to prevent creation of symlinks within protected directories
- Require privilege validation at operation execution time, not just at initial check time
- Implement inode-based tracking rather than path-based tracking for protected backup files
- Use file object identifiers (handles) that persist across operations to ensure target integrity

## Variant hunting
Test other folder operations (move, copy) on backup directories for similar monitoring gaps
Check if symlink attacks work on individual .tib files (not just directories)
Investigate whether hardlinks instead of symlinks bypass the protection
Test if renaming .tib files directly (if original folder name is unchanged) bypasses protection
Look for similar TOCTOU gaps in other Acronis products (Backup, Disaster Recovery)
Test whether junction points or directory symlinks trigger different code paths
Attempt to exploit during active backup/restore operations when file locks may be weaker

## MITRE ATT&CK
- T1548.004
- T1036.006
- T1542.005
- T1562.001

## Notes
This vulnerability chain is particularly elegant because it exploits a monitoring gap (rename operations) combined with a privileged operation (backup deletion via Acronis service) and symlink attacks. The reporter notes that the broader impact is the ability to modify AntiRansomware-protected backup files without permission, with privileged deletion being one manifestation. The attack requires local access but no special privileges initially. Acronis True Image 2021 Build 32010 is confirmed vulnerable. The report demonstrates excellent security research methodology by clearly separating preparation, exploitation, and impact analysis.

## Full report
<details><summary>Expand</summary>

## Summary
Acronis True Image 2021 is famous for its seamless Backup and Restore feature which lets users backup any data to any place of their choice and restore it back in case of accidental loss. I found a serious bug/bypass in Acronis AntiRansomware Service when it comes to accessing backup files which when combined with symlink attack can let an attacker modify AntiRansomware protected backup files and delete any file on the system without permissions leading to Privilege Escalation.


## Issue
Acronis True Image  saves information about backups in ```.tib``` files. The ```.tib``` file itself as well as the folder it is in is monitored by Acronis AntiRansomware Protection to block any kind of modification unless an exclusion is created. The issue is that it monitors all modification operations on the file and folder except **Rename** operation on the folder containing the ```.tib``` file.


## Steps To Reproduce
We need to have a backup first to be able to delete it. The **Preparation** part contains the steps to create a backup and **Exploitation** part contains the steps to exploit the vulnerability. If you already have a backup, skip **Preparation** part.


Preparation:
------------
[ 1 ] - Create a file in a folder which is to be backed up. I chose to create a file named ```poc.exe``` in ```data_acronis``` folder on my Desktop.

```mkdir %userprofile%\Desktop\data_acronis & echo PoC > %userprofile%\Desktop\data_acronis\poc.exe```

{F1028123}

[ 2 ] - In Backup tab of Acronis True Image, click on **Change source** then click on **Files and folders** and select ```poc.exe``` file from ```data_acronis``` folder.

{F1028125}

[ 3 ] - Create a folder to save the backup .tib files in. I chose to create a folder named ```backup_acronis``` on my Desktop.

```mkdir %userprofile%\Desktop\backup_acronis```

{F1028127}

[ 4 ] - Click on **Select destination**, then click on **Browse** and select the ```backup_acronis``` folder.

{F1028128}

[ 5 ] - Click on **Back up now**.

{F1028129}

```poc.exe``` file from ```data_acronis``` folder will be backed up by Acronis True Image and the .tib files will be saved in ```backup_folder``` folder.

{F1028130}

Exploitation:
------------
The name pattern for the .tib files is ```[backup_name]_[backup_scheme]_b1_s1_v1.tib``` so after the backup, a file named ```poc_full_b1_s1_v1.tib``` will be created in ```backup_acronis``` folder.

Normally, the backup ```.tib``` files and folder are protected by Acronis AntiRansomware Protection from any kind of modification.

{F1028131}

But the issue is that it does not monitor and block **Rename** operation on the folder where the ```.tib``` files are stored which is ```%userprofile%\Desktop\backup_acronis``` in this case.

[ 1 ] - Rename ```backup_acronis``` to any other name.

```rename %userprofile%\Desktop\backup_acronis not_backup_acronis```

{F1028132}

[ 2 ] - Create a symlink from ```%userprofile%\Desktop\acronis_backup\poc_full_b1_s1_v1.tib``` file to the target file which is to be deleted. I will try to delete ```C:\Windows\System32\drivers\pci.sys``` file.
I've used CreateSymlink tool from [symboliclink-testing-tools](https://github.com/googleprojectzero/symboliclink-testing-tools) in this example.

```CreateSymlink %userprofile%\Desktop\backup_acronis\poc_full_b1_s1_v1.tib C:\Windows\System32\drivers\pci.sys```

{F1028133}

[ 3 ] - Go to Backup tab, right click on the backup and click on **Delete**, then click on **Delete entirely** option.

{F1028134}

Acronis True Image will try to delete the ```poc_full_b1_s1_v1.tib``` file from ```%userprofile%\Desktop\backup_acronis``` folder but because of the symlink the operation will be performed on ```C:\Windows\System32\drivers\pci.sys``` resulting in its deletion.

{F1028135}


## Tested on
Windows 10 Home, Version 2004 (OS Build 19041.450)
Acronis True Image 2021, Build 32010

Regards,
Saurabh Patil  ( @z3ron3 )

## Impact

If we rename the folder which contains the ```.tib``` file and create new folder of same name, we are able to write into the new folder without AntiRansomware protection blocking the write and Acronis True Image will assume its the same folder and read content from it which totally breaks the aim of Actve AntiRansomware protection as anyone is able to change contents of the ```.tib``` file.

Being able to change contents of AntiRansomware protected backup files without permission is a big issue in itself for True Image so I think this issue should be considered with greater severity. Privileged delete was just an application of the issue .

</details>

---
*Analysed by Claude on 2026-05-24*
