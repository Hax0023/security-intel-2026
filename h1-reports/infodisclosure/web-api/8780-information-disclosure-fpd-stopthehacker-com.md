# Information Disclosure - Full Path Disclosure (FPD) via Error Message

## Metadata
- **Source:** HackerOne
- **Report:** 8780 | https://hackerone.com/reports/8780
- **Submitted:** 2014-04-21
- **Reporter:** quistertow
- **Program:** stopthehacker.com
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Full Path Disclosure, Error-Based Information Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
A WordPress installation exposes sensitive server path information through a fatal PHP error message when accessing wp-includes/rss-functions.php. The error reveals the full filesystem path (/home/jaalweb/stopthehacker.com/), enabling attackers to understand the server directory structure. This information can be leveraged for further reconnaissance and attack planning.

## Attack scenario
1. Attacker discovers stopthehacker.com and begins reconnaissance
2. Attacker enumerates common WordPress paths like /wp-includes/ and /wp-admin/
3. Attacker accesses http://www.stopthehacker.com/wp-includes/rss-functions.php
4. Server returns a fatal PHP error due to missing function dependency
5. Error message displays full filesystem path: /home/jaalweb/stopthehacker.com/
6. Attacker uses disclosed path information to refine exploitation strategy and identify hosting environment details

## Root cause
PHP error reporting is enabled in production environment with debug output exposed to unaccessible users. The wp-includes/rss-functions.php file has a missing or incorrectly loaded dependency, causing a fatal error that displays the full filesystem path in the error message.

## Attacker mindset
Information gathering phase - mapping server architecture and environment details. Full path disclosure helps attackers understand the hosting setup, user ownership patterns, and potential directory structures for other exploitation vectors.

## Defensive takeaways
- Disable PHP error reporting display in production (set display_errors = Off in php.ini)
- Log errors to files instead of displaying them to users
- Implement proper error handling and custom error pages that don't leak system information
- Ensure all WordPress files and dependencies are properly installed and loaded
- Use Web Application Firewall (WAF) rules to detect and block access to wp-includes files directly
- Implement .htaccess rules to restrict direct access to sensitive WordPress directories
- Regularly audit error logs for information disclosure vulnerabilities

## Variant hunting
Search for other accessible wp-includes files that generate errors (/wp-includes/load.php, /wp-includes/version.php)
Test other WordPress paths for FPD (wp-admin, wp-content, plugins)
Check for error messages in other PHP files with undefined function calls
Enumerate common deprecated or conditionally-loaded WordPress functions
Test for information disclosure via 404 pages and error handling mechanisms
Look for path disclosure in exception handlers and stack traces

## MITRE ATT&CK
- T1590.002 - Gather Victim Host Information: Software

## Notes
This is a low-severity information disclosure issue typical of misconfigured WordPress installations. While the path alone doesn't directly enable attacks, it provides valuable reconnaissance data. The vulnerability exists because error messages were not sanitized for user-facing display. Most web hosting providers use similar /home/username/domain.com patterns, making this partially predictable, but confirmation through error messages accelerates reconnaissance.

## Full report
<details><summary>Expand</summary>

Hi,
I found a information disclosure vulnerability(Full path disclosure)
Vulnerable link : http://www.stopthehacker.com/wp-includes/rss-functions.php
You can see in the page the path of the site 
 Fatal error: Call to undefined function _deprecated_file() in /home/jaalweb/stopthehacker.com/wp-includes/rss-functions.php on line 8

Regards,
   Florin

</details>

---
*Analysed by Claude on 2026-05-24*
