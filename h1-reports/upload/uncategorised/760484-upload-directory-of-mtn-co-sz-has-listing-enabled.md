# Directory Listing Enabled in Upload Directory

## Metadata
- **Source:** HackerOne
- **Report:** 760484 | https://hackerone.com/reports/760484
- **Submitted:** 2019-12-17
- **Reporter:** juni19
- **Program:** MTN Eswatini (mtn.co.sz)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Directory Enumeration, Improper Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
The WordPress upload directory at /wp-content/uploads/ has directory listing enabled, allowing unauthenticated users to browse and access all uploaded files. This enables reconnaissance and potential exposure of sensitive data stored in the uploads folder.

## Attack scenario
1. Attacker discovers the /wp-content/uploads/ directory is publicly accessible
2. Attacker navigates to the directory and observes directory listing is enabled
3. Attacker browses through folder structure to identify file organization patterns
4. Attacker locates and accesses sensitive files such as backups, user data, or confidential documents
5. Attacker uses enumeration to discover other exposed directories or file naming conventions
6. Attacker exfiltrates or documents sensitive information for further exploitation or sale

## Root cause
Web server (Apache/Nginx) has directory listing enabled for the /wp-content/uploads/ directory, and .htaccess or equivalent server configuration lacks proper access restrictions. Missing IndexIgnore or Options -Indexes directive in the upload directory configuration.

## Attacker mindset
Low-effort reconnaissance - directory listing is a passive vulnerability requiring no authentication. Attackers treat this as an easy information gathering opportunity to identify what data is exposed, plan social engineering attacks, or find additional vulnerable components.

## Defensive takeaways
- Disable directory listing via .htaccess (Options -Indexes) or web server configuration
- Implement proper access controls to restrict /wp-content/uploads/ to legitimate requests only
- Use index.php or index.html files in upload directories to prevent listing fallback
- Regularly audit WordPress configuration and file permissions
- Store truly sensitive files outside the web root or implement authentication
- Monitor web server logs for suspicious directory browsing patterns
- Implement Web Application Firewall (WAF) rules to block directory traversal attempts

## Variant hunting
Check other WordPress directories: /wp-includes/, /wp-content/themes/, /wp-content/plugins/
Test for directory listing in backup directories: /backups/, /old/, /archive/
Scan for exposed configuration files: wp-config.php, .git, .env in various directories
Look for other common web application directories with listing enabled
Check for path traversal opportunities combined with directory listing

## MITRE ATT&CK
- T1526 - Reconnaissance: Search Open Websites/Domains
- T1592 - Gather Victim Host Information
- T1083 - File and Directory Discovery
- T1040 - Network Sniffing (passive information gathering)

## Notes
This is a low-complexity, high-impact vulnerability common in misconfigured WordPress installations. The WordPress community typically considers this critical because uploads often contain user-generated content, backups, or temporary files. Severity is elevated if uploads contain database backups, user authentication data, or customer information. The vulnerability requires no authentication and is trivially exploitable via a web browser.

## Full report
<details><summary>Expand</summary>

## Summary:
There are some exposed files accessible for anyone

## Steps To Reproduce:
Go to http://www.mtn.co.sz/wp-content/uploads/ and navigate between available folders

## Impact

Every uploaded data can be  accessible through this directory listing vulnerability
This might include several private/confidential data

</details>

---
*Analysed by Claude on 2026-05-24*
