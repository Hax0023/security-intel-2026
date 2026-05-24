# Arbitrary File Upload and Stored XSS via Support Request Form

## Metadata
- **Source:** HackerOne
- **Report:** 865354 | https://hackerone.com/reports/865354
- **Submitted:** 2020-05-03
- **Reporter:** z32
- **Program:** Redacted Educational Institution
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Arbitrary File Upload, Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Missing File Type Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The support request submission form fails to validate uploaded file types, allowing attackers to upload executable files and malicious documents. When support staff open these files (particularly SVG files), stored XSS payloads execute in their browser context, enabling credential theft or session hijacking.

## Attack scenario
1. Attacker creates account and navigates to Faculty/Staff IT Support section
2. Attacker completes support request form and uploads malicious SVG file containing XSS payload
3. Malicious file is stored server-side without validation and made available for download
4. Support representative downloads and opens the SVG file in their browser
5. XSS payload executes in representative's browser with their privileges
6. Attacker redirects user to fake login page, captures credentials, or performs actions as support staff

## Root cause
Lack of file type validation on upload endpoint. System accepts all file types without whitelist verification and serves them in contexts where they can be interpreted as executable code (SVG rendering, document opening).

## Attacker mindset
Exploit trust relationship between support staff and users. Target administrators/staff with higher privileges rather than end users. Use social engineering by embedding payloads in files that appear legitimate (documents, images). Leverage file format polyglots that bypass basic checks.

## Defensive takeaways
- Implement strict file type whitelist validation (check file extensions and MIME types)
- Validate file content against magic bytes/file signatures, not just extensions
- Store uploaded files outside web root or with restricted execution permissions
- Serve uploaded files with proper Content-Disposition: attachment headers to prevent in-browser execution
- Implement sandboxed file preview instead of direct download
- Educate support staff about phishing and suspicious file handling
- Use virus scanning on uploaded files
- Implement rate limiting on file uploads to prevent mass exploitation

## Variant hunting
Check other file upload endpoints (profile pictures, document submissions, etc.) for same validation bypass
Test upload filters with polyglot files (e.g., PDF+SVG, ZIP+EXE combinations)
Try bypassing with double extensions (.svg.pdf, .svg.jpg)
Test null byte injection (.svg%00.pdf)
Check if content-type headers override actual file validation
Verify if uploaded files are accessible via direct URL with predictable paths
Test SVG+XML injection payloads beyond basic XSS
Check if CSV/TSXexcel files with formulas allow formula injection

## MITRE ATT&CK
- T1190
- T1566
- T1566.001
- T1204.002
- T1105
- T1041
- T1598.003

## Notes
Report demonstrates classic file upload vulnerability combined with XSS. The attack targets support staff rather than end users, making it more likely to succeed due to expected file downloads. SVG vector graphics are particularly dangerous as they support XML/JavaScript and browsers render them directly. The credential harvesting scenario via fake login redirect is a realistic post-exploitation goal. Redactions in report suggest this may be from an educational institution's bug bounty program.

## Full report
<details><summary>Expand</summary>

**Summary:**
A malicious user can upload files of any type when submitting a support request. 

## Impact
This would allow the attacker to upload malicious executable files as well as `.html` or `.svg` files which would allow the attacker to execute malicious code on behalf of the ████ customer support representative.

## Step-by-step Reproduction Instructions

1. Browse to████████ and create an account or sign in if you already have an account.
2. Click `█████ Faculty/Staff IT Support`.
█████████
3. Click `██████ Support`
██████████
4. Complete the form and upload a file of your choice. Click Submit.
█████████
5. You will see that your request has been created, and your files are readily available for download.
█████████
6. If the customer support representative downloads the executable, their machine could be compromised. This is unlikely, however what is more likely is for the representative to open a malicious `.svg` (or `.xls`/`.doc`/etc.) file.
██████████
7. Opening the `.svg` file in a browser would fire the XSS.
███████
8. Instead of the `alert(XSS)` payload, an attacker could use `window.location` to redirect the user to a malicious website. They could also craft a fake login page that would appear to be the `████████` login page. Once the unsuspecting user submits their credentials, the malicious page would redirect the user to the real login page and the users credentials would be stored on the attackers machine.

## Suggested Mitigation/Remediation Actions
Whitelist allowed file types for upload (`.pdf`, `.jpg`, etc) as needed.

## Impact

This would allow the attacker to upload malicious executable files as well as `.html` or `.svg` files which would allow the attacker to execute malicious code on behalf of the █████ customer support representative.

</details>

---
*Analysed by Claude on 2026-05-24*
