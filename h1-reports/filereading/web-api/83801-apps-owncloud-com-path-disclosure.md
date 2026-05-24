# apps.owncloud.com: SVN Metadata Path Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 83801 | https://hackerone.com/reports/83801
- **Submitted:** 2015-08-21
- **Reporter:** ashesh
- **Program:** ownCloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Information Disclosure, Path Traversal, Sensitive Data Exposure, Version Control System Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
Publicly accessible SVN (Subversion) metadata files were exposed on apps.owncloud.com, revealing sensitive repository information including file paths, commit history, and internal server paths. An attacker could extract repository structure, commit details, and internal system architecture from the exposed .svn/entries file.

## Attack scenario
1. Attacker discovers apps.owncloud.com is accessible via web browser
2. Attacker navigates to https://apps.owncloud.com/CONTENT/user-pics/0/.svn/entries
3. SVN metadata file is served without authentication or access controls
4. Attacker reads the XML/text contents revealing repository structure and commit metadata
5. Attacker extracts internal paths: /var/svn/repos/kde-look and full repository URL
6. Attacker gains insights into code history, authorship, and potentially exploits other SVN-related vulnerabilities

## Root cause
SVN working directory metadata (.svn folder) was not excluded from web-accessible directories. The application failed to implement web server directives (e.g., Apache .htaccess or nginx config) to deny access to version control system directories and their contents.

## Attacker mindset
Reconnaissance-focused attacker mapping application structure and repository details to identify additional attack vectors, understand code evolution, or locate sensitive information in commit history. Low effort, high information gain approach.

## Defensive takeaways
- Never deploy version control system directories (.svn, .git, .hg) in web-accessible locations
- Implement web server rules to deny access to all VC metadata: <FilesMatch '^\.svn'> or location ~/ '\.svn/' blocks
- Use .gitignore/.svnignore to exclude sensitive files from repositories
- Regularly scan deployed applications for exposed VC directories using tools like git-dumper or svn-crawler
- Implement proper .htaccess or server configuration to block dot-files and directories
- Use CI/CD pipelines that strip VC metadata during deployment
- Perform web root audits to identify unintended exposed directories

## Variant hunting
Search for exposed: .git/config, .git/HEAD, .hg/store, .bzr/branch-format, CVS/Root, _darcs/format. Check for directory listings enabled on parent directories. Look for backup files (.bak, .backup, ~), log files, and configuration files (web.config, .env, config.php) in similar paths.

## MITRE ATT&CK
- T1526 - Reconnaissance: Web Content Discovery
- T1580 - Reconnaissance: Cloud Infrastructure Discovery
- T1538 - Reconnaissance: Cloud Service Discovery
- T1592 - Gather Victim Identity Information

## Notes
This is a classic reconnaissance vulnerability common in hastily deployed applications or those using automated deployment without proper hardening. The exposed SVN repository data revealed: internal file paths (/var/svn/repos/kde-look), repository UUID, commit dates (2006), authorship (root), and historical references (KDE Look project). Severity is medium rather than high as it requires no authentication bypass and discloses only metadata, not actual code/secrets (though code is likely in commits). The vulnerability class 'Path Disclosure' is a precursor to more serious attacks.

## Full report
<details><summary>Expand</summary>

Threat:
A potentially sensitive file, directory, or directory listing was discovered on the Web server.

Impact:
The contents of this file or directory may disclose sensitive information.

Solution:
Verify that access to this file or directory is permitted. If necessary, remove it or apply access controls to it.

URL: https://apps.owncloud.com/CONTENT/user-pics/0/.svn/entries

Extracted Info:

1. committed-date="2006-06-26T14:30:45.256007Z"
2. url="file:///var/svn/repos/kde-look/trunk/usermanager/pics/0"
3. last-author="root"
4. kind="dir"
5. uuid="02c33d69-2117-0410-82eb-df9ca47e2d51" 
6. repos="file:///var/svn/repos/kde-look"

</details>

---
*Analysed by Claude on 2026-05-24*
