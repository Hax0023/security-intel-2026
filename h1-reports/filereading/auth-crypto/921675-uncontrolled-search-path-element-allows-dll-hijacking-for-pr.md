# DLL Hijacking in GlassWire Service Allows Privilege Escalation to SYSTEM

## Metadata
- **Source:** HackerOne
- **Report:** 921675 | https://hackerone.com/reports/921675
- **Submitted:** 2020-07-12
- **Reporter:** dawouw
- **Program:** GlassWire
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** DLL Hijacking, Uncontrolled Search Path Element, Privilege Escalation, Arbitrary Code Execution
- **CVEs:** None
- **Category:** auth-crypto

## Summary
GlassWire 2.2.210.0 loads nine DLLs from the PATH environment variable without verification in the SYSTEM-privileged GWCtlSrv.exe service and one additional DLL in the user-level GUI. An authenticated attacker can place a malicious DLL in a writable PATH directory to achieve arbitrary code execution with SYSTEM privileges or user-level persistence.

## Attack scenario
1. Attacker gains local access to a GlassWire-installed system (authenticated)
2. Attacker identifies writable directories in the PATH environment variable (e.g., Python installation directories)
3. Attacker crafts a malicious DLL with the same name as one loaded by GWCtlSrv.exe (e.g., swift.dll, CSUNSAPI.dll)
4. Attacker places the malicious DLL in the writable PATH directory before the legitimate GlassWire installation directory
5. System boots or service restarts, triggering GWCtlSrv.exe execution as SYSTEM
6. GWCtlSrv.exe searches PATH and loads attacker's malicious DLL first, executing arbitrary code with SYSTEM privileges

## Root cause
GlassWire's service and GUI components use implicit DLL loading without full path specification, relying on Windows' default DLL search path which includes user-writable directories. The application fails to either: (1) specify absolute paths for DLL loading, (2) validate DLL signatures, or (3) restrict search paths to protected system directories.

## Attacker mindset
An authenticated local attacker leverages predictable DLL loading behavior in privileged services. The presence of commonly-installed tools (Python, Java) that add writable directories to PATH creates exploitable conditions. This is a low-effort, high-impact technique requiring only file placement in accessible directories.

## Defensive takeaways
- Always use absolute paths or SetDllDirectory() to control DLL loading for privileged services
- Implement DLL signature verification before loading, especially for SYSTEM-level processes
- Remove user-writable directories from system PATH or position them after system directories
- Apply principle of least privilege - avoid running services as SYSTEM when lower privileges suffice
- Conduct regular binary analysis to identify implicit DLL dependencies and loading patterns
- Monitor PATH environment variable changes and DLL loading in privileged processes
- Use AppLocker or similar mechanisms to restrict DLL execution in service contexts

## Variant hunting
Search for other services using implicit DLL loading patterns (LoadLibrary without full paths)
Identify all executables running as SYSTEM or elevated that perform DLL loading
Check for hardcoded DLL names in service code that could be hijacked
Analyze installer packages to understand DLL dependency chains
Test other GlassWire components (plugins, extensions) for similar patterns
Investigate GUI component (Wtsapi32.dll.dll typo) - test if Windows API confusion is exploitable
Search for similar patterns in other network security/monitoring tools

## MITRE ATT&CK
- T1547.001
- T1547.010
- T1574.001
- T1134.005
- T1547.004
- T1053.005

## Notes
The report identifies 9 DLLs loaded by the service (including duplicate nfhwcrhk.dll) and 1 by the GUI. The GUI component loads 'Wtsapi32.dll.dll' which appears to be a malformed name (double .dll extension), suggesting possible developer error. The PoC references external DLL creation resources. Many loaded DLLs (swift, aep, ubsec, nuronssl) appear to be cryptographic or hardware security module libraries, suggesting the application's security features themselves may contain these vulnerabilities. This is a CAPEC-233 (Search Path Injection) attack.

## Full report
<details><summary>Expand</summary>

GlassWire contains a DLL hijacking vulnerability that could allow an authenticated attacker to execute arbitrary code on the targeted system. The vulnerability exists due to GlassWire loading DLL files from the PATH environment variable without verification. The machine should have at least one writable PATH directory for the privilege escalation to work (e.g. having Python, Java, etc. installed).
Nine different DLL's are loaded by the GlassWire Service (GWCtlSrv.exe) as SYSTEM. 
One DLL is loaded by the GUI (GlassWire.exe) as the currently logged in user.

Class: Privilege Escalation [CAPEC-233]
Class: Uncontrolled Search Path Element [CWE-427]

**Affected Product**
GlassWire 2.2.210.0

**Proof of Concept**
Usually, Python is prepended to the PATH environment (Path=C:\Python38\Scripts\;C:\Python38\;..). For my ease and workflow, I prepended my folder to it (C:\Dima\;). Place the [x86 DLL](https://secret.club/2020/04/23/directory-deletion-shell.html) in one of the writable folder paths.


*C:\Program Files (x86)\GlassWire\GWCtlSrv.exe*
GlassWire (32bit) loads the following DLLs during boot as SYSTEM:
- swift.dll
- CSUNSAPI.dll
- nfhwcrhk.dll
- SureWareHook.dll
- aep.dll
- nfhwcrhk.dll
- atasi.dll
- nuronssl.dll
- ubsec.dll

{F904704}
{F904728}


*C:\Program Files (x86)\GlassWire\GlassWire.exe*
Glasswire GUI (32bit) loads the following DLL after user logon as the current user:
- Wtsapi32.dll.dll

{F904730}


I hope this helps. Please let me know if you require more information.

Kind regards,
Dima van de Wouw
[Outflank](https://outflank.nl/)

## Impact

Successful exploitation of the GlassWire service allows an attacker to gain SYSTEM privileges and inject into the GlassWire service process at boot.
Successful exploitation of the GlassWire GUI allows a user to gain persistence. On shared machines, this would allow a user to move laterally to sessions of other users.

</details>

---
*Analysed by Claude on 2026-05-24*
