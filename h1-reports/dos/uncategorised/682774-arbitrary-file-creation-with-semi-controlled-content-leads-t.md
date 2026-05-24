# Arbitrary File Creation with Semi-Controlled Content in Steam Windows Client

## Metadata
- **Source:** HackerOne
- **Report:** 682774 | https://hackerone.com/reports/682774
- **Submitted:** 2019-08-27
- **Reporter:** xi-tauw
- **Program:** Steam (Valve)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Arbitrary File Write, Path Traversal, Privilege Escalation, Denial of Service, Symlink Attack, NTFS Reparse Point Abuse
- **CVEs:** None
- **Category:** uncategorised

## Summary
Steam Client Service (running as NT AUTHORITY\SYSTEM) writes log files without proper validation of the installation path, allowing local attackers to create arbitrary files with semi-controlled content through path traversal and NTFS reparse point abuse. This enables multiple attack vectors including horizontal/vertical privilege escalation, denial of service, and system compromise.

## Attack scenario
1. Attacker modifies the Steam InstallPath registry value (HKLM\Software\wow6432node\valve\steam) to include path traversal sequences like 'C:\test\1\..' which Windows normalizes to 'C:\test'
2. Attacker injects CRLF characters into the registry InstallPath value using binary edit mode in regedit to control log file content across multiple lines
3. Attacker creates an NTFS reparse point from a writable, empty directory (e.g., C:\test\logs) pointing to \RPC Control\ namespace using CreateSymlink.exe utility
4. Attacker creates a symlink from \RPC Control\service_log.txt to a privileged target file (e.g., C:\Windows\System32\config\SAM or startup scripts)
5. When Steam Client Service starts, it validates the DLL path and writes error logs to the symlink target with attacker-controlled payload lines embedded in the log message
6. Attacker achieves persistence, privilege escalation, or system compromise depending on the target file chosen (startup scripts, hosts file, SAM hive, etc.)

## Root cause
The Steam Client Service fails to properly validate and sanitize the InstallPath registry value before using it in file operations. Specifically: (1) Path traversal sequences are not blocked before normalization, (2) Log file paths are not validated for symlinks or reparse points, (3) No checks prevent writing to sensitive system locations, (4) The service runs with SYSTEM privileges without proper access controls on the log destination

## Attacker mindset
A local attacker with standard user privileges seeks to escalate to SYSTEM level or compromise other users' sessions. They exploit the trust relationship between Windows registry modifications and service operations, leveraging NTFS features (reparse points, symlinks) that are accessible to unprivileged users. The attack is stealthy since it abuses legitimate Steam functionality and Windows features.

## Defensive takeaways
- Validate and canonicalize all registry-sourced paths before using them in file operations; use GetFullPathName or equivalent after reading from registry
- Implement strict whitelist-based validation for installation paths; reject paths containing '..', symbolic references, or unexpected characters
- Use proper file creation APIs with flags to prevent following symlinks/reparse points (e.g., FILE_FLAG_OPEN_REPARSE_POINT with validation)
- Restrict write permissions on log directories to service-specific accounts only; use ACLs to prevent user-controlled symlink creation
- Implement path canonicalization checks after Windows path simplification to detect discrepancies between user-provided and resolved paths
- Apply principle of least privilege; avoid running services as SYSTEM when possible, use dedicated low-privilege service accounts
- Audit and validate all log file paths at runtime before opening; check for symlinks using GetFileInformationByHandle and FILE_ATTRIBUTE_REPARSE_POINT
- Disable NTFS reparse point creation in sensitive directories via Group Policy or filesystem ACLs where applicable

## Variant hunting
Search for other Valve services or third-party applications that read paths from HKLM registry without validation
Check for similar patterns in services that write logs based on registry-configured paths (installation paths, application data paths)
Identify other Windows services running as SYSTEM that accept user-influenced registry values for file operations
Look for applications that use registry values in SetCurrentDirectory or similar path-setting APIs without validation
Examine software installers that write registry paths and later use them for file operations, particularly in background services
Test any application that logs to user-configurable locations parsed from registry without proper canonicalization

## MITRE ATT&CK
- T1547.001
- T1547.004
- T1547.010
- T1547.014
- T1037.001
- T1547.004
- T1112
- T1040
- T1562.001
- T1036.003
- T1190

## Notes
Report demonstrates exceptional technical depth with step-by-step reproduction, registry manipulation, NTFS reparse point/symlink abuse, and multiple impact scenarios (DoS, horizontal/vertical EoP, hosts file hijacking). The vulnerability chain cleverly combines path traversal normalization quirks with Windows symlink capabilities accessible to unprivileged users. The CRLF injection technique allows partial control over file content while full lines are attacker-controlled through path manipulation. Root cause is inadequate trust boundaries around registry values used by privileged services. Report suggests additional unexplored impacts with XML/INI file corruption targeting Task Scheduler or DLL side-by-side loading manifests.

