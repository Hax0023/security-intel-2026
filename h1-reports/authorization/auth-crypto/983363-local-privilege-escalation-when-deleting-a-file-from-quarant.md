# Local Privilege Escalation via Symlink Attack in Acronis True Image Quarantine Delete

## Metadata
- **Source:** HackerOne
- **Report:** 983363 | https://hackerone.com/reports/983363
- **Submitted:** 2020-09-16
- **Reporter:** z3ron3
- **Program:** Acronis True Image
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Symlink Attack, Privilege Escalation, TOCTOU (Time-of-check-time-of-use), Arbitrary File Deletion
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image's antivirus quarantine feature performs a privileged delete operation on empty hidden files in user-writable directories without proper validation. An attacker can create a symlink pointing to protected system files and trigger deletion through the 'Delete from PC' feature, allowing arbitrary file deletion with elevated privileges.

## Attack scenario
1. Attacker creates a test file containing EICAR string in a user-accessible location to trigger quarantine
2. Acronis AV detects and quarantines the file, leaving an empty hidden file in the original location
3. Attacker deletes the parent directory to remove the hidden file entry from filesystem
4. Attacker creates a symlink from the original file path to a protected target (e.g., C:\Windows\System32\drivers\pci.sys)
5. Attacker opens Acronis Quarantine and selects 'Delete from PC' on the quarantined file
6. Acronis executes privileged delete operation on the symlink, which follows to the target file and deletes it

## Root cause
Acronis AV performs the delete operation on the hidden empty file with elevated privileges without validating that the target path hasn't been replaced with a symlink. The race condition exists between file quarantine and deletion, allowing TOCTOU exploitation. Additionally, insufficient input validation and lack of symlink resolution checks before deletion enable the attack.

## Attacker mindset
Exploit the trust boundary between user-writable locations and privileged operations. Attackers recognize that antivirus engines often run with high privileges for cleanup operations and attempt to redirect those operations to protected system files. This is a classic privilege escalation chain: craft detectable malware → trigger quarantine → replace with symlink → trigger privileged cleanup.

## Defensive takeaways
- Always resolve and validate symlink targets before performing privileged file operations
- Implement proper privilege separation: drop to user privileges when deleting user-accessible files even in privileged context
- Use Windows APIs that follow symlinks safely (e.g., FILE_FLAG_NO_REPARSE_POINT or equivalent checks)
- Implement atomic operations or robust locking mechanisms for quarantine file deletion to prevent TOCTOU attacks
- Validate file paths at deletion time match expected quarantine structure before proceeding
- Consider using file handles opened before symlink creation rather than path-based deletion
- Log and monitor suspicious symlink activity in user directories, especially targeting system files
- Apply principle of least privilege to antivirus cleanup operations

## Variant hunting
Similar vulnerabilities exist in other antivirus/cleanup utilities that: (1) Perform privileged deletion in user-writable directories, (2) Store references to files that can be replaced with symlinks between detection and cleanup, (3) Delete temporary/quarantine copies without validating the original path, (4) Run cleanup as SYSTEM without symlink validation. Check Windows Defender cleanup, Norton deletion features, McAfee quarantine handling.

## MITRE ATT&CK
- T1190
- T1548.004
- T1547
- T1222.001

## Notes
The reporter indicated potential for escalation from privileged delete to privileged write, suggesting even greater impact possible. The use of NTFS alternate data streams (::$index_allocation) to delete folders demonstrates sophisticated understanding of Windows filesystem semantics. Requires local access but no special privileges to execute. The symlink-testing-tools reference provides proof-of-concept code for exploitation.

## Full report
<details><summary>Expand</summary>

## Summary
Acronis True Image has an Antivirus functionality which provides real-time protection and signature-based defenses against viruses and malwares.
When a file is put in Quarantine by Acronis AV it is not completely deleted from the original location, but rather the original file is emptied and reduced to 0 byte size and then made hidden.
The Quarantine has a **Delete from PC** feature which can be used to delete the selected file from Acronis AV's Quarantine folder as well as the hidden empty file from the original path. The delete operation that gets performed on Acronis AV's Quarantine folder is safe as normal user does not have access to it but the delete operation on the hidden empty file is vulnerable to a symlink attack.

## Steps To Reproduce
In this example I will try to delete ```C:\Windows\System32\drivers\pci.sys``` file which is a Windows driver file that a normal user does not have the permissions to delete.

{F989876}

[ 1 ] - Create a new folder anywhere on the system.
I created a folder named 'eicar' on my system. %userprofile% is a Windows environment variable for the user folder which is 'C:\Users\Gr33n' in my case.
```mkdir %userprofile%\Desktop\eicar```

{F989879}

[ 2 ] - Write the EICAR string in the folder created above so that Acronis's AV detects it as a threat and puts the file in Quarantine.
```echo|set /p="X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*" > %userprofile%\Desktop\eicar\eicar.exe```

{F989887}

Acronis AV will put eicar.exe into its Quarantine and make the original eicar.exe file empty and hidden.

{F989894}

[ 3 ] - Delete the 'eicar' folder which contains the hidden and empty 'eicar.exe' file as it is a prerequisite for creating a symlink.
```rmdir /S /Q %userprofile%\Desktop\eicar\eicar.exe```

{F989911}

[ 4 ] - Create a symlink from 'eicar.exe' file to the target file which is to be deleted.
To create a symlink without administrator rights, we first need to create a Mount Point such that "%userprofile%\Desktop\eicar" directory points to the "\RPC Control\" object directory and then create a symlink such that "\RPC Control\eicar.exe" file points to the target file (pci.sys in this example).

A simple way to perform this is by using James Forshaw's symboliclink-testing-tools. The tools can be built with Visual Studio 2013 or higher.
https://github.com/googleprojectzero/symboliclink-testing-tools

I have used CreateSymlink tool from symboliclink-testing-tools in this example.

```CreateSymlink.exe %userprofile%\Desktop\eicar\eicar.exe C:\Windows\System32\drivers\pci.sys```

{F989916}

[  5 ] - Open Acronis AV's Quarantine, select the file and choose the option Delete from PC.

{F989920}

Acronis AV will delete the file from its Quarantine and it will also try to delete the empty and hidden 'eicar.exe' file but because of the symlink, the delete operation will be performed on ```C:\Windows\Systen32\drivers\pci.sys``` file resulting in its deletion.

{F989937}

To delete a folder, append "::$index_allocation" to the target folder when creating symlink.
For example, ```CreateSymlink.exe %userprofile%\Desktop\eicar\eicar.exe C:\Temp::$index_allocation``` will create a symlink from 'eicar.exe' file to ```C:\Temp``` folder because of the way files are stored in NTFS and 'Temp' folder will be deleted after the attack.


## Recommendations
Impersonate as normal user when deleting the hidden and empty file.

## Escalating this vulnerability further to privileged write
I think I may have found a way to escalate this privileged delete vulnerability to privileged write to increase the severity of the issue but I will need some time to verify that.

## Impact

Attacker can delete any file or folder of his choice even when he does not have the permissions to do so.

</details>

---
*Analysed by Claude on 2026-05-24*
