# Information Disclosure via Exposed Directory Listing and README Files on daily.owncloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 84085 | https://hackerone.com/reports/84085
- **Submitted:** 2015-08-22
- **Reporter:** c0ldb00t3r
- **Program:** ownCloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Directory Enumeration, Sensitive File Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
The daily.owncloud.com subdomain exposed directory listings and README.md files containing sensitive information about enterprise applications and internal structure. This allowed unauthenticated attackers to enumerate application directories and discover implementation details that could be leveraged for further attacks.

## Attack scenario
1. Attacker identifies daily.owncloud.com as a staging/development subdomain
2. Attacker navigates to /enterprise-stable8/enterprise/apps/ and discovers directory listing is enabled
3. Attacker enumerates available applications and their directory structures
4. Attacker locates and accesses README.md files in application directories
5. Attacker extracts sensitive information about application configurations, dependencies, or internal workings
6. Attacker uses discovered information to identify additional attack vectors or vulnerable components

## Root cause
Web server misconfiguration allowing directory listing and insufficient access controls on staging/development infrastructure. README files containing sensitive implementation details were not protected or removed from the web-accessible directory.

## Attacker mindset
Reconnaissance-focused attacker exploring staging environments for information leakage. The discovery of development infrastructure suggests looking for commonly-exposed documentation and configuration files that developers inadvertently leave accessible.

## Defensive takeaways
- Disable directory listing on all web servers (Options -Indexes in Apache)
- Implement strict access controls on staging/development subdomains
- Remove or restrict access to README and documentation files from production and staging environments
- Segregate development infrastructure from public internet or require authentication
- Implement Web Application Firewall rules to block enumeration attempts
- Regularly scan for exposed sensitive files and directories
- Use separate infrastructure or hostname patterns for development that are clearly not internet-facing

## Variant hunting
Check other ownCloud subdomains (test., dev., staging., qa., etc.) for similar directory listing issues
Search for other common documentation files (.md, .txt, .rst) in accessible directories
Look for git directories (.git) or version control artifacts
Enumerate other application paths and endpoints that may be similarly exposed
Check for API documentation or swagger files in development environments
Scan for backup files (*~, *.bak, .old) that may contain sensitive data

## MITRE ATT&CK
- T1526 - Reconnaissance: Gather Victim Identity Information
- T1592 - Reconnaissance: Gather Victim Host Information
- T1538 - Data from Cloud Storage Object

## Notes
This appears to be a brief/minimal submission lacking detailed technical proof or comprehensive explanation. The vulnerability likely constitutes low hanging fruit discovered during reconnaissance. The mention of 'leaking more information' suggests the reporter identified multiple exposures but provided limited specificity. This is typical of development/staging environment misconfiguration that should have been caught during infrastructure hardening.

## Full report
<details><summary>Expand</summary>

https://daily.owncloud.com/enterprise-stable8/enterprise/apps/

I have found a readme.md files also
i think this is leaking more information.



</details>

---
*Analysed by Claude on 2026-05-24*
