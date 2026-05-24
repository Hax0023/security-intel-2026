# Ubuntu Linux Privilege Escalation (dirty_sock)

## Metadata
- **Source:** HackerOne
- **Report:** 496285 | https://hackerone.com/reports/496285
- **Submitted:** 2019-02-14
- **Reporter:** initstring
- **Program:** Ubuntu/Canonical (snapd)
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Privilege Escalation, Local Code Execution, Race Condition, Improper Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical privilege escalation vulnerability in snapd (Ubuntu's default package management service) allows any local user to immediately gain root access. The vulnerability affects all Linux distributions that include snapd, with stock Ubuntu installations being particularly vulnerable due to default inclusion of the service.

## Attack scenario
1. Attacker with unprivileged local user account logs into or gains code execution on Ubuntu system with snapd installed
2. Attacker exploits a race condition or input validation flaw in snapd's snap package installation mechanism
3. Attacker crafts a malicious snap package or exploits snapd's socket interface to bypass permission checks
4. Attacker leverages the vulnerability to execute arbitrary code in the context of the snapd daemon running as root
5. Attacker obtains immediate root/administrative access to the system
6. Attacker can now access sensitive data, install persistence mechanisms, and compromise the entire system

## Root cause
The snapd service contained a flaw in its socket interface or snap package processing that failed to properly validate user inputs or enforce permission restrictions. This allowed local users to interact with the snapd daemon in ways that bypassed normal privilege escalation checks, likely through improper handling of snap package metadata, socket requests, or race conditions in file operations.

## Attacker mindset
An attacker would recognize that snapd runs as root by default on Ubuntu systems and search for ways to communicate with or manipulate its operations. The attacker would focus on finding input validation weaknesses, race conditions, or logical flaws in the privilege separation model that snapd relies on. Given snapd's ubiquity on Ubuntu, the attacker would realize this affects a massive attack surface.

## Defensive takeaways
- Implement strict input validation and sanitization for all service socket interfaces and IPC mechanisms
- Apply principle of least privilege: ensure services only run with necessary permissions and drop privileges when possible
- Conduct thorough security audits of privilege-escalation-critical code paths, particularly in system daemons
- Implement proper race condition protections when handling file operations and package installations
- Maintain rapid patching processes for default-installed services that run with elevated privileges
- Use security sandboxing and capability restrictions to limit the blast radius of service compromises
- Test privilege escalation vectors as part of regular security testing on widely-deployed services

## Variant hunting
Hunt for similar vulnerabilities in other package management systems (apt, pacman, etc.), container runtimes (docker, containerd), and system daemons that communicate via sockets. Search for race conditions in any privileged service accepting user input. Examine other snap-related operations for permission validation issues. Test privilege boundaries in other services with default high privileges.

## MITRE ATT&CK
- T1190
- T1548
- T1548.004
- T1021.004
- T1611

## Notes
This vulnerability exemplifies the risks of default-installed privileged services. The public disclosure and rapid patching by Canonical demonstrates responsible coordinated disclosure. The availability of detailed blog posts and exploit code makes this a well-documented case study in privilege escalation. The vulnerability particularly impacted multi-user systems and shared hosting environments where any user could become root.

## Full report
<details><summary>Expand</summary>

Hi team,
This week, I have publicly disclosed the dirty_sock local root exploit affecting multiple Linux Operating Systems.

Very detailed information on the vulnerability can be found in my blog posting [here](https://initblog.com/2019/dirty-sock/).

And the exploit code can be found in my GitHub repository [here](https://github.com/initstring/dirty_sock).

The vulnerability exists in stock versions of Ubuntu Linux due to the default inclusion of the snapd service, but all Linux distributions are vulnerable if they install the package. The disclosure was handled directly with Canonical via the bug tracked [here](https://bugs.launchpad.net/snapd/+bug/1813365).

A large percentage of the Internet is safer today than it was a week ago, due to the amazing response by the team at Canonical.

## Impact

Linux relies on a functioning security model, particularly in environments shared by multiple users. The ability of any user to obtain immediate root access completely breaks this model, putting sensitive data all around the world at risk of exposure.

The exploits provided allow any user to immediately elevate to a root account.

</details>

---
*Analysed by Claude on 2026-05-24*
