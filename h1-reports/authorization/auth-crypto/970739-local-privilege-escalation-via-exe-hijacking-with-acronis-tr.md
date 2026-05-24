# Local Privilege Escalation via EXE Hijacking in Acronis True Image 2021 Installer

## Metadata
- **Source:** HackerOne
- **Report:** 970739 | https://hackerone.com/reports/970739
- **Submitted:** 2020-08-30
- **Reporter:** mmg
- **Program:** Acronis True Image 2021
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** DLL/EXE Hijacking, Insecure File Search Order, Privilege Escalation, Arbitrary Code Execution
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image 2021 installer (v25.4.30480) contains an EXE hijacking vulnerability where the atih_installer_shell_standard.exe searches for executables in the root C:\ drive before checking system directories. An attacker with local file write access can place a malicious Program.exe in C:\ to achieve arbitrary code execution with elevated installer privileges.

## Attack scenario
1. Attacker gains local write access to C:\ drive (via file upload, temp directory, or separate vulnerability)
2. Attacker places malicious Program.exe in C:\ root directory before or during installer launch
3. User initiates Acronis True Image 2021 installation or upgrade with elevated privileges
4. atih_installer_shell_standard.exe searches for Program.exe and locates attacker's malicious binary in C:\
5. Malicious executable loads and executes with installer's elevated (SYSTEM/Administrator) privileges
6. Attacker gains code execution for horizontal/vertical privilege escalation or system compromise

## Root cause
Insecure search order in executable resolution where the installer searches C:\ before protected system directories. The application fails to use fully qualified paths or API functions that enforce system directory precedence (e.g., GetModuleHandle with full path).

## Attacker mindset
Opportunistic local privilege escalation via supply chain attack on legitimate software installation process. Exploits assumption that root drive is trusted and that installer runs with elevated privileges.

## Defensive takeaways
- Always use fully qualified absolute paths for executable calls rather than relative paths or implicit search orders
- Implement proper binary signing and verification before execution
- Verify file locations are in protected directories (System32, Program Files) before execution
- Run installers with minimal necessary privileges; avoid SYSTEM context
- Use SetDllDirectory() to control DLL/EXE search paths explicitly
- Implement Application Whitelisting/Control for installation processes
- Monitor file creation in root directories and system paths during installation
- Restrict write access to C:\ root and other sensitive locations via filesystem permissions

## Variant hunting
Search for similar EXE/DLL hijacking patterns: installers calling executables by name only, setup processes loading unqualified binaries, MSI/Setup.exe files with CreateProcess calls lacking full paths, processes searching multiple path components before system directories

## MITRE ATT&CK
- T1574.008
- T1547.001
- T1190
- T1548.002
- T1036.003

## Notes
Vulnerability requires either pre-existing write access to C:\ or chaining with another write/move vulnerability. Proof of concept included a benign pop-up executable demonstrating successful hijacking. Issue affects installer execution context which typically runs elevated, making this a critical privilege escalation vector despite requiring local access.

## Full report
<details><summary>Expand</summary>

Using the latest version of Acronis True Image 2021 (25.4.30480) is possible to perform EXE Hijacking.
This could potentially allow an authorized but privileged local user to execute arbitrary code with elevated privileges on the system.

A successful attempt would require the local attacker must insert an executable file in the path of the EXE that is called.
Upon the software installation or possibly upgrade, the malicious code will be run with elevated privileges.

-Impact:
If a local attacker has modifying rights, or is chaining the attack with an arbitrary move/write vulnerability, and be able to store the file in the path from where the EXE is called, allowing to perform horizontal and/or vertical privilege escalation.

-How to Reproduce:
1.Download the latest version of  Acronis True Image 2021 installer

URL: https://download.acronis.com/AcronisTrueImage2021.exe

2.Start a procmon utility, from Sysinternal, and monitor "atih_installer_shell_standard.exe".

Start the installation
4.During the installation process the atih_installer_shell_standard.exe is looking for C:\program.exe
Below is an output:

atih_installer_shell_standard.exe	19792	CreateFile	C:\Program.exe	NAME NOT FOUND

The test was perform on my Windows 10 Pro Version 1909 (OS Build 18363.1016).

I have attached a sample exe file, that when executed will display a pop-up with the message "EXE Loaded".
This need to be stored in the C:\ just to demonstrate this behavior, before the installation process begins.

## Impact

This could potentially allow an authorized low privileged local account to execute arbitrary code in order to perform horizontal and/or vertical privilege escalation.

</details>

---
*Analysed by Claude on 2026-05-24*
