# Exposing debug.log file leads to server full path disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 2778441 | https://hackerone.com/reports/2778441
- **Submitted:** 2024-10-12
- **Reporter:** farhad0x1
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Disclosure, Improper Access Control, Debug Information Exposure
- **CVEs:** None
- **Category:** business-logic

## Summary
A publicly accessible debug.log file on nextcloud.com exposes the server's full directory paths and sensitive debugging information without requiring authentication. This information disclosure aids attackers in reconnaissance and understanding internal server structure to plan further attacks.

## Attack scenario
1. Attacker discovers debug.log file is publicly accessible at /wp-content/debug.log
2. Attacker retrieves the file without authentication and reviews its contents
3. Attacker extracts full server directory paths and internal configuration details from log entries
4. Attacker uses disclosed paths to identify potential file inclusion, path traversal, or other file system vulnerabilities
5. Attacker maps server architecture and identifies misconfigurations for targeted exploitation
6. Attacker chains this information with other vulnerabilities to escalate attacks or gain unauthorized access

## Root cause
Debug logs were not properly restricted in production environment; insufficient access controls on sensitive files; debug mode left enabled on public-facing website without proper authentication or file permissions

## Attacker mindset
Reconnaissance and enumeration to map server infrastructure. Information disclosure provides foundation for subsequent attacks without triggering active exploitation attempts. Passive intelligence gathering to reduce detection risk.

## Defensive takeaways
- Disable debug logging in production environments entirely
- Implement strict file-level access controls (.htaccess, web server configuration) to block sensitive files
- Configure web server to deny access to debug.log and similar sensitive files before PHP execution
- Regular security audits to identify exposed debug files, logs, and configuration files
- Use environment-specific configuration to ensure debug settings differ between production and development
- Implement centralized logging to a restricted backend rather than web-accessible files
- Monitor access patterns for suspicious requests targeting common debug file paths
- Apply principle of least privilege to web server file permissions

## Variant hunting
Search for other common debug files: debug.log, error.log, access.log in web root
Check for .env, config.php, wp-config.php, settings.py files with exposed credentials
Look for backup files (.bak, .old, .backup, .zip) containing source code or configuration
Hunt for API keys, database credentials, or authentication tokens in accessible logs
Test for directory listing enabled on /wp-content/ and subdirectories
Check for git repositories or version control directories exposed (.git, .hg, .svn)
Search for other WordPress debug files like wp-debug.log in common paths

## MITRE ATT&CK
- T1018
- T1087
- T1526
- T1592

## Notes
Relatively straightforward information disclosure with no complex technical exploitation required. The vulnerability is in configuration/operational security rather than code. While severity is Medium due to passive nature, it significantly aids attackers in planning more damaging attacks. Common issue in misconfigured WordPress installations and web applications where debug mode is not properly disabled in production.

## Full report
<details><summary>Expand</summary>

## Summary:
The exposed debug.log file on the nextcloud.com website contains sensitive information, including the server’s full directory path. This type of information disclosure can assist attackers in understanding the internal structure of the server, potentially aiding them in planning further attacks, such as path traversal or file inclusion vulnerabilities.

## Steps To Reproduce:

  1. Navigate to the following URL:  https://nextcloud.com/wp-content/debug.log
  2. The debug.log file is publicly accessible without any authentication or authorization.
 3. Review the contents of the file to observe the full directory paths, which may include sensitive server details.

## Suggested Fix:
Restrict access to sensitive files such as debug.log through proper permissions or access control mechanisms.
Ensure that debug information is not exposed in production environments by disabling debug logs and utilizing error handling best practices.

  * POC attached

█████

## Impact

The exposed server paths provide an attacker with critical internal information, enabling more targeted attacks, such as exploiting file system-based vulnerabilities. An attacker could also use this information in reconnaissance to further exploit misconfigurations or other weaknesses within the server.

</details>

---
*Analysed by Claude on 2026-05-24*
