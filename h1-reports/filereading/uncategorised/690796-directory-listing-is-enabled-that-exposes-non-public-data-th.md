# Directory Listing Enabled Exposing Server Files and Version Information on try.nextcloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 690796 | https://hackerone.com/reports/690796
- **Submitted:** 2019-09-09
- **Reporter:** tibin_sunny
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Directory Enumeration, Improper Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
Directory listing was enabled on multiple paths (/assets/, /css/, /js/) on try.nextcloud.com, allowing unauthenticated attackers to browse server files and identify the web server version. This information disclosure vulnerability could facilitate reconnaissance for further attacks against the Nextcloud instance.

## Attack scenario
1. Attacker discovers try.nextcloud.com is publicly accessible
2. Attacker navigates to common directory paths such as /assets/, /css/, /js/ in the browser
3. Web server returns directory listing instead of 403 Forbidden or index.html
4. Attacker observes file structure, version information, and available resources
5. Attacker analyzes file names and versions to identify potential vulnerabilities in dependencies
6. Attacker uses gathered intelligence to launch targeted attacks or social engineering campaigns

## Root cause
Web server (likely Apache or Nginx) has directory listing enabled via the AutoIndex module or equivalent configuration option. The server was not configured to explicitly deny directory browsing or provide index.html files for these directories.

## Attacker mindset
Reconnaissance-focused attacker performing passive information gathering. The attacker seeks to understand the target's technology stack, file structure, and version numbers to identify attack surface and potential vulnerabilities without triggering security alerts.

## Defensive takeaways
- Disable directory listing on web server (disable AutoIndex in Apache, turn off autoindex in Nginx)
- Create index.html files in all web-accessible directories to provide default content
- Implement proper access controls and deny directives for sensitive directories
- Remove or obscure server version information in HTTP headers and error messages
- Use security headers like X-Frame-Options to prevent information disclosure
- Regularly audit web server configuration against security best practices
- Implement Web Application Firewall (WAF) rules to detect and block directory enumeration attempts

## Variant hunting
Check other Nextcloud demo/test instances for similar misconfigurations
Scan for directory listing on other common paths: /uploads/, /media/, /public/, /config/
Test for path traversal vulnerabilities combined with directory listing
Identify if backup files (.bak, .zip) are exposed through directory listing
Check for .git, .env, or configuration files visible through directory enumeration
Test different URL encoding techniques to bypass directory listing protections

## MITRE ATT&CK
- T1526 - Reconnaissance: Search Open Websites/Domains
- T1589 - Gather Victim Identity Information
- T1592 - Gather Victim Host Information
- T1580 - Cloud Infrastructure Discovery

## Notes
This is a classic misconfiguration issue commonly found in staging/demo environments that receive less security attention than production systems. The 'try' subdomain suggests this is an intentionally public demo instance, but directory listing should still be disabled as a security baseline. The vulnerability combines multiple information disclosure vectors: file exposure, version disclosure, and directory structure mapping.

## Full report
<details><summary>Expand</summary>

Directory Listing is enabled on https://try.nextcloud.com and it shows out a few files on the server + The server version.

POC: https://try.nextcloud.com/assets/
        https://try.nextcloud.com/css/
        https://try.nextcloud.com/js/

## Impact

This could leak sensitive information on the server and it also allows an attacker to gain knowledge about the web-technology used by the website

</details>

---
*Analysed by Claude on 2026-05-24*
