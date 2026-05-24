# Privilege Escalation via DLL Injection in BurpSuite through Non-existent Path

## Metadata
- **Source:** HackerOne
- **Report:** 440963 | https://hackerone.com/reports/440963
- **Submitted:** 2018-11-14
- **Reporter:** 0x09al
- **Program:** BurpSuite (PortSwigger)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Privilege Escalation, DLL Injection, Insecure Library Loading, Unquoted Search Path
- **CVEs:** None
- **Category:** auth-crypto

## Summary
BurpSuite attempts to load DLLs from a non-existent path (C:\Program%20Files) without proper validation. A low-privileged user can create this directory structure and inject malicious DLLs that execute with the privileges of any user (including administrators) who subsequently launches BurpSuite.

## Attack scenario
1. Attacker with low-privilege user account logs into a Windows system with BurpSuite installed
2. Attacker monitors BurpSuite's DLL loading behavior and identifies the non-existent search path C:\Program%20Files
3. Attacker creates the required directory structure on the C:\ drive (which allows any authenticated user to create folders)
4. Attacker places a malicious DLL (sunec.dll) in the constructed directory path
5. Administrator or privileged user launches BurpSuite on the same system
6. BurpSuite's DLL loading mechanism loads the attacker's malicious DLL from the crafted path, executing arbitrary code with elevated privileges

## Root cause
BurpSuite searches for DLLs in a non-existent directory path without validating the path exists or is secure. The application relies on the Windows DLL search order without implementing integrity checks or using absolute paths. Additionally, Windows filesystem permissions allow any authenticated user to create directories at the C:\ root level, enabling the attack vector.

## Attacker mindset
An attacker with legitimate system access exploits a trust boundary violation. By understanding application dependency loading and Windows filesystem permissions, the attacker leverages the privileged user's trust in the application to achieve code execution at a higher privilege level without requiring any user interaction beyond the privileged user running the application normally.

## Defensive takeaways
- Always use absolute, fully-qualified paths for loading dynamic libraries; avoid relative or partial paths
- Validate that DLL paths exist and are expected before loading
- Implement DLL whitelisting or signature verification before loading critical libraries
- Restrict C:\ root directory write permissions to prevent unauthorized directory creation
- Use SetDllDirectory() or similar APIs to explicitly control DLL search paths
- Avoid loading DLLs from user-writable locations or paths under user control
- Quote all paths used in library loading to prevent path interpretation vulnerabilities
- Monitor and log all failed DLL load attempts for security analysis
- Implement code signing and verify signatures of loaded DLLs at runtime

## Variant hunting
Search for other PortSwigger applications and tools that may load DLLs; audit all third-party Java/executable applications for similar non-existent path loading patterns; check for DLL loading in common penetration testing tools (Metasploit, Nmap, etc.) that might share similar architectural flaws; look for applications using spaces or encoded characters (%20) in library search paths.

## MITRE ATT&CK
- T1574.001
- T1547.001
- T1190
- T1134.003
- T1055

## Notes
The vulnerability specifically targets the space-encoded path (Program%20Files) rather than the standard 'Program Files', suggesting the application may be decoding URLs or using improper path construction. The ability to create directories at C:\ root is a Windows permission model issue that compounds the application-level vulnerability. The vulnerability affects multiple Windows versions (7, 10, Server 2008 R2, Server 2012), indicating a systemic issue in BurpSuite's library loading mechanism rather than OS-version-specific behavior.

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
