# Multiple Subdomains Vulnerable to Information Disclosure via Debug Logs and Version Files

## Metadata
- **Source:** HackerOne
- **Report:** 62778 | https://hackerone.com/reports/62778
- **Submitted:** 2015-05-17
- **Reporter:** digitalsurgn
- **Program:** Udemy
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal, Debug Information Exposure, Version Number Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple Udemy subdomains expose sensitive information through publicly accessible debug.log files and version disclosure files. These files reveal the full server path structure and application versions, providing attackers reconnaissance data. The exposure affects both business.udemy.com and about.udemy.com subdomains.

## Attack scenario
1. Attacker discovers debug.log files accessible at /wp-content/debug.log on multiple Udemy subdomains
2. Attacker retrieves full filesystem paths from debug logs, mapping the server directory structure
3. Attacker accesses readme.html and plugin readme.txt files to identify installed WordPress versions and plugins
4. Attacker correlates version information with known CVEs affecting WordPress and plugins (All-in-One SEO Pack)
5. Attacker uses gathered path and version information to craft targeted exploits against identified vulnerabilities
6. Attacker achieves code execution or further information disclosure through known plugin/software vulnerabilities

## Root cause
WordPress installations with debug logging enabled and default plugin/theme readme files left publicly accessible. Insufficient file access controls and missing security headers to restrict access to sensitive information disclosure files.

## Attacker mindset
Reconnaissance-focused attacker performing passive information gathering. The exposed data significantly reduces the effort required for vulnerability discovery and exploit development by providing exact paths and software versions.

## Defensive takeaways
- Disable WordPress debug logging in production or restrict log file access via .htaccess/web server configuration
- Remove or restrict access to readme.html, readme.txt, and CHANGELOG files from web-accessible directories
- Implement .htaccess rules to block access to wp-content/debug.log and similar diagnostic files
- Configure web server to deny directory listing and disable file enumeration
- Regularly audit all subdomains for information disclosure vulnerabilities
- Use Web Application Firewall (WAF) rules to block access to common information disclosure paths
- Implement security headers and robots.txt to discourage indexing of sensitive paths

## Variant hunting
Check for error.log, access.log, and other log files in wp-content/ and root directories
Search for wp-config.php, .env, .git/config files exposed on subdomains
Enumerate subdomain patterns (support.*, help.*, api.*, admin.*) for similar exposures
Look for other plugin readme files (WooCommerce, Contact Form 7, etc.) disclosing versions
Check for version disclosures in source comments, X-Powered-By headers, or meta tags
Scan for exposed database backups, SQL dumps in wp-content/backup* directories

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1592.003 - Client Configurations
- T1087 - Account Discovery
- T1526 - Exposure of Sensitive Information
- T1592.004 - Client Version

## Notes
This is a low-complexity, high-value reconnaissance vulnerability. The exposure chains with software versioning to enable targeted exploitation. While information disclosure alone may seem low severity, it significantly reduces attacker effort for subsequent compromise. The multi-subdomain nature indicates systemic configuration issues across the organization's infrastructure.

## Full report
<details><summary>Expand</summary>

At the following address i have found debug.log file disclose the application full path onthe server.

https://business.udemy.com/wp-content/debug.log

http://about.udemy.com/wp-content/debug.log

THe below URLs showing the version number of the application :

http://about.udemy.com/readme.html

http://about.udemy.com/wp-content/plugins/all-in-one-seo-pack/readme.txt



</details>

---
*Analysed by Claude on 2026-05-24*
