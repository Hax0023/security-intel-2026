# Arbitrary Command Execution in MS-DOS 1.1 and 2.0

## Metadata
- **Source:** HackerOne
- **Report:** 5499 | https://hackerone.com/reports/5499
- **Submitted:** 2014-04-01
- **Reporter:** badca7
- **Program:** Microsoft (MS-DOS)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Arbitrary Command Execution, Improper Input Validation, OS Command Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
MS-DOS versions 1.1 and 2.0 allow unauthenticated local users to execute arbitrary system commands through the command-line interface without proper input validation. An attacker with local access can directly invoke system commands or execute batch files containing malicious instructions, leading to complete system compromise.

## Attack scenario
1. Attacker gains local access to a system running MS-DOS 1.1 or 2.0
2. Attacker enters command mode and verifies the OS version using VER command
3. Attacker confirms system responsiveness by executing benign commands like HELP
4. Attacker crafts a malicious batch file (PROGRAM_NAME.BAT) containing arbitrary system commands
5. Attacker executes the batch file using EXEC PROGRAM_NAME.BAT command
6. Batch file executes with system privileges, allowing attacker to modify files, install backdoors, or exfiltrate data

## Root cause
MS-DOS command interpreter lacks proper input validation and access controls on command execution. The EXEC command and batch file processing do not implement restrictions on which commands can be executed, and there is no distinction between privileged and unprivileged command execution.

## Attacker mindset
An attacker with local access exploits the permissive command execution model to achieve persistence and lateral movement. Given the era of MS-DOS, the attacker likely seeks to establish system control, install malware, or leverage the compromised system for further network attacks.

## Defensive takeaways
- Implement strict input validation and allowlisting for executable commands
- Enforce role-based access control (RBAC) to restrict command execution based on user privileges
- Disable or restrict batch file execution capabilities for untrusted users
- Implement command logging and monitoring to detect suspicious execution patterns
- Require authentication for privileged command execution
- Apply principle of least privilege to user accounts and processes
- Use sandboxing or virtualization to isolate execution environments

## Variant hunting
Search for similar command injection vulnerabilities in early operating systems and shell interpreters. Look for batch file processing mechanisms that lack input validation, command-line interfaces without privilege separation, and systems allowing direct execution of arbitrary binaries without restrictions.

## MITRE ATT&CK
- T1059
- T1059.003
- T1190
- T1059.001
- T1204.002

## Notes
This report appears to be historical documentation of MS-DOS vulnerabilities rather than a contemporary bug bounty submission. MS-DOS reached end-of-life decades ago. The vulnerability is endemic to early operating system design philosophy that predated modern security concepts. This case study demonstrates the importance of input validation and access controls in OS design and highlights how permissive command execution models create critical security risks.

## Full report
<details><summary>Expand</summary>

Versions 1.1 and 2.0 of MS-DOS allow a malicious actor to execute arbitrary system commands via the main application interface.

Prerequisites:
* MS-DOS 1.1 or MS-DOS 2.0 installation
* Input device (e.g. keyboard)

Steps to reproduce:
* Enter the _command mode_
* Type `VER` to make sure that the system is on of the affected versions
* Pass a known system command like `HELP` to see that the system responds correctly
* Use `EXEC PROGRAM_NAME.BAT` to execute arbitrary programs

See PoC below.

</details>

---
*Analysed by Claude on 2026-05-24*
