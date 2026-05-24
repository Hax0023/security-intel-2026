# Unauthenticated phpinfo() File Leads to Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 2764952 | https://hackerone.com/reports/2764952
- **Submitted:** 2024-10-07
- **Reporter:** odaysec
- **Program:** Undisclosed
- **Bounty:** Unknown
- **Severity:** Medium
- **Vuln:** Information Disclosure, Lack of Access Control, Debug Information Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated phpinfo() file was accessible on the target server, exposing sensitive server configuration and environment details without authentication. An attacker could leverage this information to conduct reconnaissance and identify further attack vectors.

## Attack scenario
1. Attacker performs directory enumeration using tools like Burp Suite Intruder to discover common PHP debug files
2. Attacker identifies info.php or similar phpinfo() file accessible without authentication
3. Attacker accesses the phpinfo() page and collects detailed server configuration information
4. Attacker analyzes output to identify OS version, PHP version, loaded extensions, and environment variables
5. Attacker uses gathered intelligence to identify vulnerable components or misconfigurations
6. Attacker leverages findings to conduct targeted follow-up attacks (e.g., exploiting specific PHP extension versions)

## Root cause
Development or default configuration artifact left in production environment; lack of web server hardening to restrict access to debugging files; missing authentication controls on administrative information endpoints

## Attacker mindset
Reconnaissance and information gathering phase of attack. The attacker recognizes that phpinfo() files are common in PHP installations and systematically searches for them as part of initial reconnaissance to map the target environment and identify potential weaknesses.

## Defensive takeaways
- Remove or disable all phpinfo() and other debugging files from production environments
- Implement strict access controls requiring authentication for any information-disclosure endpoints
- Use Web Application Firewall (WAF) rules to block access to common debug file patterns (info.php, phpinfo.php, test.php, etc.)
- Disable display_errors and expose_php PHP directives in production
- Implement regular file integrity monitoring to detect unauthorized or unexpected files
- Conduct pre-deployment reviews to identify and remove debugging artifacts
- Restrict directory listing and implement proper file permissions

## Variant hunting
Search for other debugging files: test.php, debug.php, config.php, status.php
Look for exposed error pages that display phpinfo() equivalent details
Check for exposed .env files, configuration files, or application source code
Scan for exposed backup files (.php.bak, .php.old, .backup)
Identify other information disclosure endpoints (server-status, /admin panels without auth)
Look for git repositories (.git/config) exposed in web root

## MITRE ATT&CK
- T1590
- T1592
- T1592.004
- T1526
- T1087

## Notes
This is a classic reconnaissance vulnerability often encountered during security assessments. While the direct impact is information disclosure, the real danger lies in the intelligence it provides for secondary attacks. Many organizations unknowingly leave phpinfo() files in production from development/testing phases. The vulnerability demonstrates the importance of differentiating development and production environments and implementing proper change control processes.

## Full report
<details><summary>Expand</summary>

## Summary 
Many PHP installation tutorials instruct the user to create a PHP file that calls the PHP function 'phpinfo()' for debugging purposes, and various PHP applications may also include such a file by default. By accessing it, a remote attacker can discover a large amount of information about the remote web server configuration to help conduct further attacks, including :
 * root/vps of the web server, operating system and PHP components
 * Details of the PHP configuration
 * Loaded PHP extensions with their configurations
 * Server environment variables.


**Proof On Concepts:**
█████
```
Linux uggogamesdb 5.4.17-2136.323.8.2.el8uek.x86_64 #2 SMP ████ █████ PDT 2023 x86_64
```

## Steps to Reproduce
* Visit the target scope is ██████
 * You can used `burp-suite-intruder` for finding sensitive directory
 * And now we found a directory is `info.php`
 * Let's see opened in our browser is directory ██████████
 * You can see this page can be view without authenticate

## Suggested Mitigation/Remediation Actions
Remove the affected file(s).
███████

The remote web server contains a PHP script that is prone to an information disclosure attack.

</details>

---
*Analysed by Claude on 2026-05-24*
