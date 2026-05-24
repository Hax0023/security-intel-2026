# Information Disclosure - Application and Plugin Version Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 78765 | https://hackerone.com/reports/78765
- **Submitted:** 2015-07-25
- **Reporter:** shekhar93
- **Program:** Udemy
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Sensitive Information Exposure, Version Number Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The Udemy application exposed sensitive version information through publicly accessible files including readme.html and plugin readme.txt files. This disclosure allows attackers to identify the specific versions of the application and plugins in use, enabling targeted exploitation of known vulnerabilities.

## Attack scenario
1. Attacker discovers publicly accessible readme.html file at about.udemy.com/readme.html
2. Attacker identifies application version number from the exposed file
3. Attacker discovers WordPress plugin All-In-One SEO Pack readme.txt at wp-content/plugins path
4. Attacker identifies specific plugin version number from the readme file
5. Attacker correlates disclosed versions with known public vulnerabilities in CVE databases
6. Attacker develops or obtains exploit code for identified vulnerable versions and initiates targeted attack

## Root cause
Failure to restrict or remove publicly accessible configuration, readme, and documentation files that contain version information. Common causes include default WordPress installations, inadequate file access controls, and lack of security hardening during deployment.

## Attacker mindset
Reconnaissance-focused. Attackers leverage version disclosure for enumeration and to identify attack surface. Knowing specific versions drastically reduces attack complexity by enabling use of public exploits without blind exploitation or version fingerprinting.

## Defensive takeaways
- Remove or restrict access to readme.html, readme.txt, and similar documentation files from web root
- Implement web server configuration to block access to sensitive plugin/theme directories and files
- Remove version numbers from HTML comments, HTTP headers, and configuration files
- Regularly audit for exposed sensitive files in web-accessible directories
- Implement proper file permissions and access controls on deployment servers
- Consider using Web Application Firewalls (WAF) to block requests to common sensitive paths
- Perform routine security hardening of CMS installations and plugin configurations

## Variant hunting
Search for other readme files in common locations: /readme.txt, /readme.md, /CHANGELOG.txt
Check for exposed .git, .svn, or other version control directories
Enumerate common WordPress paths: /wp-content/, /wp-includes/, /wp-admin/
Look for plugin directories: /plugins/, /extensions/, /modules/
Check for version exposure in HTTP headers (Server, X-Powered-By, X-AspNet-Version)
Scan for exposed composer.json, package.json, or requirements.txt files
Enumerate theme directories and readme files
Check for exposed configuration files (.env, config.php, settings.ini)

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1592.004 - Client Configurations
- T1590 - Gather Victim Network Information
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information

## Notes
Low severity finding as version disclosure alone is not directly exploitable but significantly aids attacker reconnaissance. Often chained with other vulnerabilities for successful exploitation. Common issue in WordPress installations. Frequently found during security assessments due to default configurations.

## Full report
<details><summary>Expand</summary>

THe below URLs showing the version number of the application :

http://about.udemy.com/readme.html

http://about.udemy.com/wp-content/plugins/all-in-one-seo-pack/readme.txt

</details>

---
*Analysed by Claude on 2026-05-24*
