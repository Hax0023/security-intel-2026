# Local Privilege Escalation via EXE Hijacking in Acronis True Image 2021 Scheduler2 Service

## Metadata
- **Source:** HackerOne
- **Report:** 971610 | https://hackerone.com/reports/971610
- **Submitted:** 2020-08-31
- **Reporter:** mmg
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper Search Path Hijacking, Unquoted Service Path, Privilege Escalation, DLL/EXE Hijacking
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image 2021's Scheduler2 service (schedul2.exe) searches for executable files in unqualified paths, specifically attempting to load C:\Program.exe during service startup. An attacker with local filesystem write access can place a malicious executable in the root of the C: drive to achieve arbitrary code execution with SYSTEM privileges.

## Attack scenario
1. Attacker gains low-privileged local access to Windows system running Acronis True Image 2021
2. Attacker identifies that Scheduler2 service searches for C:\Program.exe during startup via process monitoring
3. Attacker crafts malicious executable and places it at C:\Program.exe with appropriate permissions
4. Attacker triggers service restart (either waiting for automatic restart or forcing restart if permissions allow)
5. Service executes malicious Program.exe under SYSTEM context
6. Arbitrary code execution achieved with SYSTEM privileges enabling further lateral movement or privilege escalation

## Root cause
The application uses an unqualified executable path (C:\Program.exe) rather than a fully qualified path (e.g., C:\Program Files\Acronis\...). Windows search order resolution attempts to locate the executable in common directories including the root drive, allowing path hijacking. Additionally, the service runs with SYSTEM privileges, making it an attractive attack vector.

## Attacker mindset
An insider or low-privileged user seeks to escalate to SYSTEM level. They recognize that poorly configured service paths represent a reliable privilege escalation vector. By placing a single malicious file in an easily accessible location (C: root), they achieve reliable code execution at the highest privilege level without requiring complex exploit chains.

## Defensive takeaways
- Always use fully qualified absolute paths when launching executables from services; avoid relative or partially qualified paths
- Implement path validation and verification that executable locations match expected installation directories before execution
- Apply principle of least privilege: run services with minimum required privileges rather than SYSTEM context
- Monitor service startups and file execution for unexpected file loads from suspicious locations
- Regularly audit service configurations during security assessments to identify path hijacking vulnerabilities
- Implement application whitelisting on critical systems to prevent execution of unauthorized binaries
- Use file integrity monitoring on critical service paths to detect unauthorized modifications

## Variant hunting
Search for other Acronis services or third-party applications that may reference unqualified paths in service configurations. Examine Windows services that load DLLs or executables without full path qualification. Check for similar patterns in backup/recovery software, system utilities, and privileged services that commonly run elevated.

## MITRE ATT&CK
- T1574.008
- T1547.001
- T1190
- T1543.003
- T1548.004

## Notes
The vulnerability is trivial to exploit once discovered, requiring only file write access to C:\ drive root. The bug bounty report demonstrates clear reproduction steps with process monitor output. This represents a classic case of improper search path handling in service binaries. The fact that schedul2.exe searches C:\ before other expected locations indicates a fundamental flaw in Windows service configuration practices within Acronis' build process.

## Full report
<details><summary>Expand</summary>

Using the latest version of Acronis True Image 2021 (25.4.30480) is possible to perform EXE Hijacking.
This could potentially allow an authorized but privileged local user to execute arbitrary code with elevated privileges on the system.

A successful attempt would require the local attacker must insert an executable file in the path of the EXE that is called.
Upon the Acronis Scheduler2 Service start/restart , the malicious code will be run with SYSTEM rights.

-Impact:
If a local attacker has modifying rights, or is chaining the attack with an arbitrary move/write vulnerability, and be able to store the file in the path from where the EXE is called, allowing to execute code with SYSTEM rights.

-How to Reproduce:
1.Download the latest version of Acronis True Image 2021 installer

URL: https://download.acronis.com/AcronisTrueImage2021.exe

2.Start a procmon utility, from Sysinternal, and monitor "schedul2.exe".

3.Finish the installation
4.During the  Acronis Scheduler2 Service start/restart the executable is looking for C:\program.exe
Below is an output:

NT AUTHORITY\SYSTEM	schedul2.exe	2976	CreateFile	C:\Program.exe	NAME NOT FOUND	

The test was perform on my Windows 10 Pro Version 1909 (OS Build 18363.1016).

I have attached a sample exe file, that when executed will display a pop-up with the message "EXE Loaded". 
This need to be stored in the C:\ just to demonstrate this behavior, before the installation process begins.

I have attached a print-screen that shows the  schedul2.exe is running the sample executable.

## Impact

This could potentially allow an authorized low privileged local account to execute arbitrary code in order to perform horizontal and/or vertical privilege escalation.

</details>

---
*Analysed by Claude on 2026-05-24*
