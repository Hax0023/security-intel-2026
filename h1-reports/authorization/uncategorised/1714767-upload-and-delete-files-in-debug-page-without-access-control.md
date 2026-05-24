# Unauthenticated File Operations via Unprotected Debug Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1714767 | https://hackerone.com/reports/1714767
- **Submitted:** 2022-09-28
- **Reporter:** 0r10nh4ck
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Missing Authentication, Unrestricted File Upload, Arbitrary File Deletion, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated debug page exposed critical file operations including upload, read, and delete functionality without any access controls. An attacker can directly access the debug endpoint to manipulate files on the application server, leading to data loss and potential system compromise.

## Attack scenario
1. Attacker discovers publicly accessible /debug endpoint through reconnaissance
2. Attacker navigates to the debug page and observes file management interface
3. Attacker uploads malicious files or system files to the application server
4. Attacker reads sensitive JSON-formatted files to extract confidential data
5. Attacker identifies and deletes critical application files causing service disruption
6. Attacker exploits uploaded files for further system compromise or lateral movement

## Root cause
Debug functionality was deployed to production without authentication/authorization controls. The endpoint was not restricted to admin users or internal networks, and no session validation was implemented before allowing file operations.

## Attacker mindset
An attacker would recognize that debug pages often contain powerful administrative functions. Finding one without access control is immediately exploitable - the attacker can read sensitive configuration files, delete critical data for denial of service, or upload files for code execution or persistence.

## Defensive takeaways
- Never expose debug endpoints in production environments; segregate debugging functionality
- Implement strict authentication and role-based access control on all file operation endpoints
- Restrict file uploads with whitelisting, size limits, and content validation
- Disable file deletion capabilities or require multi-factor approval for destructive operations
- Audit all endpoints for authentication/authorization coverage during security reviews
- Use Content Security Policy and disable directory listing to prevent discovery
- Implement detailed logging and alerting for file operations
- Apply network-level access restrictions (IP whitelisting) to debug functionality

## Variant hunting
Search for other debug endpoints: /admin/debug, /dev, /_debug, /internal, /system
Look for file operation endpoints lacking auth: /api/files, /upload, /download, /delete
Check for console/REPL endpoints without authentication
Identify exposed admin panels, maintenance pages, or developer interfaces
Test for directory traversal in file read/delete operations (../../sensitive_file)
Look for other unprotected administrative functions in debug pages
Check if uploaded files are executable or accessible via web root

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1134
- T1485
- T1040
- T1526

## Notes
This is a classic case of debug code reaching production. The vulnerability is trivial to exploit and has severe impact - no authentication required, no obfuscation, direct file system access. The /debug path is a common red flag during reconnaissance. The fact that JSON files can be read suggests potential exposure of configuration, API keys, or database credentials. Deletion capability indicates risk of data loss and service disruption.

## Full report
<details><summary>Expand</summary>

I found a debug page with no access control that allows:
- Uploading files.
- Reading files if they are in JSON format.
- Delete files.

## Impact

- Insufficient access control.
- An attacker can delete files exposed by the application.

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
## For upload file:
1. Use a browser to navigate to: https://█████/debug. 
2. Click on choose file button.
3. Set the file path in the location field
4. Click on the upload files button.
5.See the file uploaded on the list.

## For Read File
1. Select the file.
2. Click and Read File Content.
3. See the content file.

## For delete file:
1. Select the file.
2. Click on the Delete ENC Files button.

## Suggested Mitigation/Remediation Actions
- Implement access control on the page.



</details>

---
*Analysed by Claude on 2026-05-24*
