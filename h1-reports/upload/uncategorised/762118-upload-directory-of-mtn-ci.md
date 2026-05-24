# Directory Listing Enabled in Upload Directory - MTN.ci

## Metadata
- **Source:** HackerOne
- **Report:** 762118 | https://hackerone.com/reports/762118
- **Submitted:** 2019-12-20
- **Reporter:** juni19
- **Program:** MTN (Mtn.ci)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Improper Access Control, Information Disclosure, Directory Enumeration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The /wp-content/uploads/ directory on mtn.ci has directory listing enabled, allowing unauthenticated users to browse and access all uploaded files. This exposes potentially sensitive data uploaded by website administrators including documents, media, and confidential information.

## Attack scenario
1. Attacker discovers the /wp-content/uploads/ directory is publicly accessible
2. Attacker navigates to the base upload directory and observes directory listing is enabled
3. Attacker browses through subdirectories to identify files uploaded by administrators
4. Attacker identifies sensitive files such as configuration backups, documents, or media
5. Attacker downloads confidential data for further analysis or exploitation
6. Attacker may use discovered information for social engineering or identify additional vulnerabilities

## Root cause
Web server (likely Apache or Nginx) has directory listing enabled for the /wp-content/uploads/ directory, typically through missing or misconfigured .htaccess rules or server directives that should disable IndexOptions.

## Attacker mindset
Reconnaissance-focused attacker performing passive enumeration to identify exposed data and sensitive information without authentication, seeking low-hanging fruit in misconfigured web directories.

## Defensive takeaways
- Disable directory listing on all web server directories using .htaccess (Options -Indexes) or web server configuration
- Implement proper access controls on upload directories - restrict to authenticated users only
- Use robots.txt to discourage indexing of upload directories
- Regularly audit web server configurations for directory listing settings
- Implement monitoring to alert on unusual patterns of upload directory access
- Store sensitive uploads outside the web root or in protected directories
- Consider implementing content delivery mechanisms that serve files through application logic rather than direct web access

## Variant hunting
Check other upload directories: /uploads/, /files/, /documents/, /media/
Test for directory listing in backup/archive directories: /backups/, /archives/, /downloads/
Enumerate WordPress plugin and theme directories for listings: /wp-content/plugins/, /wp-content/themes/
Check for exposed admin-related directories: /wp-admin/, /admin/
Test subdomain upload directories and staging environments
Look for similar misconfiguration on sister domains within the organization

## MITRE ATT&CK
- T1526
- T1592
- T1005
- T1040

## Notes
URL in summary mentions mtn.co.sz but title and steps reference mtn.ci - likely a typo. This is a common misconfiguration in WordPress installations. The severity depends on what data is actually stored in the uploads directory; exposure of customer data would escalate to critical.

## Full report
<details><summary>Expand</summary>

## Summary:
Upload directory of Mtn.co.sz has listing enabled

## Steps To Reproduce:

  1. Just go to https://www.mtn.ci/wp-content/uploads/ and navigate between available folders

## Impact

Every data uploaded by the webmaster can be accessible through this directory listing vulnerability
This might include several private/confidential data

</details>

---
*Analysed by Claude on 2026-05-24*
