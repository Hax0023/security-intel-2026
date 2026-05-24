# Code Injection in Slack's Windows Desktop Client via OpenSSL Config File Loading

## Metadata
- **Source:** HackerOne
- **Report:** 162955 | https://hackerone.com/reports/162955
- **Submitted:** 2016-08-24
- **Reporter:** fbogner
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Arbitrary Code Execution, Privilege Escalation, DLL Injection, Insecure File Loading, Local Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Slack's Windows Desktop Client (version 2.1.1) attempts to load OpenSSL configuration from a world-writable system path (C:\usr\local\ssl\openssl.cnf) that does not exist by default. An authenticated local attacker can create this directory structure and place a malicious OpenSSL config file that instructs OpenSSL to load arbitrary libraries, achieving code execution in other users' Slack processes with their privileges.

## Attack scenario
1. Attacker with local user account access identifies that Slack Desktop Client loads OpenSSL config from C:\usr\local\ssl\openssl.cnf
2. Attacker creates the directory structure C:\usr\local\ssl\ on the system drive (allowed for any authenticated user)
3. Attacker crafts a malicious openssl.cnf configuration file that references a malicious DLL/library path
4. Attacker places the malicious config file at C:\usr\local\ssl\openssl.cnf with appropriate payload DLL in accessible location
5. When another user logs in, Slack auto-starts and loads the malicious OpenSSL config during initialization
6. The malicious DLL is loaded into the Slack process context, executing arbitrary code with the victim user's privileges

## Root cause
Slack's Windows Desktop Client does not validate the source of the OpenSSL configuration file and loads it from an untrusted, world-writable system location without verifying file integrity or restricting the directory permissions. The application searches for the config file at C:\usr\local\ssl\openssl.cnf without checking if the path is secure or within application-controlled directories.

## Attacker mindset
An attacker seeks to compromise other users on a shared system without requiring administrative privileges. By exploiting the auto-start behavior of Slack and the application's trust in system-level config files, they can achieve persistent code execution at the privilege level of any user who logs in. This is particularly valuable on shared workstations or multi-user systems.

## Defensive takeaways
- Never load configuration files from world-writable system locations; restrict config file searches to application directories only
- Implement strict directory permission checks before loading any configuration or library files
- Use absolute paths within the application installation directory for all config/resource loading
- Implement code signing and manifest-based dependency loading to prevent DLL search order hijacking
- Consider using Windows API SetDllDirectory() or removing the current directory from DLL search path
- Validate file integrity through digital signatures before executing code or loading libraries
- Apply the principle of least privilege to auto-start applications
- On multi-user systems, isolate user processes and prevent inter-user code injection vectors
- Regularly audit file loading behavior using process monitoring tools during application startup

## Variant hunting
Search for other applications that load OpenSSL, third-party SSL libraries, or configuration files from system-level paths like C:\usr\, C:\opt\, or other unconventional locations
Review any application using bundled interpreters (Python, Node.js, Ruby) that may have similar config search patterns
Audit enterprise software and middleware that often use legacy paths for compatibility
Look for applications that trust environment variables for library/config paths without validation
Check for similar patterns in other Electron-based applications that may inherit insecure practices

## MITRE ATT&CK
- T1574.001
- T1574.008
- T1574.010
- T1547.001
- T1547.014
- T1195.002
- T1134.003
- T1548.004

## Notes
This vulnerability demonstrates the danger of loading system resources from untrusted locations. The attack is particularly effective because: (1) It requires only local user access, not admin rights; (2) It affects auto-start applications; (3) It enables privilege escalation through inter-user code injection; (4) The OpenSSL config feature is a legitimate mechanism being abused. The fix is straightforward but the impact was critical for a widely-used enterprise communication tool. The report includes proof-of-concept code and video demonstration.

## Full report
<details><summary>Expand</summary>

Hi,

This report is about a Code Injection vulnerability in Slack's Windows Desktop Client (slack.exe) that allows any local user to inject code into other user's Slack client.

It has been verified on a fully patched english Windows 7 64bit running the latest available Slack Desktop Client (2.1.1 32-Bit Direct Download). 

The issue is that slack.exe tries to load its OpenSSL configuration from the non-existing file
C:\usr\local\ssl\openssl.cnf (See Procmon screenshot). As any authenticated Windows user is allowed to
create new folders at the system drive's root, the expected folder structure can be created by anyone. 

This enables any local user to create the expected OpenSSL config file. Using this config file it is then possible to instruct OpenSSL to load additional libraries. This finally leads to arbitrary code execution in other user's slack.exe process. This is especially a problem as Slack is automatically started after logging in.

Here's a video illustrating the attack: https://owncloud.bogner.sh/s/MRXZSp0YyfK9ycf
Additionally you can download the source code and the binary version of the used payloads here: https://owncloud.bogner.sh/s/z7kbZr9STr08R73

To fix this vulnerability the OpenSSL config file should only be loaded from secure locations (like somewhere from within the application's root folder)

If you have any questions just let me know.
Florian

</details>

---
*Analysed by Claude on 2026-05-24*
