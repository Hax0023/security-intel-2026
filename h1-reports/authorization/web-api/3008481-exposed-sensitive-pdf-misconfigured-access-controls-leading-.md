# Exposed Sensitive PDF: Misconfigured Access Controls Leading to Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 3008481 | https://hackerone.com/reports/3008481
- **Submitted:** 2025-02-23
- **Reporter:** ziad616
- **Program:** ACC (likely U.S. Army Contracting Command or similar government entity)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Information Disclosure, Misconfigured Server Permissions
- **CVEs:** None
- **Category:** web-api

## Summary
An internal PDF document marked as restricted and not approved for public release was publicly accessible on the ACC website due to misconfigured access controls. The vulnerability allowed any unauthenticated user to download and view sensitive internal communications and operational information.

## Attack scenario
1. Attacker discovers the ACC website and explores common directory structures or uses web crawling tools
2. Attacker identifies a publicly accessible directory or file path containing sensitive documents
3. Attacker navigates to the URL hosting the internal PDF without encountering authentication prompts
4. Attacker successfully downloads the PDF and reviews its contents, discovering internal markings indicating restricted classification
5. Attacker can exfiltrate the document and potentially share it with adversaries for intelligence gathering or targeted attacks
6. Attacker uses disclosed information to conduct social engineering, identify key personnel, or plan targeted cyber operations

## Root cause
The web server was misconfigured to serve the PDF with overly permissive access controls, likely due to: improper file/folder permissions, lack of authentication middleware, absence of access control lists (ACLs), or failure to properly restrict sensitive directories from public access

## Attacker mindset
Opportunistic reconnaissance attacker scanning government/institutional websites for information disclosure vulnerabilities. The attacker likely used automated tools or manual directory enumeration to discover publicly accessible sensitive content and recognized the value of the disclosed internal communications.

## Defensive takeaways
- Implement defense-in-depth: use authentication AND authorization checks for all sensitive resources
- Enforce principle of least privilege on file system permissions and web server configurations
- Conduct regular security audits of web server directory structures and access controls
- Implement web application firewalls (WAF) to restrict access to sensitive paths
- Use robots.txt and security.txt to guide bot behavior, but never rely on it for access control
- Classify and mark sensitive documents clearly, and ensure classification is paired with technical controls
- Establish automated scanning to detect publicly accessible sensitive files (PDFs, backups, config files)
- Implement proper logging and monitoring to detect unauthorized access attempts
- Use server-side access control mechanisms rather than relying on obscurity of URLs

## Variant hunting
Check for similar internally-marked PDFs in other directories (../docs/, ../internal/, ../archive/)
Look for other file types with restricted markings (.docx, .xlsx, .txt, .zip, .sql)
Enumerate common backup file patterns (.bak, .backup, .old, .tmp)
Test for directory traversal attacks to access parent directories
Scan for exposed git repositories or .git directories containing sensitive commits
Check for exposed configuration files (.env, .config, web.config, settings.json)
Look for exposed API endpoints that may return sensitive data without proper authentication
Test sibling paths to identify other publicly accessible restricted content

## MITRE ATT&CK
- T1526 - Reconnaissance: Exposure of sensitive data
- T1592 - Gather Victim Identity Information
- T1598 - Phishing for Information (using disclosed organizational data)
- T1589 - Gather Victim Organization Information
- T1590 - Gather Victim Network Information

## Notes
This is a classic misconfiguration vulnerability affecting government/institutional entities. The document markings (UNCLASSIFIED // NOT APPROVED FOR PUBLIC RELEASE // FOR OFFICIAL USE ONLY) suggest U.S. federal classification protocols. The impact could extend beyond information disclosure to enabling social engineering, targeting key personnel, and informing adversary operations. The redacted URL and system host indicate this was a real HackerOne report; the remediation is straightforward but the security failure suggests broader systemic issues with access control implementation.

## Full report
<details><summary>Expand</summary>

**Description:**
An internal PDF document, marked “UNCLASSIFIED // NOT APPROVED FOR PUBLIC RELEASE // FOR OFFICIAL USE ONLY,” is publicly accessible on the ACC website. This misconfiguration allows unauthorized users to download and view sensitive internal content, resulting in an unintended disclosure of information.
** References:**
CWE-200: Information Disclosure

## Impact

An attacker can view, download, and potentially disseminate sensitive internal information. This exposure can compromise operational security, lead to reputational damage, and enable targeted cyber attacks by revealing confidential internal communications.

## System Host(s)
██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1.Open a web browser.
2.Navigate to:
██████████
3.Observe that the PDF loads without any authentication or access controls.
4.Verify that the document contains internal markings indicating it is not approved for public release.

## Suggested Mitigation/Remediation Actions
Restrict public access to the folder or server hosting the document by updating access controls and permissions.
Implement authentication or other measures to ensure only authorized users can view sensitive documents.
Audit related directories on the ACC website for other inadvertent exposures and remediate accordingly.



</details>

---
*Analysed by Claude on 2026-05-24*
