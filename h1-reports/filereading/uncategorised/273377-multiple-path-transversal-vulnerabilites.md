# Multiple Path Traversal Vulnerabilities Across Tor Project Subdomains

## Metadata
- **Source:** HackerOne
- **Report:** 273377 | https://hackerone.com/reports/273377
- **Submitted:** 2017-09-30
- **Reporter:** myselfphoton
- **Program:** Tor Project
- **Bounty:** Not specified (reporter noted as out of scope)
- **Severity:** Medium
- **Vuln:** Path Traversal, Directory Listing, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple subdomains of torproject.org expose directory listing functionality, allowing unauthenticated attackers to browse and enumerate file system contents. The vulnerability affects at least three distinct subdomains and likely extends to additional endpoints across the organization.

## Attack scenario
1. Attacker discovers torproject.org subdomains via search engine dorking using 'inurl:index of site:torproject.org'
2. Attacker identifies vulnerable endpoints including findoc/, user directories, and package repositories
3. Attacker directly accesses directory listing URLs without authentication
4. Attacker enumerates sensitive files, configurations, or backups exposed in directory listings
5. Attacker downloads or analyzes exposed files for further exploitation opportunities
6. Attacker maps organizational structure and identifies additional target systems

## Root cause
Web server misconfiguration allowing directory listing (likely Apache with Options +Indexes enabled) across multiple virtual hosts without proper access controls or directory indexing restrictions

## Attacker mindset
Opportunistic reconnaissance through passive enumeration; low-effort attack leveraging search engines to identify misconfigured servers; motivated by information gathering rather than immediate exploitation

## Defensive takeaways
- Disable directory listing globally via web server configuration (Options -Indexes for Apache, disable autoindex for nginx)
- Implement centralized web server hardening baselines across all subdomains and virtual hosts
- Audit all *.torproject.org subdomains for information disclosure via automated scanning
- Deploy WAF rules to detect and block directory enumeration patterns
- Implement Content Security Policy headers to limit information leakage
- Conduct regular security assessments of all public-facing web properties
- Document approved directory structures and validate compliance in CI/CD pipeline

## Variant hunting
Scan all torproject.org subdomains for enabled directory indexing
Test for path traversal sequences (../, ..\, encoded variants) on all web endpoints
Check for backup files (.bak, .old, .swp) accessible via directory listing
Enumerate hidden directories and files using wordlists on vulnerable endpoints
Identify other Tor-related domains (tpo.org, etc.) with similar misconfigurations
Search for .git, .env, config files exposed in directory listings
Test for authentication bypass on restricted directories

## MITRE ATT&CK
- T1526 - Acquire Infrastructure (reconnaissance via directory enumeration)
- T1040 - Traffic Sniffing (identifying sensitive information in exposed files)
- T1087 - Account Discovery (via exposed user directories)
- T1087.004 - Email Account Discovery

## Notes
Reporter voluntarily disclosed despite marking as out of scope, suggesting good faith participation. Vulnerability is widespread across multiple subdomains, indicating systemic configuration issue rather than isolated oversight. Search engine indexing of directory listings provides trivial discovery method. Low technical sophistication required for exploitation; primarily an information disclosure risk that could enable more targeted attacks.

## Full report
<details><summary>Expand</summary>

I have found multiple path transversal in *.torproject.org
POC:
[+] https://www.torproject.org/about/findoc/
[+] https://people.torproject.org/~infinity0/
[+] https://deb.torproject.org/torproject.org/
There are many many others which can be accessed by searching following in google:
inurl:"index of" site:torproject.org
I know that its out of scope of your bounty program but I thought I should tell you about it.
Regards!

</details>

---
*Analysed by Claude on 2026-05-24*
