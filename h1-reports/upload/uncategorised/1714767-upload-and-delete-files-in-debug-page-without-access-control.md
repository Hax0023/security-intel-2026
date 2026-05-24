# Unauthenticated File Operations in Debug Page

## Metadata
- **Source:** HackerOne
- **Report:** 1714767 | https://hackerone.com/reports/1714767
- **Submitted:** 2022-09-28
- **Reporter:** 0r10nh4ck
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Missing Authentication, Arbitrary File Upload, Arbitrary File Deletion, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
A debug endpoint at /debug lacks any access control mechanisms, allowing unauthenticated attackers to upload, read, and delete files on the server. This enables arbitrary file manipulation and potential information disclosure through JSON file reading.

## Attack scenario
1. Attacker discovers the unauthenticated /debug endpoint through reconnaissance or directory enumeration
2. Attacker uploads malicious files (web shells, executables) to the server using the file upload functionality
3. Attacker reads sensitive application data by uploading and retrieving JSON-formatted configuration or database files
4. Attacker selectively deletes critical application files to disrupt service availability or remove audit logs
5. Attacker exfiltrates information stored in JSON files by reading their contents through the debug interface
6. Combined with file upload capabilities, attacker potentially achieves remote code execution by uploading scripts to accessible directories

## Root cause
The debug page was deployed without authentication/authorization controls, relying on obscurity rather than security. No checks verify user identity or permissions before processing file operations. The endpoint likely remained from development/testing and was not properly secured before production deployment.

## Attacker mindset
An attacker would recognize this as a critical oversight—a completely exposed administrative function. They would immediately attempt to upload a web shell or reconnaissance tool, then systematically enumerate and exfiltrate data. The presence of JSON file reading suggests the application stores sensitive configuration or user data that could be compromised.

## Defensive takeaways
- Never deploy debug/admin endpoints to production without multi-layered authentication and authorization controls
- Implement role-based access control (RBAC) on all privileged operations with explicit permission checks
- Use environment-based conditional compilation to exclude debug code from production builds entirely
- Apply authentication middleware globally and use allowlist-based access rather than blacklists
- Monitor and log all file operations with alerting for anomalous upload/deletion patterns
- Restrict file upload destinations to non-executable directories with strict MIME type validation
- Implement CSRF tokens on state-changing operations even on internal pages
- Regularly scan for exposed debug endpoints using SAST and DAST tools before deployment
- Use Web Application Firewalls (WAF) rules to block access to /debug and similar patterns

## Variant hunting
Search for other debug/admin endpoints: /admin, /internal, /test, /dev, /debug/*, /api/debug, /management
Look for console/shell pages with similar patterns: /console, /shell, /repl, /terminal
Test other file operation endpoints for access control: /api/files, /upload, /download, /delete
Check for similar functionality in different paths with slight obfuscation: /d3bug, /dbg, /debug.php
Review API endpoints for missing authentication on CRUD operations on sensitive resources
Test GraphQL/REST API endpoints for authorization bypass on file/resource operations
Look for backup/temporary files from debug pages: .bak, .tmp, .debug versions

## MITRE ATT&CK
- T1190
- T1566
- T1547
- T1070
- T1056
- T1526
- T1552
- T1021

## Notes
This is a classic broken access control vulnerability (OWASP A01:2021). The debug endpoint represents a significant security risk—it's essentially an administrative console with no authentication. The ability to upload files combined with file deletion creates both confidentiality and availability risks. If the upload directory is web-accessible, this likely enables remote code execution. The JSON file reading capability suggests the application may store sensitive data in JSON format. This vulnerability should be treated as critical due to the direct path to system compromise.

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
