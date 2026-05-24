# DNN - Unrestricted Arbitrary File Upload (CVE-2025-64095)

## Metadata
- **Source:** HackerOne
- **Report:** 3414079 | https://hackerone.com/reports/3414079
- **Submitted:** 2025-11-06
- **Reporter:** 0xr2r
- **Program:** DNN (DotNetNuke)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Unrestricted File Upload, Authentication Bypass, Arbitrary File Overwrite, Cross-Site Scripting (XSS), Website Defacement
- **CVEs:** CVE-2025-64095
- **Category:** uncategorised

## Summary
DNN versions prior to 10.1.1 contain a critical unrestricted file upload vulnerability in the default HTML editor provider (DNNConnect.CKE). The FileUploader.ashx endpoint allows unauthenticated attackers to upload and overwrite arbitrary files, enabling website defacement and XSS injection attacks.

## Attack scenario
1. Attacker identifies the vulnerable FileUploader.ashx endpoint at /Providers/HtmlEditorProviders/DNNConnect.CKE/Browser/FileUploader.ashx
2. Attacker crafts a malicious POST request containing a file payload without authentication credentials
3. The vulnerable endpoint accepts the upload due to missing authentication and authorization checks
4. Attacker uploads a malicious file (e.g., XSS payload in HTML/JS or ASP.NET shell) or overwrites existing legitimate files
5. The uploaded file is stored in the web-accessible directory, either executing or being served to victims
6. Victims browsing the site trigger XSS payloads or attackers gain code execution via web shell

## Root cause
The HTML editor provider's FileUploader.ashx handler lacks proper authentication and authorization validation before processing file uploads. Input validation and file type restrictions are either missing or insufficient, allowing arbitrary file types to be uploaded and existing files to be overwritten.

## Attacker mindset
Low-effort, high-impact attack. The vulnerability requires no authentication, no user interaction, and is easily exploitable with basic HTTP knowledge. Attackers targeting DNN installations seek quick wins for defacement, credential harvesting via injected forms, or establishing persistence through webshells.

## Defensive takeaways
- Implement mandatory authentication and authorization checks on ALL file upload endpoints, especially in default provider components
- Enforce strict whitelist-based file type validation using both MIME type checking and file extension verification
- Disable file overwriting by default; implement unique naming schemes or reject duplicate filenames
- Store uploaded files outside the web root directory or in non-executable directories with restrictive permissions
- Implement rate limiting and upload quotas to prevent abuse
- Configure web server to prevent execution of uploaded files (disable script execution in upload directories)
- Apply principle of least privilege to file upload service accounts
- Regularly audit provider components and third-party integrations for similar vulnerabilities
- Keep DNN and all extensions updated to latest patched versions

## Variant hunting
Search for other FileUploader endpoints or upload handlers in DNN provider directories
Audit other HTML editor providers (e.g., TinyMCE integration, Telerik editor) for similar issues
Review custom IHttpHandler implementations in DNN modules that process file uploads
Check for similar unauthenticated endpoints in other DNN provider services (e.g., DesktopModuleProviders, AuthenticationProviders)
Analyze any ASHX endpoints exposed in the Providers folder structure for missing authentication
Test for path traversal in upload parameters to write files outside intended directories

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1190.01 - Upload Malicious Content
- T1499.004 - HTTP Flood (potential defacement impact)
- T1207 - Website Defacement
- T1598 - Phishing (via injected XSS forms)
- T1505.003 - Web Shell Upload

## Notes
This is a pre-authentication RCE/defacement vector affecting default DNN installations. The FileUploader.ashx endpoint's public path suggests it was potentially intended for authenticated use but lacks enforcement. Organizations running DNN <10.1.1 are at immediate risk. The vulnerability likely affects multiple DNN instances as it targets core provider functionality. Investigation should verify if the fix in 10.1.1 includes authentication checks and file type enforcement.

## Full report
<details><summary>Expand</summary>

**Description:**
DNN (formerly DotNetNuke) \u003C 10.1.1 contains an unrestricted file upload vulnerability caused by the default HTML editor provider allowing unauthenticated file uploads and overwriting existing files, letting unauthenticated attackers deface websites and inject XSS payloads, exploit requires no authentication.

## References
https://nvd.nist.gov/vuln/detail/CVE-2025-64095

## Impact

Unauthenticated attackers can upload and overwrite files, leading to website defacement and cross-site scripting attacks.

## System Host(s)
█████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
#Vulnerable subdomain

https://██████████/Providers/HtmlEditorProviders/DNNConnect.CKE/Browser/FileUploader.ashx

#Testing the Vulnerability
raw POST request

██████████

## Suggested Mitigation/Remediation Actions
Update to version 10.1.1 or later.



</details>

---
*Analysed by Claude on 2026-05-24*
