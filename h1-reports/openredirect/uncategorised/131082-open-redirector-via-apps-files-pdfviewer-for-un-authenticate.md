# Open Redirector via files_pdfviewer for Unauthenticated Users in ownCloud

## Metadata
- **Source:** HackerOne
- **Report:** 131082 | https://hackerone.com/reports/131082
- **Submitted:** 2016-04-15
- **Reporter:** penrose
- **Program:** ownCloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect, Client-side Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
The ownCloud PDF viewer application accepts unsanitized file parameters that can redirect unauthenticated users to arbitrary external domains. Attackers can craft malicious URLs disguised as file sharing links to redirect victims to phishing or malware distribution sites without any authentication requirements.

## Attack scenario
1. Attacker crafts a malicious URL containing files_pdfviewer endpoint with a file parameter pointing to an external attacker-controlled domain (e.g., https://demo.owncloud.org/index.php/apps/files_pdfviewer?file=https://evildomain.xx/EvilFile.pdf)
2. Attacker sends phishing email or message to targets claiming to be a file sharing notification from a legitimate ownCloud instance
3. Victim clicks the link believing they are accessing a legitimate shared file
4. The PDF viewer loads with the malicious external file reference, but the file does not display automatically
5. Victim clicks the download button in the upper right corner of the viewer interface
6. Browser is redirected to the attacker's external domain (evildomain.xx) where phishing forms, malware, or credential harvesting pages are hosted

## Root cause
The files_pdfviewer application fails to validate and sanitize the 'file' GET parameter before using it in redirect operations. The parameter is passed directly to the download functionality without checking if it references an internal ownCloud file or an external URL. No whitelist validation or URL scheme restrictions are implemented.

## Attacker mindset
Leveraging trusted institutional domains (ownCloud instances) to bypass user skepticism and redirect victims to attacker infrastructure. The attack exploits the assumption that clicks within a legitimate domain are safe, using the PDF viewer's legitimate functionality as a delivery mechanism. This is effective for phishing campaigns targeting organizations using ownCloud for file sharing.

## Defensive takeaways
- Implement strict whitelist validation for file parameters - only allow relative paths or absolute URLs pointing to internal ownCloud instances
- Validate that file paths resolve to files actually stored within the ownCloud instance before processing
- Implement URL scheme validation to reject http:// and https:// URLs in file parameters meant for local file access
- Require authentication for access to the files_pdfviewer endpoint, or at minimum require valid share tokens
- Add Content-Security-Policy headers to prevent arbitrary redirects
- Implement user warnings or confirmation dialogs when redirects to external domains are detected
- Use URL canonicalization and parsing libraries to prevent bypass techniques like encoded characters or protocol confusion
- Apply input validation at application entry points rather than relying on client-side enforcement

## Variant hunting
Check other file handler applications in ownCloud (files_imageviewer, etc.) for similar parameter injection
Test alternative parameter names (filepath, path, document, url, source) for open redirect vulnerabilities
Investigate if authentication bypass can be chained with this redirect for privilege escalation
Search for similar vulnerabilities in other file-sharing platforms using parameter-based file handling
Test URL encoding variations and double-encoding to bypass potential filtering
Check if the vulnerability exists in embedded viewer endpoints or API endpoints

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1589
- T1192

## Notes
All ownCloud installations mentioned as vulnerable. The vulnerability is particularly effective because it leverages the legitimate appearance of ownCloud URLs and the expected functionality of file viewers. The attack requires user interaction (clicking download button) but this is natural behavior when trying to access a file. The lack of authentication requirement makes this a widespread risk across all public ownCloud instances.

## Full report
<details><summary>Expand</summary>

Affected Products:  OWNCLOUD (https://demo.owncloud.org/index.php/apps/files_pdfviewer)
Version Tested: v1.0.712, other versions might be vulnerable
Class:	Open Redirector
Remote:	Yes

A non authenticated user can be easily tricked into following one of the following links in order to download a supposedly uploaded file on an owncloud instance:
The EvilFile the pdfviewer is trying to redirect will not load in the viewer automatically. But if the user clicks the download button on the right upper corner of the viewer any file will be downloaded instantly and the browser will be redirected to a different domain (ex. https://evildomain.xx ).

****OPEN REDIRECT Attack Replication Steps: 

Step 1: Visit https://demo.owncloud.org/index.php/apps/files_pdfviewer?file=https://evildomain.xx/EvilFile.xx [ Check POC1.jpg ]

Step 2: Click Download button on the right upper corner of the viewer.

Step 3: Browser is redirected to https://evildomain.xx/EvilFile.xx

Comment: No user authentication is required for the user to be redirected. All owncloud installations in the wild are vulnerable to this attack.


****Example Phishing Message with OPEN REDIRECT Attack:


Message:

Please view the files i have shared with you by following the link below, if this file is not automatically opened please click the download button on the right upper corner: 

https://demo.owncloud.org/index.php/apps/files_pdfviewer?file=https://evildomain.xx/remote.php/webdav/Demo.pdf%20%3CIf%20this%20file%20is%20not%20available%20please%20click%20the%20dowload%20button%20on%20the%20right%20upper%20corner%3E [ Check POC2.jpg ]



</details>

---
*Analysed by Claude on 2026-05-24*
