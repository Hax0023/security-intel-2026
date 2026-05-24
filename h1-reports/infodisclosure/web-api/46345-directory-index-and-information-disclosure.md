# Directory Index and Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 46345 | https://hackerone.com/reports/46345
- **Submitted:** 2015-02-03
- **Reporter:** 4lemon
- **Program:** Whisper Systems
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Directory Listing, Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
The web server at http://gateway.whisper.sh/ was configured to allow directory indexing, exposing sensitive file listings and enabling discovery of potentially confidential files such as presto-query.txt. This misconfiguration could provide attackers with valuable reconnaissance information to plan further attacks.

## Attack scenario
1. Attacker identifies the target domain gateway.whisper.sh through reconnaissance
2. Attacker navigates to the root directory and discovers directory indexing is enabled
3. Attacker browses exposed directory listings to identify available files and folders
4. Attacker locates and retrieves sensitive files like presto-query.txt containing configuration or query data
5. Attacker analyzes discovered files for additional attack vectors (SQL injection, authentication bypasses, internal system details)
6. Attacker uses gathered intelligence to launch targeted attacks against backend systems or databases

## Root cause
Web server misconfiguration where directory listing (index.html fallback) was not disabled, allowing automatic generation of directory contents when no default index file is present. This typically occurs in Apache, Nginx, or IIS when the Options Indexes directive is enabled or directory browsing is not explicitly disabled.

## Attacker mindset
Reconnaissance-focused attacker seeking low-hanging fruit through basic enumeration. The attacker understands that exposed files can leak internal architecture, database query patterns, credentials, API endpoints, and other sensitive information useful for chaining into more severe vulnerabilities.

## Defensive takeaways
- Explicitly disable directory listing in web server configuration (Options -Indexes for Apache, autoindex off for Nginx)
- Ensure all directories either contain a default index file (index.html, index.php) or are not web-accessible
- Implement proper access controls and remove unnecessary files from web-accessible directories
- Conduct regular audits of web server configuration and file permissions
- Use security headers and implement rate limiting to prevent automated directory enumeration
- Scan for exposed sensitive files (.txt, .conf, .sql, .log, .bak, .config) and remove from public directories
- Implement monitoring and alerting for unusual file access patterns

## Variant hunting
Search for other instances of directory indexing on different subdomains (cdn.whisper.sh, api.whisper.sh, static.whisper.sh). Look for exposed configuration files (.env, .git, .svn), backup files (.bak, .old, .zip), query/script files (.sql, .py, .sh), and sensitive data files (.csv, .xlsx, .json) in web-accessible directories.

## MITRE ATT&CK
- T1526 - Active Scanning
- T1595 - Active Scanning
- T1592 - Gather Victim Org Information
- T1010 - Application Window Discovery
- T1083 - File and Directory Discovery
- T1087 - Account Discovery

## Notes
This is a classic misconfiguration vulnerability often discovered during initial reconnaissance. While seemingly low-severity, it frequently leads to information disclosure that enables more sophisticated attacks. The presto-query.txt filename suggests the target uses Presto SQL engine, which itself may be an information disclosure. Directory indexing is among the easiest misconfigurations to identify and remediate.

## Full report
<details><summary>Expand</summary>

Directory index allowed in http://gateway.whisper.sh/
Info that might be useful in some other attack's vectors
http://gateway.whisper.sh/presto-query.txt

</details>

---
*Analysed by Claude on 2026-05-24*
