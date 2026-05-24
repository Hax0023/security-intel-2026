# Local Privilege Escalation via Symlink Attack in Acronis True Image Update

## Metadata
- **Source:** HackerOne
- **Report:** 1075449 | https://hackerone.com/reports/1075449
- **Submitted:** 2021-01-10
- **Reporter:** z3ron3
- **Program:** Acronis True Image
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Symlink/Junction Attack, Insecure Temporary File Handling, TOCTOU (Time-of-Check-Time-of-Use)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image writes log files to a predictable world-writable temporary directory during updates with SYSTEM privileges. An attacker can create a symlink from the log file path to any protected system file, allowing arbitrary file overwrite during the update process. This can lead to complete system compromise through malicious driver or DLL injection.

## Attack scenario
1. Attacker deletes existing %temp%\Acronis\DriverSetup directory to ensure clean state
2. Attacker creates empty %temp%\Acronis folder (writable by normal user)
3. Attacker creates symlink from %temp%\Acronis\DriverSetup\inst.log pointing to a critical system file (e.g., C:\Windows\System32\drivers\pci.sys or a vulnerable DLL)
4. User triggers update via Account tab in Acronis True Image or update occurs automatically
5. Acronis installer (setupapp_amd64.exe) executes with SYSTEM privileges and writes to inst.log path
6. Log writes follow symlink and overwrite the target protected file with attacker-controlled content or log data

## Root cause
The application fails to validate that the log file path is not a symlink before writing with elevated privileges. The temporary directory structure is predictable and world-writable, allowing pre-creation of malicious symlinks. No proper file handle validation or directory traversal checks are implemented.

## Attacker mindset
An attacker would recognize that update processes run with elevated privileges and target the logging mechanism as a reliable vector. By controlling the filesystem before the privileged operation occurs, the attacker exploits the race condition window and the application's trust in hardcoded paths without symlink detection.

## Defensive takeaways
- Always validate that file paths are not symlinks before writing to them, especially from privileged processes
- Use secure temporary file creation APIs (e.g., GetTempFileNameW, _mktemp_s) that return exclusive file handles
- Avoid predictable temporary directory structures; use random subdirectories or per-session isolation
- Implement proper access controls on intermediate directories in the path (deny Everyone/Users write access)
- Run installer/updater processes with minimal necessary privileges, not full SYSTEM context
- Use FILE_FLAG_NO_REPARSE_POINT flag when opening files to prevent symlink/junction following
- Implement directory traversal and symlink detection before each file operation
- Log to application-specific directories (e.g., ProgramData) with restricted permissions rather than shared %temp%
- Regularly audit and test update mechanisms for privilege escalation vectors

## Variant hunting
Search for other Acronis products with similar update mechanisms (Acronis Backup, Acronis Cyber Backup, Acronis Disk Director)
Identify other installer frameworks using predictable temp paths without symlink validation
Test Windows update, third-party software update services, and antivirus updaters for identical patterns
Hunt for applications writing driver-related files or system-critical files during updates
Check for similar vulnerabilities in products that write to %temp%\Acronis, %temp%\Microsoft, or vendor-specific folders
Test for TOCTOU race conditions in pre-update validation phases
Examine services that perform automatic updates with elevated privileges without filesystem safeguards

## MITRE ATT&CK
- T1547.008 - Boot or Logon Autostart Execution: Kernel Modules and Extensions (driver injection via pci.sys overwrite)
- T1574.012 - Hijack Execution Flow: COR_PROFILER Environment Variable (DLL injection variant)
- T1548.003 - Abuse Elevation Control Mechanism: Sudo and Sudo Caching (privilege escalation)
- T1036.006 - Masquerading: Match Legitimate Name or Location (symlink impersonation)
- T1021.001 - Remote Services: SSH (lateral movement post-compromise)
- T1027 - Obfuscation of Files or Information (malicious content in log file)
- T1036.004 - Masquerading: Masquerade Task Scheduler Task

## Notes
This is a classic symlink/TOCTOU vulnerability affecting privileged update mechanisms. The fix is straightforward but the impact is critical as it affects millions of Acronis users. The attack requires local access but no special privileges, making it a high-risk vector for privilege escalation chains. Similar patterns are common in legacy enterprise software. Windows systems with %temp% on NTFS with default permissions are particularly vulnerable.

## Full report
<details><summary>Expand</summary>

## Summary
Acronis True Image has a feature that updates itself with its newer version automatically or manually depending on the user choice. When updating, the software writes log file named ```%temp%\Acronis\DriverSetup\inst.log``` with **SYSYEM** privileges accessible to normal user . This can be escalated to privileged write vulnerability by an attacker to write to files that he does not have permission to leading to Privilege Escalation.

## Steps To Reproduce
I'm using **Acronis True Image Version 2021, Build 32010** and will update it to latest build for demonstration.
{F1151730}
In this example, I will overwrite ```C:\Windows\System32\drivers\pci.sys``` file which cannot be modified by normal user.

[ 1 ] - Delete ```%temp%\Acronis\DriverSetup``` if it already exists.
```rmdir /S /Q %temp%\Acronis\DriverSetup```

{F1151731}

[ 2 ] - Create empty ```%temp%\Acronis``` folder.
```mkdir %temp%\Acronis```

{F1151732}

[ 3 ] - Create a symlink from ```%temp%\Acronis\DriverSetup\inst.log``` file to ```C:\Windows\System32\drivers\pci.sys``` file.
```CreateSymlink %temp%\Acronis\DriverSetup\inst.log C:\Windows\System32\drivers\pci.sys```

{F1151733}

[ 4 ] - Go to Account tab in Acronis True Image and click on **A new version is available**. True Image will begin to download the latest version.
{F1151734}

Wait for True Image to download new build.
{F1151735}

[ 5 ] - The installer will open after the download is complete, click on **Update** in the installer.
{F1151736}

While installing the new build, **setupapp_amd64.exe** will write to the log file in ```%temp%\Acronis\DriverSetup\inst.log``` with **SYSTEM** privileges and because of the symlink, pci.sys file will get overwritten.

{F1151737}

This is the MD5 hash of **pci.sys** file before the attack.
{F1151738}

This is the MD5 hash of **pci.sys** file after the attack.
{F1151739}

This proves that the content of **pci.sys** file was overwritten with the content of **inst.log** file


## Tested on:
Windows 10 Home Version 20H2 (OS Build 19042.685)
Acronis True Image Version 2021, Build 32010

## Impact

Attacker can overwrite any file of his choice without permission. Further, the vulnerability can be escalated to SYSTEM privileged code execution if the content of the file can be controlled.

</details>

---
*Analysed by Claude on 2026-05-24*
