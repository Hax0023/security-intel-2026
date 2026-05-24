# Local Privilege Escalation via DLL Search-Order Hijacking in Acronis Cyber Protection Agent

## Metadata
- **Source:** HackerOne
- **Report:** 959608 | https://hackerone.com/reports/959608
- **Submitted:** 2020-08-15
- **Reporter:** mmg
- **Program:** Acronis Cyber Protection Agent
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** DLL Search-Order Hijacking, Local Privilege Escalation, Insecure Library Loading, PATH Environment Variable Abuse
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis Cyber Protection Agent version 12.5.23130 is vulnerable to DLL search-order hijacking through its systeminfo.exe utility. An attacker with write access to any folder in the PATH environment variable can place a malicious DLL that will be loaded with elevated privileges when systeminfo.exe executes. This allows arbitrary code execution with system-level privileges.

## Attack scenario
1. Attacker identifies a writable folder in the system PATH variable (e.g., C:\Python27 from a user installation)
2. Attacker places a malicious DLL with a name matching what the application seeks (e.g., snapapi.dll) in that writable PATH directory
3. Legitimate user or system process triggers execution of systeminfo.exe from Acronis
4. Windows DLL search-order mechanism locates the attacker's malicious DLL in the PATH directory before the legitimate system DLL
5. Malicious DLL is loaded into systeminfo.exe's process memory with elevated privileges
6. Attacker's code executes within the elevated context, allowing privilege escalation and further system compromise

## Root cause
The Acronis Cyber Protection Agent's systeminfo.exe utility loads DLLs without validating their location or digital signature. It relies on the default Windows DLL search-order which includes user-writable PATH directories before system directories, and does not implement secure loading mechanisms such as absolute path loading, signature verification, or DLL directory prioritization.

## Attacker mindset
A local attacker with limited privileges seeks to escalate to system level. By identifying commonly writable PATH directories (especially those from user-installed software like Python), they can plant a malicious DLL with minimal detection. This is a low-effort, high-impact attack requiring only file-system write access to a single location.

## Defensive takeaways
- Always load system DLLs using full absolute paths rather than relying on search-order
- Implement digital signature verification for all loaded DLLs before execution
- Use SetDllDirectory() or remove current directory from DLL search path to prevent hijacking
- Regularly audit PATH environment variable for writable directories with elevated process execution
- Apply principle of least privilege - avoid unnecessary elevated execution of utilities
- Monitor DLL load attempts that deviate from expected locations using EDR solutions
- Restrict write permissions on system-critical directories and PATH locations

## Variant hunting
Search for other Acronis utilities or third-party software that dynamically load DLLs without verification. Look for patterns where legitimate executables in common program folders load unverified DLLs. Check for similar hijacking vectors in other endpoint protection tools that may call system utilities during initialization.

## MITRE ATT&CK
- T1547.001
- T1574.001
- T1574.008
- T1548.002

## Notes
The vulnerability is particularly impactful because systeminfo.exe runs with elevated privileges as part of the Cyber Protection Agent. The researcher provided proof-of-concept with process monitoring evidence. The issue is exacerbated by common user installations (Python, etc.) that add writable directories to PATH. This is a textbook example of DLL search-order hijacking and represents a significant privilege escalation vector in enterprise environments.

## Full report
<details><summary>Expand</summary>

Using the latest version of Cyber Protection Agent (Version 12.5.23130) is possible to perform DLL Search-Order Hijacking.
The only requirement is to have modify rights to one folder defined in the PATH system variable, due to the order in which the DLL is loaded.

-Impact:
If a local attacker has modifying rights to one of the folders defined in the PATH system variable, will be able to load his malicious DLL, when the systeminfo.exe  starts, and execute his code with elevated privileges.

-How to Reproduce:
1.Download the latest version for the Windows Agent
URL: https://mc-beta-cloud.acronis.com/download/u/baas/4.0/12.5.23130/Cyber_Protection_Agent_for_Windows_web.exe

2.Start a procmon utility, from Sysinternal, and monitor "systeminfo.exe"
As part of my PATH system variables, I have the Python's location, which was installed in the C:\Python27 folder.

After the installation is complete, manually start the systeminfo.exe, which in my case is pointing to "C:\Program Files\Common Files\Acronis\AdvReport\systeminfo.exe" executable.
Below is an output of the process is which is looking for snapapi.dll:

systeminfo.exe	2132	CreateFile	C:\python27\snapapi.dll	NAME NOT FOUND

The test was perform on my Windows 10 Pro Version 1909 (OS Build 18363.1016).

I have attached a sample DLL, when loaded this will call C:\attacker\mmg.bat file.
You will need to create the c:\attcker folder and you can add in the mmg.bat file any command you want.
For validation i usually append in the file "whoami /all >> c:\attacker\who.txt" to confirm the security context in which my code was executed.

## Impact

The software executable is not verifying the authenticity of the DLL files, or the Search-Order before loading, thus an attacker may leverage this vulnerability to execute arbitrary code on the victim's machine, with the highest privileges.

</details>

---
*Analysed by Claude on 2026-05-24*
