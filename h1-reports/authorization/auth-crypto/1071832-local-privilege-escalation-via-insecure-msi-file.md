# Local Privilege Escalation via Insecure MSI Repair in Acronis True Image

## Metadata
- **Source:** HackerOne
- **Report:** 1071832 | https://hackerone.com/reports/1071832
- **Submitted:** 2021-01-05
- **Reporter:** twvyy3vyaw8k
- **Program:** Acronis True Image
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure Temporary File Handling, DLL Hijacking, Privilege Escalation via MSI Repair, Arbitrary Code Execution
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image installs MSI files in the world-readable C:\Windows\Installer directory, allowing non-admin users to trigger repair operations via msiexec. During repair, the MSI creates a DLL in the world-writable %TEMP% folder that gets loaded by the auto-escalating MsiExec.exe process, enabling privilege escalation to SYSTEM.

## Attack scenario
1. Attacker with non-admin user privileges identifies the Acronis True Image MSI file in C:\Windows\Installer (readable by all users)
2. Attacker executes 'msiexec /fa C:\Windows\Installer\[MSI_name].msi' to trigger the repair operation
3. MSI repair process creates a temporary directory in %TEMP% and begins extracting files including schedule.dll
4. Attacker monitors %TEMP% for the created folder and replaces the legitimate schedule.dll with malicious payload before repair completes
5. MsiExec.exe auto-escalates privileges and loads the malicious schedule.dll from %TEMP%, executing attacker code as SYSTEM
6. Attacker gains SYSTEM-level code execution and can install rootkits, disable antivirus, or perform lateral movement

## Root cause
The vulnerability stems from two design flaws: (1) MSI files stored in world-readable C:\Windows\Installer directory can be accessed and manipulated by non-privileged users, and (2) MSI repair process writes DLL files to the world-writable %TEMP% directory instead of a protected location like C:\Windows\TEMP, creating a Time-of-Check-Time-of-Use (TOCTOU) window for DLL hijacking before MsiExec.exe loads it.

## Attacker mindset
An attacker seeks to bypass antivirus detection and security controls by leveraging legitimate, trusted binaries (MsiExec.exe) to execute malicious code with SYSTEM privileges. By exploiting installer-level vulnerabilities, the attacker avoids direct UAC prompts and uses the auto-escalation behavior of MSI repair operations to gain maximum privileges without user awareness.

## Defensive takeaways
- Store temporary files created during MSI repair in protected directories (C:\Windows\TEMP or other admin-only locations) rather than user-writable %TEMP%
- Implement file integrity checks or code signing verification before loading DLLs from temporary locations during repair operations
- Restrict permissions on MSI files to prevent non-admin users from executing repair operations via msiexec command-line flags
- Use atomic operations or proper locking mechanisms to prevent TOCTOU attacks during temporary file creation and loading
- Avoid relying on auto-escalation behavior of system binaries; instead use explicit, controlled privilege escalation with minimal scope
- Implement application whitelisting or code integrity checks to prevent DLL hijacking attacks
- Monitor and alert on suspicious msiexec /fa invocations from non-admin users

## Variant hunting
Search for similar patterns in other installers using MSI format, particularly vendor applications that repair themselves. Look for MSI repair operations that create temporary files in user-writable directories, execute auto-escalating binaries, or load DLLs without integrity verification. Check other Acronis products and competing backup/imaging solutions (Veeam, Carbonite, etc.) for identical vulnerability patterns.

## MITRE ATT&CK
- T1547.002
- T1547.004
- T1190
- T1574.001
- T1574.002
- T1548.002
- T1053.005
- T1036.004

## Notes
The attacker must have local access to the system but does not require administrative privileges, making this a practical attack for malware or local privilege escalation. The PoC video mentioned in the report provides valuable proof-of-concept evidence. The use of 'msiexec /fa' (force advertised repair) is a legitimate maintenance command, making this particularly dangerous as it's difficult to distinguish malicious usage from legitimate administrative repair operations. The 1.3GB size and Acronis authorship make the vulnerable MSI easy to identify.

## Full report
<details><summary>Expand</summary>

## Summary
I've found a vulnerability which leads to a local privilege escalation starting from a non-admin user.

When `True Image` client installs it drops 2 MSI files into `C:\Windows\Installer` folder.
Since this folder (by default) is readable by anyone, a non-admin user can execute commands like `msiexec /fa installer_name.msi`, which forces `installer_name.msi` to "repair" the program.

One of these 2 MSIs (i can't named it because MSI file names are random and unique for every installation) when forced to repair it creates a dll in `%TEMP%\random_name` and then, after some time, `MsiExec.exe` loads it. Since `MsiExec.exe` auto-escalate privileges when executed and `%TEMP%` is writable by anyone, this behavior could be abused to gain `nt authority\system` privileges.

## Steps To Reproduce
  1.  Open `%TEMP%` and `C:\Windows\Installer`
  2.  Locate the MSI file in the installer folder: it's 1.3 GB large and has `Acronis` as author 
  3.  Open `cmd.exe` and execute `msiexec /fa C:\Windows\Installer\installer_name.msi`.  After few seconds a new folder will appear in `%TEMP%`
  4.  Replace `schedule.dll` inside that folder with the `schedule.dll` attachment  in this report
  5.  Wait until the process finishes. After some time a UAC should prompt, just select "no"
  6.  A new cmd should pop up. Type `whoami` to confirm the new privileges


I've also recorded a PoC video in case something it's not clear.

## Recommendations
Do not use local `%TEMP%` to create `schedule.dll`, use `C:\Windows\TEMP`.

## Impact

LPEs like this one are often used by malwares to evade antivirus engines, install rootkits, spread over the network, etc...
A malware author could use this exploit to target Acronis end users.

</details>

---
*Analysed by Claude on 2026-05-24*
