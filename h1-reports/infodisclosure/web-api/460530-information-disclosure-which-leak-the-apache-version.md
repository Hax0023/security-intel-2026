# Information Disclosure: Apache Version Leakage via Manual Page

## Metadata
- **Source:** HackerOne
- **Report:** 460530 | https://hackerone.com/reports/460530
- **Submitted:** 2018-12-11
- **Reporter:** hamzamn2098
- **Program:** ratelimited
- **Bounty:** unknown
- **Severity:** low
- **Vuln:** Information Disclosure, Server Information Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
The Apache server version is disclosed through the manual documentation page accessible at https://social.ratelimited.me/manual/en/index.html. This allows attackers to identify the specific Apache version running on the target server, facilitating reconnaissance for version-specific vulnerabilities. While low severity, version disclosure should be minimized as part of defense-in-depth strategy.

## Attack scenario
1. Attacker discovers the /manual/ directory is accessible on the target domain
2. Attacker navigates to https://social.ratelimited.me/manual/en/index.html
3. Manual page header or content reveals the specific Apache version number
4. Attacker catalogs this information as part of reconnaissance
5. Attacker searches for known vulnerabilities affecting that specific Apache version
6. Attacker uses this intelligence to plan targeted exploitation attempts

## Root cause
The Apache manual documentation directory (/manual/) was left accessible to the internet without restriction. This directory is typically installed by default with Apache and contains version information in page headers or metadata. No access controls or directory hiding were implemented.

## Attacker mindset
Reconnaissance-focused attacker gathering intelligence about server infrastructure. Version information reduces attack surface research time and enables targeting of known CVEs. Typical behavior in early-stage reconnaissance before attempting exploitation.

## Defensive takeaways
- Disable or restrict access to /manual/ directory via Apache configuration (.htaccess or httpd.conf)
- Configure ServerTokens to 'Prod' or 'Min' to minimize version disclosure in HTTP headers
- Remove unnecessary Apache modules and documentation from production servers
- Implement IP-based access controls on administrative/documentation endpoints
- Use Web Application Firewall (WAF) rules to block access to /manual/ paths
- Regularly audit directory listings and accessible documentation
- Consider using reverse proxy to strip version information from headers

## Variant hunting
Check for other documentation directories: /doc/, /help/, /docs/
Test HTTP headers for Server: headers revealing version information
Look for default Apache status pages at /server-status/ or /server-info/
Search for package manager version info accessible via web interface
Check for README files, CHANGELOG, or VERSION files in web root
Test other subdomains for similar information disclosure

## MITRE ATT&CK
- T1592.4 - Gather Victim Identity Information - Infrastructure Details
- T1592.2 - Gather Victim Identity Information - Software Details

## Notes
This is a classic low-severity information disclosure. While it doesn't directly compromise the system, it aids attackers in reconnaissance. Many organizations leave /manual/ accessible by default. The vulnerability requires minimal technical complexity to exploit but has limited direct impact. Often bundled with other reconnaissance findings for higher severity reports.

## Full report
<details><summary>Expand</summary>

Hello ratelimited team !

I have found a  information disclosure which leak the apache version

Link : https://social.ratelimited.me/manual/en/index.html

## Impact

Leaking the http apache server version

</details>

---
*Analysed by Claude on 2026-05-24*
