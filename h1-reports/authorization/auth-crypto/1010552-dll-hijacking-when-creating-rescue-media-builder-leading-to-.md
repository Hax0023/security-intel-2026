# DLL Hijacking in Acronis True Image 2021 Rescue Media Builder Leading to Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 1010552 | https://hackerone.com/reports/1010552
- **Submitted:** 2020-10-17
- **Reporter:** z3ron3
- **Program:** Acronis True Image 2021
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** DLL Hijacking, Insecure Library Loading, Privilege Escalation, PATH Environment Variable Manipulation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image 2021's Rescue Media Builder (MediaBuilder.exe) searches for a non-existent tcmalloc.dll file in user-writable directories and PATH-controlled locations, allowing an attacker to place a malicious DLL that executes with Administrator privileges. The vulnerability can be further exploited to achieve SYSTEM-level privilege escalation through scheduled task creation.

## Attack scenario
1. Attacker gains unprivileged user access to target Windows system running Acronis True Image 2021
2. Attacker creates malicious tcmalloc.dll containing payload (e.g., cmd.exe spawning code) and places it in %USERPROFILE%\AppData\Local\Microsoft\WindowsApps folder or adds custom folder to User PATH environment variable
3. Attacker or unprivileged user launches Rescue Media Builder via Tools tab in Acronis True Image
4. MediaBuilder.exe searches for tcmalloc.dll following standard DLL search order, locates malicious version in attacker-controlled location, and loads it with Administrator privileges
5. Malicious DLL executes within Administrator context, spawning command prompt with elevated privileges
6. Attacker leverages Administrator cmd.exe to create scheduled task running as NT AUTHORITY\SYSTEM and executes arbitrary code with SYSTEM privileges

## Root cause
MediaBuilder.exe attempts to load tcmalloc.dll without specifying absolute path or verifying DLL signature/location. The application follows standard Windows DLL search order which includes user-writable locations like %USERPROFILE%\AppData\Local\Microsoft\WindowsApps that are present in default User PATH variable. No integrity checks or code signing validation is performed on loaded DLLs.

## Attacker mindset
Privilege escalation from unprivileged user to SYSTEM level. The attacker recognizes that administrative tools running with elevated privileges are prime targets for DLL hijacking. By targeting installer/maintenance utilities like Rescue Media Builder, the attacker ensures the malicious code executes in a trusted context. The escalation to SYSTEM via scheduled tasks demonstrates understanding of Windows privilege model and legitimate system utilities that can be weaponized.

## Defensive takeaways
- Use absolute paths with SetDllDirectory() or LoadLibraryEx() with LOAD_LIBRARY_SEARCH_SYSTEM32 flag to restrict DLL search to system directories only
- Implement manifest-based DLL search order controls or delay-load DLLs for non-critical functionality
- Sign all DLLs and verify signatures at load time using Windows Code Integrity mechanisms
- Remove or minimize user-writable directories from application-specific DLL search paths
- Run applications with minimum required privileges; avoid running MediaBuilder.exe with Administrator privileges unless absolutely necessary
- Monitor and audit DLL loading attempts through ETW or Windows Defender Application Guard
- Use Windows Defender for Endpoint or similar EDR to detect suspicious DLL loads from user directories
- Implement AppLocker or Windows Defender Application Control policies to prevent unsigned DLL execution in system directories
- Educate users about risks of modifying PATH environment variables and monitor for suspicious PATH modifications

## Variant hunting
Similar DLL hijacking vulnerabilities likely exist in other Acronis products (Backup, Disk Director) that perform system-level operations. Search for other executables in Acronis installation directories that load third-party libraries like tcmalloc.dll, OpenSSL DLLs, or other common libraries without absolute path specification. Check for other administrative tools in Windows that search user-writable paths before system paths (common in older software).

## MITRE ATT&CK
- T1574.001 - Hijack Execution Flow: DLL Search Order Hijacking
- T1574.008 - Hijack Execution Flow: Path Interception by Search Order Hijacking
- T1547.001 - Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder
- T1053.005 - Scheduled Task/Job: Scheduled Task
- T1134.003 - Access Token Manipulation: Make and Impersonate Token
- T1548.002 - Abuse Elevation Control Mechanism: Bypass User Account Control

## Notes
Report demonstrates complete end-to-end exploitation chain from unprivileged user to SYSTEM. The %USERPROFILE%\AppData\Local\Microsoft\WindowsApps directory is particularly dangerous because it's standard in default PATH and provides world-writable location by default. Acronis' use of Google's tcmalloc library (non-standard for Windows) created an opportunity where legitimate Microsoft directories wouldn't contain the DLL. The researcher provided proof-of-concept code and detailed reproduction steps. Scheduled task creation via schtasks.exe from Administrator context reliably escalates to SYSTEM, making this a reliable two-stage attack.

## Full report
<details><summary>Expand</summary>

## Summary
Acronis True Image 2021 provides a **Rescue Media Builder** tool which lets the user create a bootable media to recover system if it becomes unbootable. 
```MediaBuilder.exe``` is the binary which manages such functionalities. The application is vulnerable to DLL hijacking attack because it searches for a non-existing DLL file named ```tcmalloc.dll``` (Google's custom implementation of dynamic memory allocation) in locations which can be controlled by the attacker or normal user thus placing a malicious DLL in one of the folder will result it getting loaded by ```MediaBuilder.exe``` with Administrator privileges which can be escalated to SYSTEM privileges thus resulting in Privilege Escalation.

Every Windows system contains ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder as a value in the User PATH environment variable where ```MediaBuilder.exe``` will search for the DLL if not found in the preceding Search order folders. The malicious DLL file can be placed in this folder as normal user has Full control over this folder.

{F1039832}

Even if ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder is not in User PATH environment variable, attacker can add any folder of his choice to the User PATH environment variable as this does not require Administrative permissions.

## Steps To Reproduce
I created a DLL file which when loaded spawns ```cmd.exe``` while giving information as to which application loaded the DLL, path from where the file was loaded, and user privilege. I have attached the DLL file as well as the C++ code to build the DLL below if any necessary changes are to be made.

[ 1 ] - Copy or write the DLL file named ```tcmalloc.dll```  which is to be executed in ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder.

{F1039839}

[ 2 ] - Got to Tools tab of True Image and open **Rescue Media Builder**.

{F1039840}

A ```cmd.exe``` window will open when ```MediaBuilder.exe``` loads the DLL file.
We can see in the title of the ```cmd.exe``` window that it was started with Administrator privileges. To confirm, I ran ```net session``` command which gives **There are no entries in this list** output if executed with Administrator privileges and **Access denied** if executed as a normal user.

{F1039842}

## Escalating from Administrator privileges to NT AUTHORITY\SYSTEM
[ 1 ] - From the Command Prompt that was executed after the DLL was loaded, create a scheduled task by using the Windows built-in schtasks.exe utility.

```schtasks /create /SC WEEKLY /RU "NT AUTHORITY\SYSTEM" /TN EOP /TR C:\Windows\System32\winver.exe /IT /RL HIGHEST```

{F1039843}

[ 2 ] - Run the task created in above step from the elevated Command Prompt.

```schtasks /run /I /TN EOP```

{F1039844}

```winver.exe``` can be seen executed as **NT AUTHORITY\SYSTEM** resulting in **SYSTEM** privileged code execution.

## Impact

Attackers gaining privilege to execute commands as Administrator or NT AUTHORITY\SYSTEM.

</details>

---
*Analysed by Claude on 2026-05-24*
