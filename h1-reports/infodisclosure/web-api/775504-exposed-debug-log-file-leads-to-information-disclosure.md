# Exposed debug.log File Leads to Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 775504 | https://hackerone.com/reports/775504
- **Submitted:** 2020-01-15
- **Reporter:** muhammaddaffa
- **Program:** MariaDB
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Information Disclosure, Path Traversal/Directory Traversal, Sensitive Data Exposure, Improper Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
A debug.log file is publicly accessible at http://mariadb.org/wp-content/debug.log, exposing sensitive information including the application's full server path and database credentials. This allows unauthenticated attackers to gather reconnaissance data for further attacks.

## Attack scenario
1. Attacker discovers MariaDB website and identifies common WordPress paths like /wp-content/
2. Attacker attempts to access common debug/log files such as debug.log in the wp-content directory
3. The debug.log file is publicly accessible without authentication or access controls
4. Attacker reads the log file and extracts full server filesystem paths (/var/www/html/...)
5. Attacker identifies database username credentials stored in debug output
6. Attacker uses gathered intelligence for further reconnaissance or exploitation attempts

## Root cause
Debug logging was enabled in production environment and the log file was placed in a web-accessible directory without proper access restrictions. WordPress debug logs containing sensitive information were not protected by .htaccess or web server configuration.

## Attacker mindset
Reconnaissance-focused attacker scanning for common debug/log files in standard web application directories. Exploits default WordPress structure and misconfiguration to gather system information without authentication.

## Defensive takeaways
- Disable debug logging in production environments or restrict to non-web-accessible directories
- Move log files outside the webroot or use parent directories inaccessible via HTTP
- Implement .htaccess rules to deny access to debug.log, wp-config.php, and other sensitive files
- Configure web server to deny directory listings and access to log files
- Implement proper file permissions (644 for files, 755 for directories) at OS level
- Sanitize debug output to never include database credentials or full filesystem paths
- Use Web Application Firewall (WAF) rules to block access to common log file paths
- Implement security headers and access controls in WordPress configuration
- Regularly scan for exposed debug/log files using automated tools

## Variant hunting
Check for .log files in other web-accessible directories: /logs/, /var/log/, /tmp/
Search for error_log, access_log, debug.txt, debug.xml configurations
Enumerate backup files: debug.log.bak, debug.log.1, debug.old
Test for application-specific log files: error.log, system.log, trace.log
Check wp-content/cache/ and wp-content/plugins/ for exposed log files
Look for application configuration files that might be exposed: wp-config.php.bak, config.php
Test for other information disclosure in error pages, source code comments

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1592 - Gather Victim Host Information
- T1592.004 - Gather Victim Host Information: Client Configurations
- T1526 - Acquire Infrastructure
- T1526.005 - Acquire Infrastructure: Scan Web Content Discovery

## Notes
This is a common misconfiguration in WordPress installations. The vulnerability is particularly severe because it exposes database credentials which can be leveraged for database-level attacks. The wp-content directory is often overlooked in security hardening checklists. Similar issues may exist with other debug files, error logs, and backup files.

## Full report
<details><summary>Expand</summary>

At the following address i have found debug.log file disclose the application full path on the server. And there is database username too in debug.log

http://mariadb.org/wp-content/debug.log

## Impact

Information disclosure

</details>

---
*Analysed by Claude on 2026-05-24*
