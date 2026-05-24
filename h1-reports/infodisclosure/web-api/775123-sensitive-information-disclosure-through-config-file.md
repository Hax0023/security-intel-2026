# Sensitive Information Disclosure Through Exposed Config File

## Metadata
- **Source:** HackerOne
- **Report:** 775123 | https://hackerone.com/reports/775123
- **Submitted:** 2020-01-15
- **Reporter:** a1c3venom
- **Program:** Kubernetes
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Configuration Management Error
- **CVEs:** None
- **Category:** web-api

## Summary
A configuration file containing sensitive information including credentials was publicly accessible at https://prow.k8s.io/config. This exposure allows attackers to gather reconnaissance data and potentially obtain valid credentials for unauthorized access.

## Attack scenario
1. Attacker discovers the /config endpoint through directory enumeration or public documentation
2. Attacker accesses https://prow.k8s.io/config and retrieves the configuration file
3. Attacker parses the config file to extract sensitive details such as API keys, credentials, and internal system architecture
4. Attacker uses obtained credentials to authenticate to internal systems or services
5. Attacker gains unauthorized access to resources or performs privilege escalation
6. Attacker establishes persistence or exfiltrates additional sensitive data

## Root cause
Configuration file was placed in a web-accessible directory without proper access controls or authentication requirements, likely due to misconfiguration during deployment or lack of awareness regarding sensitive data exposure risks

## Attacker mindset
Opportunistic reconnaissance - attacker systematically probes common configuration paths (/config, /settings, /.env, /config.json) looking for exposed credentials and system information that can be leveraged for further attacks

## Defensive takeaways
- Never store configuration files or credentials in web-accessible directories
- Implement strict access controls and authentication for all administrative endpoints
- Use environment variables or secure secret management systems (e.g., HashiCorp Vault, AWS Secrets Manager) for sensitive data
- Regularly audit and scan for exposed configuration files using automated tools
- Implement a policy to never commit sensitive data to version control systems
- Use .gitignore and similar exclusion patterns for configuration files
- Conduct security awareness training on secure configuration management
- Implement monitoring and alerting for access to sensitive endpoints

## Variant hunting
Search for other common config endpoint patterns: /settings, /admin/config, /api/config, /.env, /config.json, /configuration, /conf
Check for backup files: config.bak, config.old, .config~, config.php.bak
Look for exposed environment files: .env, .env.local, .env.production
Scan for exposed source code repositories with hardcoded credentials
Check for information disclosure in error messages or debug endpoints
Test for directory listing vulnerabilities that may expose additional files

## MITRE ATT&CK
- T1526
- T1580
- T1018
- T1040

## Notes
The report is brief and lacks technical depth. The reporter did not provide specific examples of what sensitive information was exposed (specific credential types, internal IPs, API endpoints). A more detailed report would have included: actual content samples (redacted), file permissions analysis, potential impact timeline, and proof of exposure duration. The vulnerability represents a common misconfiguration in CI/CD and Kubernetes environments where configuration management endpoints are inadvertently exposed.

## Full report
<details><summary>Expand</summary>

Report Submission Form

## Summary:
hello Team

while Exploring Your Site.I found Config File Is leaked
In Your Site Where Contains Sensitive Information,Credentials ETc

Vulnerable URL:- https://prow.k8s.io/config

## Impact

Attacker Is Able To Gain sensitive Information About target and Also might Get Credentials

</details>

---
*Analysed by Claude on 2026-05-24*
