# Acronis True Image 2020 Build 22510 Nonstop Backup Service Unquoted Service Path Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 1083532 | https://hackerone.com/reports/1083532
- **Submitted:** 2021-01-21
- **Reporter:** sanderz31
- **Program:** Acronis True Image 2020
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Unquoted Service Path, Privilege Escalation, Local Privilege Escalation (LPE)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image 2020 registers the Nonstop Backup Service with an unquoted executable path containing spaces, allowing local privilege escalation to SYSTEM. An attacker can place a malicious executable in a writable directory that will be executed with SYSTEM privileges when the service starts.

## Attack scenario
1. Attacker identifies the vulnerable service path: C:\Program Files (x86)\Common Files\Acronis\CDP\afcdpsrv.exe
2. Attacker creates a malicious executable named Common.exe or Program.exe with admin user creation code
3. Attacker places the executable in a predictable directory path (C:\Program Files (x86)\Common.exe or C:\Program.exe)
4. Attacker restarts the vulnerable service or waits for system reboot
5. Windows service manager parses the unquoted path and executes the attacker's Common.exe first
6. Malicious code executes with SYSTEM privileges, creating administrator account or installing backdoor

## Root cause
Service executable path registered without quotes in Windows registry, enabling path traversal during service startup when Windows searches for the executable name with spaces

## Attacker mindset
Local user seeking persistent SYSTEM-level access through misconfigurations in third-party software installations, exploiting Windows service parsing behavior to gain administrative control

## Defensive takeaways
- Always quote service executable paths in Windows registry, especially those containing spaces
- Implement service installation validation testing for unquoted paths
- Restrict write permissions on Program Files and subdirectories to prevent executable placement
- Monitor service registry modifications and executable file creation in sensitive directories
- Enable Windows Defender Application Control (WDAC) or equivalent to restrict execution of unsigned executables
- Require signed executables in Program Files directories
- Conduct pre-deployment security testing of all installer scripts and service configurations

## Variant hunting
Search for other Acronis services or products with identical vulnerability pattern
Audit all installed third-party services for unquoted paths in HKLM\SYSTEM\CurrentControlSet\Services
Identify backup/system utility software commonly installed with unquoted service paths
Check for similar patterns in other common software vendors (VMware, Backup Exec, etc.)

## MITRE ATT&CK
- T1547.001
- T1548.004
- T1574.008
- T1569.002

## Notes
This is a classic unquoted service path vulnerability that requires local access but results in complete system compromise. The vulnerability is trivial to exploit and affects Windows systems with default configurations. The PoC demonstrates practical exploitation by creating administrator accounts, though malware installation or persistence mechanisms would be more sophisticated in real attacks. This vulnerability class has been known since Windows service inception but remains prevalent in legacy and third-party software.

## Full report
<details><summary>Expand</summary>

## Summary
Acronis True Image 2020 Nonstop Backup Service is created with an executable path that contains spaces and isn't enclosed within quotes this leads to a vulnerability known as Unquoted Service Path which allows a user to gain SYSTEM privileges.

See screenshot below.

 {F1166932} {F1166937}

## POC

The vunability can be easily exploited by placing a custom executable C:\Program Files (x86)\Common.exe or C:\Program.exe and restarting the computer/service. The executable will be executed with system privileges.

An example code for such application can be creating a new user with Administrator privilegles.

```C
#include <stdlib.h>
// i686-w64-mingw32-gcc adduser.c -o adduser.exe
int main ()
{
int i;
i = system ("net user username P@ssword! /add");
i = system ("net localgroup administrators username /add");
return 0;
}
```

## Recommendations
Add quotes to the path "C:\Program Files (x86)\Common Files\Acronis\CDP\afcdpsrv.exe" instead of C:\Program Files (x86)\Common Files\Acronis\CDP\afcdpsrv.exe

## Impact

privilege escalation on the affected system.

</details>

---
*Analysed by Claude on 2026-05-24*