## Full report
<details><summary>Expand</summary>

The vulnerability allows to create arbitrary file with some crafted text (or append to existing file). Tested on actual version 5.31.28.21 (SteamService.exe filevesion info). At start of the report I describe how to trigger vulnerability, than describe how to cause any consequences.

How to trigger
-
1. Environment
Close Steam application and stop "Steam Client Service", if it is necessary.
Create folder at user-controlled space (e.g. "C:\test"). Copy files Steam.exe and steamservice.dll from origina Steam folder ("C:\Program Files (x86)\Steam"). Create empty folder "C:\test\logs"
Now go to registry and change value of "InstallPath" (HKLM\Software\wow6432node\valve\steam) to "C:\test\1\..".
This registry branch has explicit permission "Full control" for "Users".

2. Little test
Start "Steam Client service". After it has been stopped, check C:\test\logs. Here must be file "service_log.txt" with something like: "08/27/19 13:45:01 : ERROR: SteamService: Invalid file signature C:\test\1\..\bin\SteamService.dll".
Note, that "C:\test\1\..\" path equals to "C:\test" path, so Windows used second but message contain first one.
Delete service_log.txt.

3. Add some more text
Interesting fact: when Windows used path with "\..\" it is autosimplified the one. Without any check.
For example, path "C:\1\<test>\.." will be converted to "C:\1" in spite of impossible folder name.
Lets add some CLRF. It is easy from code, but it is possible via regedit. Open "HKLM\Software\wow6432node\valve\steam" and select "Modify binary data..." from context menu on "InstallPath".
Here screen (reg_clrf.png) of such changes.
So Windows will use path "C:\test", but content of "service_log.txt" will be with custom lines (see service_log_content.png).
Delete service_log.txt after test.

4. Redirect file creation
Non-admin unable to create file symlink. But there is one trick - you could combine NTFS-reparse point and object-directory symlink (both could be created without admin rights). Create reparse point "C:\test\logs" <-> "\RPC Control\", than create symlink "\RPC Control\service_log.txt" <-> any target path. This strick requre two things - folder of source file must be writeable and must be empty (this is reason of deleting service_log.txt ater every test). There is simple utility named CreateSymlink.exe from (https://github.com/googleprojectzero/symboliclink-testing-tools/ binaries could be finded on Release) that automate the trick.
More details could be readed there - https://github.com/googleprojectzero/symboliclink-testing-tools/blob/master/CreateSymlink/CreateSymlink_readme.txt
Using of utility: CreateSymlink.exe <from> <to>
In our case CreateSymlink.exe C:\test\logs\service_log.txt <target>.
Steam Client Service after start will create file <target> (or append to, if file exists) and add some lines which could be controlled (except the first and the last ones). Since Steam client service work as NT AUTHORITY\SYSTEM, almost any target could be choosed.

Impacts
-
Now I list some impact from low to high.
1. DoS
If we choose target "C:\Winwos\System32\config\SAM" or "C:\Winwos\System32\config\SECURITY" it seems OS will be broken wont be booted after shutdown.

2. Redirect of internet services
Target: C:\Windows\system32\drivers\etc\hosts
Add line: "127.0.0.1 google.com" (for example)
Result on ping.png

3. Horizontal EoP
Target: C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\run.bat
Add line: "start C:\test\1.exe"
Any files from "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp" are executed during logon of any user (this folder not writable for non-admin users). The vulnerability create bat file and all lines of the file will be executed (the first one and the last one has no effect, but payload will be executed). This is allows any user of OS force to execute any payload as another user (even administrator) when the target user logined.
Note: since line contains '\', we need add some "\.." at the end of "InstallPath" (we need "InstallPath" be equals to "C:\test")

4. Vertical EoP
Many software uses bat files for its own purposes and some times this files runs with high privileges. For example, NVIDIA and VmWare uses this. Moreover, domain users ofteh have Startup and Shutdown scripts from GroupPolicy. All of that scripts could be appended with payload.
Yes, I unable to found any script that out-of-box-Windows has, but this is not means that there are no such files.

5. Not checked but need to be mentioned.
The vulnerability allows to create xml files and ini files (with extra lines, which breaks format). I was not check that kind of files for vaildity for TaskSheduler or .manifest (Windows dll side-by-side loading) or so on. This will take so much of my time if I do this checks. so I just mention it.

## Impact

1. DoS (force OS to be broken)
2. Redirect of internet services (take control of name-ip resolution)
3. Horizontal EoP (from one user to another)
4. Vertical EoP (possible with additions, from user to NT AUTHORITY\SYSTEM)

</details>

---
*Analysed by Claude on 2026-05-24*
