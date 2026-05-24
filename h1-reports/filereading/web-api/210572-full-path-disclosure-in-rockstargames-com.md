# Full Path Disclosure in Rockstargames.com

## Metadata
- **Source:** HackerOne
- **Report:** 210572 | https://hackerone.com/reports/210572
- **Submitted:** 2017-03-04
- **Reporter:** pappan
- **Program:** Rockstar Games
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak
- **CVEs:** None
- **Category:** web-api

## Summary
The Rockstar Games web server discloses the full filesystem path when returning HTTP 403 Forbidden errors for certain requests. This information disclosure allows attackers to understand the server's directory structure and potentially identify targets for further exploitation.

## Attack scenario
1. Attacker browses to a restricted endpoint on rockstargames.com
2. Server returns HTTP 403 Forbidden status code
3. Error page displays the full filesystem path of the directory being accessed
4. Attacker documents the directory structure revealed in the error message
5. Attacker uses path information to identify potential file locations or application structure
6. Information aids in planning targeted attacks against known file paths

## Root cause
Web server (likely Apache or IIS) is configured to display verbose error messages that include filesystem paths in HTTP 403 responses instead of generic error pages.

## Attacker mindset
Reconnaissance-focused attacker gathering intelligence about server architecture. While low-severity alone, this information can be combined with other findings to map application structure and identify exploitation opportunities.

## Defensive takeaways
- Configure web server to return generic error pages without revealing filesystem paths
- Implement custom error handlers that sanitize all error output
- Use .htaccess or web server configuration to suppress detailed error messages
- Regularly audit error responses across the application for information leakage
- Monitor and log 403 errors to detect reconnaissance attempts
- Implement Web Application Firewall (WAF) rules to block verbose error exposure

## Variant hunting
Search for similar path disclosure in error pages (404, 500, 503 errors), stack traces in production, directory listing pages, Apache/IIS default error templates, and any endpoints returning system information in error responses.

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1592.004 - Client Configurations
- T1526 - Exposure of Resource Information to Untrusted Party

## Notes
Low severity issue as it only reveals filesystem paths without direct exploitation capability. However, it's valuable reconnaissance data for attackers. The report lacks specific details about which exact paths were disclosed. This is a common misconfiguration in legacy applications or default server setups.

## Full report
<details><summary>Expand</summary>

Browsing this link http://www.rockstargames.com██████ gives forbidden error. Its good but also it displays the full path of the current directory . Refer screenshot attached.

</details>

---
*Analysed by Claude on 2026-05-24*
