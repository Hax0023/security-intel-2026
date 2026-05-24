# DLL Hijacking in Acronis True Image 2021 Leading to Privilege Escalation via aszbrowsehelper.exe

## Metadata
- **Source:** HackerOne
- **Report:** 1004740 | https://hackerone.com/reports/1004740
- **Submitted:** 2020-10-10
- **Reporter:** z3ron3
- **Program:** Acronis True Image 2021
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** DLL Hijacking, Privilege Escalation, Insecure Library Loading, Environment Variable Manipulation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image 2021's aszbrowsehelper.exe process searches for tcmalloc.dll using an unsafe search order that includes user-writable directories like %USERPROFILE%\AppData\Local\Microsoft\WindowsApps. An unprivileged attacker can place a malicious tcmalloc.dll in this directory to achieve code execution with administrative privileges, which can be further escalated to NT AUTHORITY\SYSTEM.

## Attack scenario
1. Attacker creates a malicious DLL file that mimics tcmalloc.dll with embedded payload code
2. Attacker places the malicious DLL in %USERPROFILE%\AppData\Local\Microsoft\WindowsApps (which is user-writable and in User PATH)
3. Attacker triggers aszbrowsehelper.exe execution by accessing Acronis Secure Zone partition (via Manage Wizard or Windows Explorer browsing)
4. aszbrowsehelper.exe searches for tcmalloc.dll and loads the attacker's malicious DLL from WindowsApps directory
5. Malicious DLL executes with administrative privileges (inherited from aszbrowsehelper.exe process)
6. Attacker uses the elevated command prompt to create and execute scheduled tasks running as NT AUTHORITY\SYSTEM

## Root cause
aszbrowsehelper.exe uses unsafe DLL search order that includes user-writable directories before system directories, without implementing absolute path loading or DLL whitelisting. The application runs with administrative privileges and performs operations on Secure Zone without validating DLL integrity or location.

## Attacker mindset
Low-skill attacker can exploit this without advanced techniques. The vulnerability is trivially exploitable: place a DLL in a user-writable directory already in PATH and trigger the vulnerable application. No privilege escalation exploit knowledge required initially, though system knowledge helps with SYSTEM-level escalation via scheduled tasks.

## Defensive takeaways
- Load DLLs using absolute paths rather than relying on search order
- Remove user-writable directories from application-specific library search paths
- Implement DLL signing and validation before loading
- Use Safe DLL Search Mode or SetDllDirectory() to restrict search scope
- Run privileged operations with minimal required privileges rather than full administrative rights
- Audit and validate all directories in PATH environment variable, especially user-modifiable ones
- Use Code Integrity/DEP and binary signing to prevent unsigned DLL loading
- Monitor for suspicious DLL loading in user temp/local directories

## Variant hunting
Identify other Acronis executables that perform privileged operations and audit their DLL loading mechanisms
Search for other applications loading tcmalloc.dll or similar third-party DLLs with unsafe search orders
Check for similar patterns in backup/partition management software that runs elevated
Hunt for processes loading DLLs from %USERPROFILE%\AppData\Local\Microsoft\WindowsApps in enterprise environments
Examine other applications using Google's tcmalloc that may have similar unsafe loading patterns

## MITRE ATT&CK
- T1574.001
- T1547.001
- T1134.003
- T1053.005
- T1053.006

## Notes
This is a classic and well-documented DLL hijacking vulnerability. The WindowsApps directory is particularly insidious as it's automatically added to User PATH by Windows 10/11 and is user-writable by design. The escalation to SYSTEM via scheduled tasks demonstrates complete system compromise. Acronis likely fixed this in subsequent versions by implementing Safe DLL Search Mode or absolute path loading.

## Full report
<details><summary>Expand</summary>

## Summary
Acronis True Image 2021 lets user create a special protected partition for storing backups. ```aszbrowsehelper.exe``` process enables browsing contents of the Acronis Secure Zone partition but every time any kind of operation gets performed in Secure Zone, ```aszbrowsehelper.exe``` looks for for ```tcmalloc.dll``` (Google's custom implementation of dynamic memory allocation) DLL file according to the untrusted search order.
1) C:\Program Files (x86)\Acronis\TrueImageHome
2) Application's current working directory
3) System directory
4) 16-bit System directory
5) Windows directory
6) Directories in System PATH environment variable
7) Directories in User PATH environment variable

Every Windows system contains ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder as a value in the User PATH environment variable where ```aszbrowsehelper.exe``` will search for the DLL if not found in other Search order folders.

{F1030633}

Normal user has Full control over ```WindowsApps``` folder so anyone can place a malicious DLL file in the folder and ```aszbrowsehelper.exe``` will load that malicious DLL file resulting in its execution with **Administrative** privileges which can be escalated to **NT/AUTHORITY SYSTEM** privileges resulting in Privilege Escalation.

Even if ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder is not in User PATH environment variable, attacker can add any folder of his choice to the User PATH environment variable as this does not require Administrative permissions.

## Steps To Reproduce
An Acronis Secure Zone partition is required for this vulnerability to work.
To create a secure partition,
1) Open Acronis Secure Zone tool from Tools tab.
2) Select a partition from the disk of your choice and click Next.
3) Select how much size you want to give the secure partition and click Next.
4) Click Proceed and True Image will prompt you to reboot the system to complete the operation.

After rebooting, the Secure Zone partition will be created.

I'm assuming the partition is already created in this example.

I created a DLL file which when loaded spawns ```cmd.exe``` while giving information as to which application loaded the DLL, path from where the file was loaded, and user privilege. I have attached the DLL file as well as the C++ code to build the DLL below if any necessary changes are to be made.

[ 1 ] - Copy or write the DLL file named ```tcmalloc.dll``` in ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder.

{F1030634}

[ 2 ] - In this example, I chose to execute the DLL by opening the **Manage Acronis Secure Zone Wizard** from Tools tab in Acronis True Image but the DLL will also get loaded when  browsing the secure partition in Windows Explorer.

{F1030635}

We can see in the title of the cmd.exe window that it was started with Administrator privileges. To confirm, I ran ```net session``` command which gives **There are no entries in this list** output if executed with Administrator privileges and **Access denied** if executed as a normal user.

## Escalating from Administrator privileges to NT AUTHORITY\SYSTEM.

[ 1 ] - From the Command Prompt that was executed after the DLL was loaded, create a scheduled task by using the Windows built-in schtasks.exe utility.

```schtasks /create /SC WEEKLY /RU "NT AUTHORITY\SYSTEM" /TN EOP /TR C:\Windows\System32\winver.exe /IT /RL HIGHEST```

{F1030636}

[ 2 ] - Run the task created in above step from the elevated Command Prompt.

```schtasks /run /I /TN EOP```

{F1030637}

```winver.exe``` can be seen executed as NT AUTHORITY\SYSTEM after the task is started thus resulting in SYSTEM privileged code execution.

## Impact

Granting attackers privilege to execute commands as Administrator or NT AUTHORITY\SYSTEM.

</details>

---
*Analysed by Claude on 2026-05-24*
