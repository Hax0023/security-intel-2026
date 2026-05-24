# Local Privilege Escalation via DLL Search-Order Hijacking in Cyber Protection Agent tibxread.exe

## Metadata
- **Source:** HackerOne
- **Report:** 963103 | https://hackerone.com/reports/963103
- **Submitted:** 2020-08-20
- **Reporter:** mmg
- **Program:** Acronis Cyber Protection Agent
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DLL Search-Order Hijacking, Insecure Library Loading, Privilege Escalation, Local Code Execution
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Cyber Protection Agent (v12.5.23130) contains a DLL search-order hijacking vulnerability in tibxread.exe that loads tcmalloc.dll without validating the full path. An attacker with write permissions to any PATH-defined directory can place a malicious DLL to achieve arbitrary code execution with elevated privileges. The vulnerability requires only local filesystem access to a shared PATH directory, making it exploitable by low-privileged users.

## Attack scenario
1. Attacker identifies a world-writable or user-writable directory in the system PATH (e.g., C:\Python27)
2. Attacker crafts a malicious DLL named tcmalloc.dll matching the expected library name
3. Attacker places malicious DLL in the vulnerable PATH directory before legitimate tibxread.exe execution
4. User or system process executes tibxread.exe utility
5. Windows DLL loader searches PATH directories in order, finding attacker's malicious tcmalloc.dll first
6. Malicious DLL loads with privileges of the tibxread.exe process, potentially elevated, executing arbitrary payload

## Root cause
The application fails to use fully-qualified paths or secure DLL loading mechanisms (SafeDllSearchMode, SetDllDirectory) when loading tcmalloc.dll. The DLL search follows default Windows order: current directory, system directories, then PATH directories. By placing a malicious DLL in an attacker-writable PATH location, the loader prioritizes it over legitimate system DLLs.

## Attacker mindset
Opportunistic lateral movement and privilege escalation via low-hanging fruit. Attacker recognizes that many Windows systems have shared PATH directories with weak permissions (Python installations, shared tools directories). The attack requires no special exploits, just file-write capabilities and knowledge of DLL loading behavior.

## Defensive takeaways
- Use fully-qualified absolute paths for all DLL dependencies
- Implement SafeDllSearchMode or explicitly set DLL search directories using SetDllDirectory API
- Restrict write permissions on PATH directories to administrators only
- Sign and validate DLL integrity before loading
- Use DLL pinning or manifest-based assembly loading to lock dependencies to expected locations
- Remove unnecessary directories from PATH, especially world-writable or user-writable ones
- Audit PATH variable in deployment and production environments
- Monitor DLL load failures and unexpected DLL load sources via ETW or WMI

## Variant hunting
Search for other executables in Acronis suite and backup/recovery tools that load DLLs without fully qualified paths. Check for similar patterns in other security software. Investigate other common utility libraries (e.g., zlib.dll, libcurl.dll) that might be similarly hijackable.

## MITRE ATT&CK
- T1547.001 - Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder
- T1574.001 - Hijack Execution Flow: DLL Search Order Hijacking
- T1574 - Hijack Execution Flow
- T1190 - Exploit Public-Facing Application
- T1548.002 - Abuse Elevation Control Mechanism: Bypass User Account Control

## Notes
The vulnerability is particularly insidious because PATH directories are often legitimately writable by non-admin users (e.g., Python installations in user directories). The tibxread.exe executable suggests read operations but actually has privilege implications if run in elevated context. Reporter provides clear PoC with batch file execution validation. Version 12.5.23130 confirmed vulnerable; unclear if patched in later versions.

## Full report
<details><summary>Expand</summary>

Using the latest version of Cyber Protection Agent (Version 12.5.23130) is possible to perform DLL Search-Order Hijacking.
The only requirement is to have modify rights to one folder defined in the PATH system variable, due to the order in which the DLL is loaded.

-Impact:
If a local attacker has modifying rights to one of the folders defined in the PATH system variable, will be able to load his malicious DLL when the tibxread.exe starts, allowing a low privileged  attacker to perform horizontal and/or vertical privilege escalation.

-How to Reproduce:
1.Download the latest version for the Windows Agent
URL: https://mc-beta-cloud.acronis.com/download/u/baas/4.0/12.5.23130/Cyber_Protection_Agent_for_Windows_web.exe

2.Start a procmon utility, from Sysinternal, and monitor "tibxread.exe"
As part of my PATH system variables, I have the Python's location, which was installed in the C:\Python27 folder.

After the installation is complete, you can run the following utility "C:\Program Files\BackupClient\BackupAndRecovery\tibxread.exe" executable.
Below is an output of the process is which is looking for tcmalloc.dll:

tibxread.exe	1336	CreateFile	C:\python27\tcmalloc.dll	NAME NOT FOUND


The test was perform on my Windows 10 Pro Version 1909 (OS Build 18363.1016).

I have attached a sample DLL, when loaded this will call C:\attacker\mmg.bat file.
You will need to create the c:\attcker folder and you can add in the mmg.bat file any command you want.
For validation i usually append in the file "whoami /all >> c:\attacker\who.txt" to confirm the security context in which my code was executed.

## Impact

This could potentially allow an authorized low privileged local account to execute arbitrary code in order to perform horizontal and/or vertical privilege escalation.

</details>

---
*Analysed by Claude on 2026-05-24*
