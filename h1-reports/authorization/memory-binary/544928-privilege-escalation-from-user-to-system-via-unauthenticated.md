# Privilege Escalation From user to SYSTEM via Unauthenticated Command Execution in EvoStream API

## Metadata
- **Source:** HackerOne
- **Report:** 544928 | https://hackerone.com/reports/544928
- **Submitted:** 2019-04-22
- **Reporter:** b0yd
- **Program:** EvoStream
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln:** Privilege Escalation, Arbitrary Command Execution, Insecure API Design, Missing Authentication
- **CVEs:** CVE-2019-15595
- **Category:** memory-binary

## Summary
EvoStream exposes an unauthenticated API on localhost:7440 that allows any local user to execute arbitrary commands via the launchProcess endpoint with SYSTEM privileges. While localhost-only access mitigates remote exploitation, the vulnerability can be chained with SSRF attacks to achieve remote code execution.

## Attack scenario
1. Attacker gains initial access as unprivileged local user on system running EvoStream service
2. Attacker discovers EvoStream API listening on http://localhost:7440
3. Attacker crafts HTTP request to /launchProcess endpoint with arbitrary command and arguments
4. EvoStream service executes command with SYSTEM privileges without authentication checks
5. Attacker achieves code execution as SYSTEM user, escalating privileges
6. Optional: Attacker chains with SSRF vulnerability in another application to trigger API calls remotely

## Root cause
EvoStream API implements the launchProcess command without requiring authentication, and the service runs with SYSTEM privileges. The API blindly executes any command passed by local clients without validation or privilege verification.

## Attacker mindset
An attacker would recognize that localhost-bound services are often treated as 'trusted' and left unguarded. They would look for processes running as SYSTEM/root that expose APIs on localhost, and search for endpoints that perform privileged operations. This vulnerability becomes critical when combined with SSRF or when an attacker has already compromised a low-privilege account.

## Defensive takeaways
- Implement authentication and authorization checks on all API endpoints, even localhost-only services
- Apply principle of least privilege: run services with minimal required permissions, not SYSTEM/root
- Validate and sanitize all command execution inputs; use allowlists rather than accepting arbitrary commands
- Disable or restrict dangerous API endpoints like launchProcess unless explicitly needed
- Implement rate limiting and logging on sensitive API operations
- Consider using OS-level isolation (AppArmor, SELinux) to restrict what SYSTEM processes can do
- Audit all localhost-bound services for privilege escalation vectors

## Variant hunting
Search for similar patterns in other services: Elasticsearch, Jenkins, Docker daemon, Kubernetes API running on localhost. Look for unauthenticated endpoints that execute system commands. Check for other EvoStream endpoints beyond launchProcess that may perform privileged operations. Investigate if service supports authentication and if it can be enabled.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1053 - Scheduled Task/Job
- T1059 - Command and Scripting Interpreter
- T1021 - Remote Service Session Initiation

## Notes
The researcher correctly identifies that localhost-only binding significantly reduces risk but does not eliminate it when SSRF vulnerabilities exist elsewhere. This is a good example of how 'defense in depth' is necessary - even localhost services need authentication. The vulnerability likely exists because EvoStream was designed for trusted networks without considering multi-tenant or hostile-user scenarios.

## Full report
<details><summary>Expand</summary>

The vulnerability, or feature depending how you look at it, is the ability to execute commands using the 
evostream API interface that is exposed on localhost:7440. Since the evostream service is running as SYSTEM a user can use the launchprocess command,  http://docs.evostream.com/2.0/launchProcess.html, to execute any binary with supplied arguments. The only thing that is keeping this "feature" from allowing remote code execution is the fact that it listens on localhost only. However, if it were couple with an SSRF, an attacker could achieve full remote code execution.

## Impact

The ability to run arbitrary commands as SYSTEM from any user.

</details>

---
*Analysed by Claude on 2026-05-24*
