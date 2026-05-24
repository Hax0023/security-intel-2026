# Race Condition (TOCTOU) in NordVPN Service Leading to Local Privilege Escalation via Arbitrary DLL Loading

## Metadata
- **Source:** HackerOne
- **Report:** 768110 | https://hackerone.com/reports/768110
- **Submitted:** 2020-01-04
- **Reporter:** hexgold
- **Program:** NordVPN
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Race Condition (TOCTOU), Privilege Escalation, Arbitrary Code Execution, Path Traversal, DLL Injection
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A time-of-check-time-of-use (TOCTOU) race condition exists in NordVPN's service when validating OpenVPN configuration files. An attacker can exploit the window between validation and execution to swap a legitimate config with one containing malicious OpenSSL engine directives that trigger arbitrary DLL loading. Since the NordVPN service runs as SYSTEM, the attacker gains code execution with the highest privileges.

## Attack scenario
1. Attacker gains local user access to the target system (low-privileged account)
2. Attacker calls the NordVPN WCF service with a crafted ServerDomain parameter pointing to a writable location containing a benign OpenVPN config file
3. NordVPN service validates the configuration file at the attacker-controlled path and approves it
4. Using NTFS opportunistic locks (oplock) via tools like BaitAndSwitch, attacker detects the validation read operation
5. In the race condition window between validation and OpenVPN process launch, attacker swaps the config file with a malicious version containing an OpenSSL engine directive pointing to attacker's DLL
6. NordVPN service launches OpenVPN with the swapped malicious configuration, causing OpenVPN to load the attacker's DLL with SYSTEM privileges

## Root cause
The vulnerability stems from three design flaws: (1) No validation of the ServerDomain parameter allows arbitrary paths; (2) OpenVPN config validation and execution are separate operations with a time gap; (3) Lack of path canonicalization/isolation means the config file can be replaced after validation but before use. The removal of the 'engine' whitelist in version 6.26.8.0 was incomplete mitigation.

## Attacker mindset
A local attacker with low privileges seeks to escalate to SYSTEM level. Rather than finding a new vulnerability, they exploit the gap between security checks and their enforcement. By controlling the filesystem path and leveraging Windows NTFS oplock mechanics, they create a detectable race condition that is reliably exploitable with timing precision.

## Defensive takeaways
- Always perform security checks immediately before the operation they protect, not earlier; avoid time gaps between validation and use
- Implement atomic operations or use file locks to prevent TOCTOU races; consider using OS-level mechanisms like file moves to trusted locations
- Validate user-supplied paths strictly; whitelist expected directories and use Path.Combine() with validation that result stays within allowed bounds
- Copy security-critical files to protected directories (SYSTEM-only access) before validation to eliminate attacker race windows
- Use cryptographic hashes or secure file handles to ensure the validated file is the same one being executed
- Disable or restrict NTFS opportunistic locks for privileged service operations where applicable
- Implement comprehensive input validation on WCF service parameters, not just configuration content

## Variant hunting
Hunt for similar TOCTOU patterns in other services: (1) Check services that construct file paths from user parameters and later access those files; (2) Search for validate-then-use code patterns with file I/O separated across function calls; (3) Examine services that load plugins/DLLs where the plugin location can be influenced by user input; (4) Audit other VPN clients (OpenVPN, Windscribe, ExpressVPN) for identical patterns; (5) Test Windows services that perform staged file operations (read config, execute, etc.) for oplock exploitation

## MITRE ATT&CK
- T1547.001 Registry Run Keys / Startup Folder
- T1574.001 DLL Search Order Hijacking
- T1574.011 Services Registry Permissions Weakness
- T1134.003 Access Token Manipulation - Make and Impersonate Token
- T1548.004 Abuse Elevation Control Mechanism - Elevated Execution with Prompt
- T1036.006 Masquerading - Space after Filename
- T1566.002 Phishing - Spearphishing Link

## Notes
The vulnerability demonstrates the critical importance of atomic file operations in privilege-sensitive code. The attacker's use of James Forshaw's BaitAndSwitch tool showcases how NTFS oplock primitives enable reliable race condition exploitation. The fact that version 6.26.8.0 attempted mitigation by removing the 'engine' option from whitelist but failed to address the underlying TOCTOU flaw highlights how incomplete security patches can leave systems vulnerable. This is a textbook example of why 'check-then-use' patterns are fundamentally insecure for privilege escalation scenarios.

## Full report
<details><summary>Expand</summary>

## Summary:
A vulnerability exists in the NordVPN service, which is installed as part of the NordVPN Windows app. By exploiting a race condition in the NordVPN service it is possible to launch OpenVPN with a user-supplied configuration file. By setting an OpenSSL engine name within this configuration file, it is possible to cause OpenVPN to load an arbitrary DLL. The NordVPN service is running with SYSTEM privileges and is responsible for starting the OpenVPN process. Consequently, the code in the attacker's DLL will also run with SYSTEM privileges.

This issue exists because it is possible to pass the NordVPN service an arbitrary path via the `DomainName` parameter. The service will use the domain name to construct a path to the location of a OpenVPN configuration file. The configuration file is validated before starting OpenVPN. If the path is controlled by a local attacker it is possible to trigger a race condition. In the time after the validation of the NordVPN service and before starting OpenVPN, it is possible to switch the validated configuration with a different one containing configuration options that are normally not allowed.

## Steps To Reproduce:
Attached PowerShell Module can be used to exploit this issue. Example usage:

```
Import-Module .\Invoke-ExploitNordVPNConfigLPE.psd1
Invoke-ExploitNordVPNConfigLPE "net user backdoor P@ssword /add" "net localgroup administrators backdoor /add"## Supporting 
```

## Vulnerability details:
NordVPN 6.26.8.0 mitigates a different local privilege escalation vulnerability by removing the `engine` option from the whitelist with allowed OpenVPN options. No validation of the `ServerDomain` parameter of the `VpnConnectionProxy` WCF model was added to prevent the loading of OpenVPN configuration files from arbitrary locations.

A time-of-check-time-of-use (TOCTOU) race condition exists in the way OpenVPN configuration files are validated/used. First the NordVPN service will validate the OpenVPN configuration that is located at the path that is constructed using the `ServerDomain` parameter. If the configuration file is valid, OpenVPN is launched with the same path. In the time between the validation and launching, the configuration file can be swapped for another one, and OpenVPN will used that file instead of the one that was validated by the NordVPN service.

NTFS [opportunistic locks](https://docs.microsoft.com/en-us/windows/win32/fileio/opportunistic-locks) can be used to exploit this issue by detecting that a process is accessing a certain file. When this occurs, the file can be swapped for another file. The second read will thus return different content. The [BaitAndSwitch](https://github.com/googleprojectzero/symboliclink-testing-tools/releases) from [James Forshaw](https://twitter.com/tiraniddo) does exactly this and can be used to exploit this issue.

## Possible fix(es):
- Perform strict validation of the `ServerDomain` parameter.
- Copy the OpenVPN configuration file to a folder that is only accessible by the SYSTEM user. Give the configuration file a unique (random) name and validate it after the file has been copied. Start OpenVPN with the configuration file from this path.
- After constructing the path  with `Path.Combine()` validate if the path starts with the value of `PrebundledOpenVpnConfig.BundleDirectory()`.

## Impact

A local low privileged user can exploit this issue to run arbitrary code with LocalSystem privileges.

</details>

---
*Analysed by Claude on 2026-05-24*
