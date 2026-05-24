# DLL Hijacking in Acronis True Image 2021 report_sender.exe Leading to Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 1008427 | https://hackerone.com/reports/1008427
- **Submitted:** 2020-10-14
- **Reporter:** z3ron3
- **Program:** Acronis True Image 2021
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** DLL Hijacking, Privilege Escalation, Unsafe DLL Search Order, Insecure PATH Environment Variable Usage
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image 2021's report_sender.exe searches for multiple DLL files in user-controllable directories without validating their origin, allowing unprivileged users to place malicious DLLs that get loaded with Administrator privileges. The vulnerability can be escalated to SYSTEM level privileges through scheduled task manipulation, enabling complete system compromise without user interaction during automatic crash reporting.

## Attack scenario
1. Attacker creates a malicious DLL with any name matching the hardcoded search list (CSUNSAPI.dll, swift.dll, SureWareHook.dll, etc.)
2. Attacker places the malicious DLL in %USERPROFILE%\AppData\Local\Microsoft\WindowsApps or adds a custom folder to the User PATH environment variable
3. User initiates feedback submission via Help menu or report_sender.exe automatically sends crash report without user interaction
4. report_sender.exe executes with Administrator privileges and searches for DLLs in the attacker-controlled directory, loading the malicious DLL
5. Malicious DLL code executes with Administrator privileges and creates a scheduled task with SYSTEM privileges
6. Attacker runs the scheduled task to achieve NT AUTHORITY\SYSTEM code execution

## Root cause
The application uses an unsafe DLL search order by looking in user-writable directories (AppData\Local\Microsoft\WindowsApps and user-modifiable PATH) before validating DLL integrity. The application runs with elevated privileges but fails to implement proper DLL loading safeguards such as full path specification, digital signature verification, or manifest-based dependency loading.

## Attacker mindset
An attacker exploits the trust boundary between privileged processes and user-controllable file system locations. They recognize that AppData\Local\Microsoft\WindowsApps is universally writable and PATH environment variables are user-modifiable, making DLL hijacking trivial. The automatic crash reporting feature eliminates even the need for user interaction, enabling wormable privilege escalation attacks.

## Defensive takeaways
- Always load DLLs using absolute paths rather than relying on search order resolution
- Implement digital signature verification for all loaded DLLs, especially in elevated processes
- Use SetDllDirectory() or remove user-writable directories from the DLL search path
- Avoid searching in user-controllable PATH directories for system-critical DLLs
- Implement manifest-based dependency loading to avoid dynamic DLL resolution
- Run crash reporting utilities with least privilege, or isolate them in low-privilege subprocesses
- Disable automatic crash reporting by default and require explicit user consent
- Regularly audit DLL loading behavior in elevated processes using tools like Procmon
- Never hardcode DLL names without full path qualification

## Variant hunting
Search for other Acronis applications or system utilities that use report_sender.exe or similar feedback mechanisms
Check for similar DLL hijacking patterns in other backup/system software (Veeam, Commvault, Backup Exec)
Identify other executables running with elevated privileges that load DLLs via search order
Review Windows services that may search for DLLs in user-modifiable directories
Check for antivirus/EDR software with similar feedback mechanisms
Analyze other Acronis components (TrueSync, Cyber Backup) for identical vulnerability patterns

## MITRE ATT&CK
- T1574.001 - Hijack Execution Flow: DLL Search Order Hijacking
- T1574.008 - Hijack Execution Flow: Execution via Alternative Extension
- T1547.001 - Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder
- T1053.005 - Scheduled Task/Job: Scheduled Task
- T1134.003 - Access Token Manipulation: Make and Impersonate Token
- T1134.004 - Access Token Manipulation: Parent PID Spoofing
- T1548.002 - Abuse Elevation Control Mechanism: Bypass User Account Control

## Notes
This vulnerability is particularly severe because: (1) it requires no administrative access to exploit, (2) it can be triggered automatically without user interaction, (3) it achieves SYSTEM-level code execution, (4) the %USERPROFILE%\AppData\Local\Microsoft\WindowsApps directory is universally present and writable, and (5) the hardcoded DLL names suggest copy-paste patterns from cryptographic libraries indicating systemic design flaws. The report demonstrates a complete attack chain from user-level execution to SYSTEM privileges, making this a critical privilege escalation vulnerability suitable for wormable malware distribution.

## Full report
<details><summary>Expand</summary>

## Summary
Acronis True Image 2021 has a feature to send user feedback or application crash report to Acronis Support staff. ```report_sender.exe``` is the binary which manages such functionalities. The application is vulnerable to DLL hijacking attack because it searches for non-existing DLL files in locations which can be controlled by the attacker or normal user thus placing a malicious DLL in one of the folder will result it getting loaded by ```report_sender.exe``` with Administrator privileges which can be escalated to SYSTEM privileges thus resulting in a Privilege Escalation.

```report_sender.exe``` looks for the following DLL files and name of any file can be used to exploit the vulnerability.

+ CSUNSAPI.dll
+ swift.dll
+ nfhwcrhk.exe
+ SureWareHook.dll
+ aep.dll
+ atasi.dll
+ nusonsll.dll
+ ubsec.dll

Every Windows system contains ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder as a value in the User PATH environment variable where ```report_sender.exe``` will search for the DLL if not found in the preceding Search order folders. The malicious DLL file can be placed in this folder as normal user has Full control over this folder.

{F1035152}

Even if ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder is not in User PATH environment variable, attacker can add any folder of his choice to the User PATH environment variable as this does not require Administrative permissions.

## Steps To Reproduce
I created a DLL file which when loaded spawns ```cmd.exe``` while giving information as to which application loaded the DLL, path from where the file was loaded, and user privilege. I have attached the DLL file as well as the C++ code to build the DLL below if any necessary changes are to be made.

[ 1 ] - Copy or write the DLL file with any name from the above specified DLL file names in ```%USERPROFILE%\AppData\Local\Microsoft\WindowsApps``` folder. I chose ```ubsec.dll``` in this example.

{F1035153}

[ 2 ] - Go to the **Help** tab in Acronis True Image and click on **Send feedback**.

{F1035539}

[ 3 ] - Fill in the details of the feedback and click on **Send**.

{F1035561}

A ```cmd.exe``` window will open when ```report_sender.exe``` loads the DLL file.
We can see in the title of the ```cmd.exe``` window that it was started with **Administrator** privileges. To confirm, I ran ```net session``` command which gives **There are no entries in this list** output if executed with Administrator privileges and **Access denied** if executed as a normal user.

{F1035584}

## Escalating from Administrator privileges to NT AUTHORITY\SYSTEM.
[ 1 ] - From the Command Prompt that was executed after the DLL was loaded, create a scheduled task by using the Windows built-in schtasks.exe utility.

```schtasks /create /SC WEEKLY /RU "NT AUTHORITY\SYSTEM" /TN EOP /TR C:\Windows\System32\winver.exe /IT /RL HIGHEST```

{F1035585}

[ 2 ] - Run the task created in above step from the elevated Command Prompt.

```schtasks /run /I /TN EOP```

{F1035586}

```winver.exe``` can be seen executed as **NT AUTHORITY\SYSTEM** resulting in SYSTEM privileged code execution.

## Impact

Attackers gaining privilege to execute commands as Administrator or NT AUTHORITY\SYSTEM.

This attack can also work without any user interaction when ```report_sender.exe``` automatically sends crash report.

</details>

---
*Analysed by Claude on 2026-05-24*
