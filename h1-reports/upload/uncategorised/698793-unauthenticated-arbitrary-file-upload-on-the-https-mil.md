# Unauthenticated Arbitrary File Upload on Military Domain

## Metadata
- **Source:** HackerOne
- **Report:** 698793 | https://hackerone.com/reports/698793
- **Submitted:** 2019-09-20
- **Reporter:** sp1d3rs
- **Program:** Department of Defense (DoD) Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Arbitrary File Upload, Missing Authentication, Missing File Type Validation, Information Disclosure, Improper Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated file upload endpoint (upload.php) on a military domain lacks proper validation and access controls, allowing attackers to upload arbitrary files. The vulnerability enables code execution, stored XSS, and hosting of malicious content, with uploaded files accessible via predictable paths and internal path information disclosed to attackers.

## Attack scenario
1. Attacker identifies publicly accessible upload.php endpoint on the military domain without authentication requirements
2. Attacker crafts malicious file (PHP webshell, executable, or XSS payload) and uploads via the unprotected endpoint
3. Server accepts file without validating file type, extension, or content, providing success response with internal path disclosure
4. Attacker accesses uploaded file via predictable path structure (e.g., /delete.me directory) and executes or deploys the payload
5. Attacker establishes web shell for remote code execution, spreads malware, or injects XSS to compromise users visiting the domain
6. Attack infrastructure is hosted on government domain, providing legitimacy and bypassing reputation-based filtering

## Root cause
The upload endpoint implements no authentication mechanism, lacks file type/extension validation, stores files in web-accessible directories with predictable paths, and fails to sanitize or restrict file execution. Error responses leak internal directory structures aiding attackers.

## Attacker mindset
Target high-value government infrastructure for maximum impact; exploit trivial upload vulnerabilities to gain initial foothold; leverage government domain trust to host payloads and establish persistence; abuse information disclosure to navigate file system and locate sensitive files.

## Defensive takeaways
- Require strong authentication (OAuth, mutual TLS) for all file upload endpoints, especially on government/critical systems
- Implement strict whitelist-based file type validation using magic bytes, not just extensions; reject executable types entirely
- Store uploaded files outside web root or in non-executable directories with restricted permissions (chmod 000 execute bit)
- Generate randomized, unpredictable filenames and implement access control to prevent directory traversal enumeration
- Disable script execution in upload directories via web server config (.htaccess, nginx config) and Content-Disposition headers
- Implement rate limiting and abuse detection on upload endpoints; log all upload activities for forensic analysis
- Sanitize error messages to avoid leaking internal paths, server info, or directory structures
- Conduct security code review of file handling functions; establish secure file upload patterns in development guidelines
- Implement automated security scanning (SAST/DAST) in CI/CD to catch upload vulnerabilities before deployment

## Variant hunting
Search for other publicly accessible upload endpoints on the same domain (upload_image.php, file_upload.php, attachment.php); test for authenticated bypasses via parameter tampering or token reuse; check for ZIP/archive extraction features enabling path traversal; test for polyglot file uploads (e.g., PHP image hybrids); verify if .htaccess upload is possible to enable execution; examine backup/old versions (/upload_old.php, /v2/upload.php); test bulk upload APIs; check for XXE in XML uploads or zip bomb attacks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1190.001 - Arbitrary Code Execution via File Upload
- T1566.002 - Phishing: Spearphishing Link (hosting malware)
- T1583.004 - Acquire Infrastructure: Compromise Third-party Infrastructure (government domain abuse)
- T1190 - Code Injection via Stored XSS

## Notes
Critical severity justified by unauthenticated access on military domain, direct code execution risk, and information disclosure. Report demonstrates responsible disclosure to DoD program. The /delete.me path suggests incomplete file deletion logic, potentially exposing previously deleted files. Lack of CSRF tokens suggests additional POST-based vulnerabilities may exist. File upload endpoints are consistently high-priority targets; this vulnerability exemplifies why secure upload handling is security-critical infrastructure requirement.

## Full report
<details><summary>Expand</summary>

##Description
I was able to identify unsafe upload endpoint on the https://██████/upload.php

##POC
1) Go to the https://██████/upload.php
2) Upload some test file.
You will see success message, leaking some internal paths
3) Visit `https://██████████/delete.me` and you will see your uploaded file there
I uploaded example image file there:
█████

## Impact

Arbitrary file upload, may lead to the Stored XSS, hosting attacker's content and code execution.

</details>

---
*Analysed by Claude on 2026-05-24*
