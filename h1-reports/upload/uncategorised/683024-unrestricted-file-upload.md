# Unrestricted File Upload via Authentication Bypass in FileCloud UI

## Metadata
- **Source:** HackerOne
- **Report:** 683024 | https://hackerone.com/reports/683024
- **Submitted:** 2019-08-27
- **Reporter:** javilarx8
- **Program:** U.S. Department of Defense / Military Organization
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Authentication Bypass, Unrestricted File Upload, Arbitrary File Write, Insufficient Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
A FileCloud instance failed to enforce authentication on a public mode endpoint, allowing unauthenticated users to upload arbitrary files including executables to a .mil domain. By navigating to a specially crafted URL with mode=public parameter, attackers could bypass authentication and gain read/write access to shared directories without credentials.

## Attack scenario
1. Attacker discovers the vulnerable FileCloud instance and identifies the authentication-required UI endpoint
2. Attacker appends mode=public parameter and navigates to the unprotected public endpoint
3. Attacker uses the web interface to create arbitrary subdirectories within SHARED folders
4. Attacker uploads malicious files including executables (e.g., putty.exe, backdoors, RATs) to the accessible directories
5. Attacker hosts these files on the .mil domain for distribution or creates malware distribution infrastructure
6. Attacker performs targeted social engineering attacks using legitimate .mil domain URLs to host phishing payloads

## Root cause
The application implements mode=public parameter that disables authentication checks on the UI endpoint without validating that the public mode should only apply to read-only or strictly limited operations. Access control logic fails to enforce authentication across all file upload endpoints, treating the mode parameter as a blanket permission mechanism rather than a scoped restriction.

## Attacker mindset
An attacker recognizes that .mil domains carry inherent trust and legitimacy, making them ideal for malware distribution and social engineering campaigns. By leveraging the authentication bypass, the attacker can weaponize government infrastructure for widespread attacks with minimal detection risk due to domain reputation.

## Defensive takeaways
- Never use URL parameters alone to control authentication state; implement server-side session validation on every request
- Apply principle of least privilege: mode=public should only enable specific read operations, never write/upload capabilities
- Implement allowlist-based file type restrictions at multiple layers (client, server, filesystem) and block executables (.exe, .com, .bat, .scr, .msi, etc.)
- Enforce authentication checks before processing any file upload requests, independent of UI routing or mode parameters
- Implement comprehensive input validation on all path parameters to prevent directory traversal and unauthorized directory creation
- Apply Content Security Policy and serve uploads with correct MIME types to prevent execution in browser context
- Conduct security code review of authentication bypass logic, particularly around conditional authentication mechanisms
- Monitor file uploads for suspicious patterns (executable uploads, unusual paths) and alert on anomalies
- Implement strict CORS and referrer policies to prevent cross-origin file uploads

## Variant hunting
Search for other mode parameters (mode=guest, mode=limited, mode=preview) that may bypass authentication
Test for similar bypasses on other endpoints: download.html, export.html, share.html with public/guest parameters
Investigate whether direct API calls to /api/upload or /api/files endpoints bypass authentication checks
Check if authentication can be bypassed by modifying other URL parameters: ?auth=false, ?bypass=true, ?role=public
Test if path traversal (../ sequences) in the mode or directory parameters can access protected areas
Verify if removing/modifying authentication cookies allows continued file operations
Search for other SaaS file sharing platforms using similar mode-based access control patterns
Test whether file upload restrictions can be bypassed by using double extensions (.exe.jpg) or null bytes

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1574 - Hijack Execution Flow (via executable upload)
- T1566 - Phishing (using .mil domain for credibility)
- T1105 - Ingress Tool Transfer (uploading malware)
- T1657 - Defense Evasion via Trusted Domain
- T1204 - User Execution (social engineering with legitimate domain)
- T1071 - Application Layer Protocol (HTTP/HTTPS file upload)
- T1534 - Internal Spearphishing (leveraging .mil domain authority)

## Notes
This vulnerability is particularly severe due to the .mil domain context, which implies government/military infrastructure. The combination of authentication bypass + unrestricted file upload + executable hosting capability creates a critical vulnerability suitable for malware distribution campaigns and sophisticated social engineering attacks. The FileCloud software vendor should issue emergency patches. Organizations running FileCloud should immediately audit public-accessible instances and implement network-level restrictions blocking anonymous uploads.

## Full report
<details><summary>Expand</summary>

**Summary:**
The endpoint at https://███████/ui/core/index.html required authentication, but navigating to https://█████/ui/core/index.html?mode=public#expl-tabl./SHARED/rpchllmd/CSAT allow for read/write access.

**Description:**
The endpoint at https://████/ui/core/index.html?mode=public#expl-tabl./SHARED/rpchllmd/CSAT allowed for read as well as write access. It was possible to create directories and upload images as well as .exe files such as putty.exe. 

## Impact
An attacker can attempt to use the site to host malware, or perform social engineering attacks since the domain URL will be a .mil address.

## Step-by-step Reproduction Instructions

1. Navigate to:
https://████/ui/core/index.html?mode=public#expl-tabl./SHARED/rpchllmd/CSAT
2. Create sub-directory 
3. Upload test files
4. Files are then uploaded and hosted on a .mil website without authenticating to the application.

## Product, Version, and Configuration (If applicable)
FileCloud software
https://www.getfilecloud.com/
## Suggested Mitigation/Remediation Actions
Enforce authentication on endpoints of the application, restrict file uploads to only necessary business requirements. If possible restrict uploads to .jpg .pfd .docx. Don't allowed upload of executable files

## Impact

An attacker can attempt to use the site to host malware, or perform social engineering attacks since the domain URL will be a .mil address.

</details>

---
*Analysed by Claude on 2026-05-24*
