# Full Path Disclosure via Exposed PHP File Path

## Metadata
- **Source:** HackerOne
- **Report:** 591002 | https://hackerone.com/reports/591002
- **Submitted:** 2019-05-27
- **Reporter:** bbc6dfb7d3878289f2f98d4
- **Program:** Unikrn
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Full Path Disclosure, Improper Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
A PHP script file path was directly accessible and disclosed via HTTP response, revealing the server's internal directory structure (/app/bundles/CampaignBundle/EventListener/LeadSubscriber.php). This information disclosure allows attackers to map application architecture and identify potential attack vectors. The vulnerability can be remediated by implementing proper .htaccess restrictions to prevent direct access to PHP source files.

## Attack scenario
1. Attacker discovers or guesses PHP file paths within the application bundle structure
2. Attacker makes HTTP request to the vulnerable endpoint containing the PHP file path
3. Server responds with or exposes the full file path in error messages, source code, or headers
4. Attacker gains insight into application structure, naming conventions, and module organization
5. Attacker uses disclosed paths to identify other sensitive files or components for further exploitation
6. Attacker could combine with other vulnerabilities (LFI, RFI) to access or execute these files

## Root cause
Missing access controls to prevent direct HTTP requests to PHP source files. Server configuration lacks .htaccess rules or equivalent restrictions (deny direct access to /app/bundles/* or *.php files). No prevention of path disclosure in error messages or HTTP responses.

## Attacker mindset
Reconnaissance phase - mapping application structure to understand architecture, identify technologies, locate potential high-value files (config files, vendor directories), and find patterns for other sensitive endpoints. Information disclosure is a stepping stone to more severe exploits.

## Defensive takeaways
- Implement .htaccess rules to deny direct access to PHP files: 'deny from all' or 'Require all denied'
- Configure web server to prevent execution of scripts in bundle/vendor directories
- Implement proper error handling to avoid displaying file paths in error messages
- Use security headers and response filtering to strip path information from responses
- Restrict directory listing - ensure DirectoryIndex is disabled for sensitive paths
- Conduct application-wide code review for hardcoded paths in responses
- Implement Web Application Firewall rules to detect and block requests for PHP source files
- Use separate web root with only necessary files, keep source code outside webroot

## Variant hunting
Search for other exposed bundle paths: /app/bundles/*/Controller/*, /src/*, /vendor/*
Check for path disclosure in error pages, stack traces, or debug output
Test access to configuration files: config.php, database.yml, .env files
Enumerate common Laravel/Symfony bundle paths if framework identified
Check for path leakage in HTTP headers (Server, X-Powered-By, X-AspNet-Version)
Test for arbitrary file disclosure via LFI using discovered paths as reference
Scan for exposed .git, .env, composer.json in web root
Check for path disclosure in backup files (.php.bak, .php.old)

## MITRE ATT&CK
- T1190
- T1217
- T1526
- T1592

## Notes
This is a low-severity information disclosure vulnerability. While not immediately exploitable on its own, it significantly aids attackers in reconnaissance and mapping application architecture. The report demonstrates good vulnerability communication by citing OWASP reference and suggesting mitigation (.htaccess). Common in misconfigured web servers where source code is placed in webroot. Often chained with other vulnerabilities for greater impact.

## Full report
<details><summary>Expand</summary>

HI security team!

we can see path on your resource.

https://crm.unikrn.com/app/bundles/CampaignBundle/EventListener/LeadSubscriber.php


You must create a ban on viewing the script from the outside using .htaccess

## Impact

Full Path Disclosure

https://www.owasp.org/index.php/Full_Path_Disclosure

</details>

---
*Analysed by Claude on 2026-05-24*
