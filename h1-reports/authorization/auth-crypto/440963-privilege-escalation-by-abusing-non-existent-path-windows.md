# Privilege Escalation via DLL Injection in BurpSuite through Non-existent Path

## Metadata
- **Source:** HackerOne
- **Report:** 440963 | https://hackerone.com/reports/440963
- **Submitted:** 2018-11-14
- **Reporter:** 0x09al
- **Program:** BurpSuite (Pro and Community versions)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Privilege Escalation, DLL Injection, Insecure Library Loading, CWE-427: Uncontrolled Search Path Element
- **CVEs:** None
- **Category:** auth-crypto

## Summary
BurpSuite attempts to load DLLs from a non-existent directory path (C:\Program%20Files) during startup. Since low-privileged users can create folders on the C:\ drive, an attacker can create the directory structure and inject a malicious DLL that gets loaded with elevated privileges when a privileged user runs BurpSuite.

## Attack scenario
1. Attacker logs in as a low-privileged user on a Windows system with BurpSuite installed
2. Attacker identifies the non-existent directory path that BurpSuite attempts to load DLLs from (C:\Program%20Files)
3. Attacker creates the complete directory structure leading to the target directory (amd64)
4. Attacker places a malicious DLL (e.g., sunec.dll) in the created directory tree
5. A privileged user logs in and launches BurpSuite
6. BurpSuite searches for and loads the malicious DLL from the attacker-created path with elevated privileges, executing arbitrary code

## Root cause
BurpSuite does not properly validate or secure the library loading path, attempting to load DLLs from non-existent directories. Combined with Windows default permissions that allow authenticated users to create directories on C:\, this creates a DLL preloading vulnerability. The application does not use absolute paths or validate that libraries are loaded from trusted locations.

## Attacker mindset
An attacker with local low-privileged access can escalate privileges by exploiting the application's insecure DLL loading mechanism. By understanding that Windows allows directory creation on the root drive and that applications search multiple paths during startup, the attacker can inject malicious code that executes in a higher privilege context without detection.

## Defensive takeaways
- Use absolute paths for all library loads and validate library locations before loading
- Implement manifest files to restrict DLL search paths and avoid searching in user-writable directories
- Run applications with the principle of least privilege to minimize impact of DLL injection
- Use SafeDllSearchMode or modify DLL search order to prevent searches in user-writable locations first
- Implement Code Signing and verify digital signatures before loading libraries
- Restrict file system permissions to prevent low-privileged users from creating directories on system drives (C:\)
- Monitor process creation and DLL loading events for anomalous behavior
- Apply Windows patches and use modern security features like Control Flow Guard (CFG) and Address Space Layout Randomization (ASLR)

## Variant hunting
Search for other applications that load DLLs from relative paths or non-existent directories. Look for processes that search multiple paths during startup including user-writable locations. Audit applications running with elevated privileges for similar DLL preloading vulnerabilities, particularly security tools, system utilities, and background services.

## MITRE ATT&CK
- T1547.001
- T1574.001
- T1190
- T1548
- T1134.003

## Notes
This vulnerability affects Windows 7, 10, Server 2008 R2, and Server 2012. The use of '%20' (URL-encoded space) in the path suggests the application may be handling paths incorrectly. This is a classic DLL hijacking attack enabled by insecure search path configuration. The vulnerability requires local access but results in privilege escalation from low to high privilege, making it critical for multi-user systems.

## Full report
<details><summary>Expand</summary>

# Vulnerability Overview
When Burpsuite runs, it tries to load some DLLs in the path ```C:\Program%20Files```. Because the folder doesn't exists, it can be created **by a low-privileged user** which can inject arbitrary DLL into the process when another ** privileged user** runs Burpsuite. I have verified the vulnerability in the Pro Version but I'm pretty sure the community version is also affected.

# Vulnerability Description
Monitoring the BurpSuite application in Process Monitor, we can see that it tries to load 2 DLLs from a directory that does not exist.
{F375743}

The interesting thing here is, that on Windows (verified for 7,10,Server 2008 R2 and Server 2012) every authenticated user is allowed to add new folders on the ```C:\``` drive. This in turn allows an attacker to create the folder structure and inject arbitrary DLLs to Burpsuite.

# Vulnerability Reproduction Steps
1. Login as a low-privileged user on a system which has Burpsuite installed.
{F375748}
2. Create the directory tree as shown in the image below.
{F375753}
3. Copy the attached ```sunec.dll``` file to the last directory (amd64).
4. Simulate the login of a privileged user , run Burpsuite and a message should pop up.
{F375756}

## Impact

A low privileged user can execute code as a high privileged user.

</details>

---
*Analysed by Claude on 2026-05-24*
