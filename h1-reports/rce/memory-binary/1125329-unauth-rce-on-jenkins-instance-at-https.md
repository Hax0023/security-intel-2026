# Unauthenticated Remote Code Execution on Jenkins Instance via Script Console

## Metadata
- **Source:** HackerOne
- **Report:** 1125329 | https://hackerone.com/reports/1125329
- **Submitted:** 2021-03-14
- **Reporter:** brbsainath
- **Program:** U.S. Government Bug Bounty Program
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln:** Unauthenticated Remote Code Execution, Command Injection, Improper Access Control, Groovy Script Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
An unauthenticated attacker can execute arbitrary Groovy scripts and system commands on a publicly accessible Jenkins instance by navigating to the /_script endpoint without authentication. The vulnerable endpoint allows direct execution of Groovy code including system command execution via the .execute() method, leading to complete system compromise.

## Attack scenario
1. Attacker performs reconnaissance on U.S. Government infrastructure and identifies a Jenkins instance via SSL certificate analysis or subdomain enumeration
2. Attacker discovers the /_script endpoint is accessible without authentication requirements
3. Attacker crafts malicious Groovy code containing system command execution (e.g., 'ls'.execute().text or 'whoami'.execute().text)
4. Attacker submits the Groovy script through the vulnerable endpoint to execute arbitrary commands on the server
5. Attacker gains command execution with Jenkins process privileges and can enumerate system, install backdoors, or pivot to internal networks
6. Attacker exfiltrates sensitive data or establishes persistent access to the compromised Jenkins server

## Root cause
Jenkins script console endpoint (/_script) is enabled and accessible without authentication, combined with Groovy's powerful .execute() method that allows direct system command execution. Insufficient access controls and disabled security manager allowed arbitrary code execution.

## Attacker mindset
Opportunistic reconnaissance-driven attacker systematically probing government infrastructure for misconfigurations. Targeting Jenkins specifically due to known attack surface (script console) and high privilege context. Likely motivated by initial access, persistence, or data exfiltration objectives.

## Defensive takeaways
- Disable Jenkins script console endpoint entirely or restrict to localhost-only access
- Implement robust authentication (LDAP/SSO) with mandatory MFA for Jenkins administrative interfaces
- Run Jenkins in a sandboxed environment with restricted permissions and disable dangerous Groovy methods like .execute()
- Deploy network segmentation to restrict Jenkins access to trusted networks only
- Enable Jenkins' built-in security realm and configure authorization strategy (Matrix, Role-Based Access Control)
- Monitor and alert on access to sensitive endpoints like /_script, /_computeScriptHash
- Regularly audit Jenkins plugins and configurations for security issues
- Apply principle of least privilege - Jenkins service account should have minimal OS permissions
- Keep Jenkins and all plugins updated to latest security patches

## Variant hunting
Other Jenkins administrative endpoints without authentication (/_computeScriptHash, /scriptText, /pluginManager)
Jenkins instances with disabled security realm allowing anonymous access to build execution
Groovy postbuild plugins or other integrations with unrestricted script execution
Jenkins instances accessible via default ports (8080, 8081) on internal networks
Jenkins API endpoints lacking authentication (e.g., /queue/api/json, /api/json)
Similar script execution vulnerabilities in other CI/CD platforms (GitLab Runner, GitHub Actions, CircleCI)

## MITRE ATT&CK
- T1190
- T1059
- T1078
- T1021
- T1133

## Notes
Critical severity finding on government infrastructure. Demonstrates widespread Jenkins misconfiguration in production environments. The use of video POC suggests researcher followed responsible disclosure practices. No CVE assigned at time of report, indicating potential zero-day or known vulnerability in unpatched instance. Affects confidentiality, integrity, and availability of the Jenkins server and potentially connected infrastructure.

## Full report
<details><summary>Expand</summary>

**Description:**
Hi Team,

While Doing Recon on U.s Government Sites, I Found below asset Belongs to U.S Government (Please Check its SSL certificate to confirm or Please check attached  POC Video)
 █████████

https://███/

Attacker can execute Command Injection without Authentication.

## Impact

Unauth RCE

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Navigate to https://███████/_script
2. Please execute below commands to confirm Unauth RCE.

             Commands:  println "ls".execute().text
                                         println "whoami".execute().text
#POC

Please check Attached POC Video to follow steps (If Required)

██████

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
