# Unrestricted File Upload via URL Parameter Manipulation on auth.ratelimited.me

## Metadata
- **Source:** HackerOne
- **Report:** 463604 | https://hackerone.com/reports/463604
- **Submitted:** 2018-12-17
- **Reporter:** daniel_v
- **Program:** Rate Limited
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Unrestricted File Upload, Insufficient Input Validation, URL Parameter Tampering
- **CVEs:** None
- **Category:** uncategorised

## Summary
An authenticated user can upload arbitrary files by intercepting the profile photo change request and manipulating the 'url' parameter to point to non-image files, bypassing client-side and server-side validation checks. While code execution was not demonstrated, the vulnerability allows circumvention of intended file type restrictions present in the direct upload functionality.

## Attack scenario
1. Attacker authenticates to https://auth.ratelimited.me/
2. Attacker initiates profile photo change and intercepts the HTTP request using a proxy tool
3. Attacker modifies the 'url' parameter from a legitimate image URL to a malicious file URL (e.g., .txt, .php, .exe, .pdf)
4. Attacker forwards the modified request to the server
5. Server accepts and stores the file without proper validation of the URL target's content type
6. Attacker can later reference or download the uploaded non-image file, potentially triggering further attacks

## Root cause
The application implements file type validation only on the direct 'upload photo' endpoint but fails to validate files referenced via URL in the 'gravatar' option. The 'url' parameter is processed server-side without verifying that the resource at that URL is actually an image file, relying solely on the user-supplied parameter.

## Attacker mindset
The attacker methodically tested multiple file upload vectors, discovered inconsistent validation logic between upload methods, and recognized that URL-based uploads bypass intended restrictions. While acknowledging inability to execute code, the attacker correctly identified the security gap as worth reporting.

## Defensive takeaways
- Implement consistent file type validation across all file upload mechanisms (direct upload, URL-based, external services)
- Validate file content-type and magic bytes server-side, not just file extension
- Fetch and validate remote URLs before processing; verify MIME type matches expected values
- Implement allowlist of permitted file types rather than blocklist approach
- For external URLs (Gravatar), validate both the response Content-Type header and actual file content
- Apply the same strict validation rules to all photo change options (upload, Gravatar, no photo)
- Consider sandboxing or isolating user-uploaded content to prevent abuse

## Variant hunting
Check other user-uploaded content endpoints (avatar, banner, documents) for similar URL parameter bypasses
Test social login integrations that may reference external profile images
Investigate if stored file URLs are later processed or rendered, creating secondary vulnerabilities
Examine API endpoints that accept 'image_url' or similar parameters
Test whether uploaded files can be accessed directly and potentially served with incorrect Content-Type
Check if file validation differs between authenticated and unauthenticated endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link

## Notes
This is a well-structured, clear report demonstrating methodical testing. The researcher appropriately acknowledged the limitation (no RCE achieved) while correctly identifying the underlying vulnerability. The report would have been stronger with: (1) proof of concept showing a non-image file successfully stored, (2) investigation of potential secondary impacts (malware distribution, data exfiltration via stored files), (3) testing of file access controls. The 'Ps2' note demonstrates good security awareness - the researcher recognized inconsistent validation patterns, a key indicator of implementation flaws.

## Full report
<details><summary>Expand</summary>

Hello security team,

Have found a way to upload files that aren't images on https://auth.ratelimited.me/

Steps to reproduce:

1. Login at https://auth.ratelimited.me/
2. Click "change photo" and intercept with a tool (used burpsuite)
3. Choose "gravatar" option and change the 'url' parameter to anything you would like
4. Done
Ps: The same occurs when you intercept "no photo" option

Ps2: I could not execute code through this, but i thought it was a valid report because i tried to upload .txt files in "upload photo" options and it was not allowed.

If you need further information, please contact me
Best Regards,
Daniel

## Impact

possibility of uploading anything rather than images

</details>

---
*Analysed by Claude on 2026-05-24*
