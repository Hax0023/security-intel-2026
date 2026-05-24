# Debug Log File Exposure Leads to Server Full Path Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 696360 | https://hackerone.com/reports/696360
- **Submitted:** 2019-09-17
- **Reporter:** sohelahmed786
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal, Improper Access Control, Sensitive Information Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
A debug.log file was publicly accessible at https://nextcloud.com/wp-content/debug.log, exposing the server's full file path and potentially sensitive debugging information. This information disclosure vulnerability could aid attackers in understanding the application environment and planning targeted attacks.

## Attack scenario
1. Attacker discovers the debug.log file is accessible via web browser at a standard WordPress location (/wp-content/debug.log)
2. Attacker retrieves the log file and extracts full server file paths from error messages and stack traces
3. Attacker analyzes the paths to understand the server architecture, installed plugins, and directory structure
4. Attacker uses the disclosed paths to craft more targeted exploits targeting specific components or versions
5. Attacker identifies additional sensitive directories or files based on the disclosed path structure
6. Attacker launches secondary attacks with improved accuracy based on environment intelligence gathered

## Root cause
Web server misconfiguration allowing direct access to debug log files in publicly accessible directories without authentication or access controls; likely caused by WordPress debug mode being enabled in production with improper file permissions.

## Attacker mindset
Reconnaissance-focused; treating information disclosure as a stepping stone to more damaging attacks. Attackers actively scan for debug logs and error messages as they provide valuable environmental intelligence for planning targeted exploits.

## Defensive takeaways
- Never enable debug logging in production environments, or if necessary, log to files outside the web root
- Implement strict access controls (HTTP 403) on sensitive files like debug.log, .env, config files
- Configure web server (Apache/Nginx) to deny access to log files via .htaccess or server directives
- Move log files outside the web root (/var/log instead of /wp-content or /app/logs)
- Implement WAF rules to block access attempts to common debug/log file paths
- Disable WordPress debug mode in production (set WP_DEBUG to false in wp-config.php)
- Regularly audit web root permissions and file accessibility
- Use proper error handling to avoid exposing file paths in user-facing error messages

## Variant hunting
Check for other common log files: error.log, access.log, application.log in publicly accessible directories
Search for debug configuration files: .env, config.php, settings.py exposed in web root
Look for backup files (.bak, .old, .backup) containing configuration or path information
Scan for version control metadata (.git/config, .svn) that may expose paths
Check for temporary files or cache directories with debug information
Test for directory listing on /wp-content, /logs, /var/log, /tmp accessible via web

## MITRE ATT&CK
- T1190
- T1592
- T1598
- T1614
- T1538
- T1526

## Notes
Low severity but important for defense-in-depth. This is a classic reconnaissance vulnerability that provides attackers with valuable information for secondary attacks. The impact escalates significantly in combination with other vulnerabilities. Nextcloud's WordPress site exposed this, indicating the vulnerability affects the marketing/documentation infrastructure rather than the core Nextcloud application itself.

## Full report
<details><summary>Expand</summary>

At the following address i have found debug.log file disclose the application full path on the server.
https://nextcloud.com/wp-content/debug.log

## Impact

The server should not expose this log file as it could help an attacker to understand the environment that may lead to further attacks.

</details>

---
*Analysed by Claude on 2026-05-24*
