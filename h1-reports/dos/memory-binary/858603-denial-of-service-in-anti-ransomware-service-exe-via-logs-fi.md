# Denial of Service in anti_ransomware_service.exe via Predictable Log File Hardlink Attack

## Metadata
- **Source:** HackerOne
- **Report:** 858603 | https://hackerone.com/reports/858603
- **Submitted:** 2020-04-24
- **Reporter:** mjoensen
- **Program:** Acronis ActiveProtection
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure Temporary File, Privilege Escalation via Hard Link, Denial of Service, Unsafe File Operations
- **CVEs:** None
- **Category:** memory-binary

## Summary
anti_ransomware_service.exe creates log files in a world-writable directory with predictable naming patterns, allowing unprivileged users to create hardlinks pointing service executables to log file paths. On reboot, the service attempts to write logs to its own executable, causing a SHARING VIOLATION crash that persists across reboots.

## Attack scenario
1. Attacker enumerates existing log files in C:\ProgramData\Acronis\ActiveProtection\Logs\ (world-writable directory)
2. Attacker identifies predictable naming pattern and determines the next log file name (e.g., active_protection.2.log)
3. Attacker uses hardlink creation tool to create hardlink from predicted log file path to anti_ransomware_service.exe binary location
4. System is rebooted, triggering anti_ransomware_service startup sequence
5. Service attempts to open/write to log file, but opens its own executable instead due to hardlink
6. File I/O operation fails with SHARING VIOLATION as the executable is locked, service crashes silently and fails to restart on subsequent boots

## Root cause
Three security flaws compound to enable the attack: (1) Log directory has excessive permissions allowing unprivileged write access, (2) Log file naming follows predictable sequential pattern, (3) Service does not validate file handles or implement atomic file creation with proper permissions, leaving window for hardlink exploitation.

## Attacker mindset
Low-privilege attacker seeks to disable endpoint security protection without triggering alerts or requiring elevated privileges. Hardlink attack is stealthy—no file is modified, only linked—making detection difficult. Predictable patterns enable pre-computation of targets. Silent failure is particularly valuable as user remains unaware of disabled protection.

## Defensive takeaways
- Restrict log directory permissions to service account and administrators only; remove world-writable access
- Implement unpredictable log file naming (random suffixes, timestamps with entropy)
- Use CreateFileEx with FILE_FLAG_NO_HARDLINK or equivalent flag to prevent hardlink attacks on log operations
- Validate that opened file handles match expected file path/identity before writing sensitive data
- Implement log rotation using atomic operations and proper permission inheritance
- Add monitoring/alerting for service crashes, especially silent failures of security-critical services
- Use file integrity monitoring to detect unexpected hardlinks in sensitive directories

## Variant hunting
Search for similar patterns in other services writing to shared/world-writable directories: (1) Windows Event Log service, (2) Other antivirus/security product log operations, (3) Any service using sequential file naming without randomization, (4) Services in C:\ProgramData\ or C:\Windows\Logs with insufficient permission controls, (5) Applications creating temporary files in predictable locations during initialization

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1547 - Boot or Logon Autostart Execution
- T1036 - Masquerading
- T1070 - Indicator Removal
- T1499 - Endpoint Denial of Service
- T1068 - Exploitation for Privilege Escalation

## Notes
This attack exploits a classic TOCTOU (Time-of-Check-Time-of-Use) race condition combined with Windows hardlink semantics. The 'silent fail' aspect is critical—users have no indication their ransomware protection is disabled. The vulnerability requires only local access and no elevated privileges, making it suitable for post-compromise lateral degradation of defenses or initial attack vector by local user. James Forshaw's symbolic link tools demonstrate established hardlink attack methodologies that should be considered in threat model for any file-writing service.

## Full report
<details><summary>Expand</summary>

anti_ransomware_service.exe keeps a log in a folder where any unprivileged user has write permissions. The logs are generated in a predictable pattern allowing the unprivileged user to create a hardlink from the, not yet created, log file to the anti_ransomware_service itself. On reboot, this forces the anti_ransomware_service to try to write its log into its own process, crashing in a SHARING VIOLATION. This crash occurs on every reboot.

Steps to reproduce:
1. Download the symbolic link testing tools by James Forshaw:
    https://github.com/googleprojectzero/symboliclink-testing-tools
2. Create hardlink from the next log file in line. E.g. If active_protection.1.log exist but not active_protection.2.log, create the hardlink on number 2 and so on.
    CreateHardlink.exe "C:\ProgramData\Acronis\ActiveProtection\Logs\active_protection.2.log" "C:\Program Files (x86)\Common Files\Acronis\ActiveProtection\anti_ransomware_service.exe"
3. Reboot and verify that anti_ransomware_service.exe is not running.

## Impact

The anti_ransomware_service.exe stops working from the first reboot (step 3) and onwards. This is a silent fail meaning that the user is not aware of the failing protection of the anti_ransomware_service.exe making the user vulnerable to ransomware.

</details>

---
*Analysed by Claude on 2026-05-24*
