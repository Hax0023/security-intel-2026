# Local File Inclusion via Directory Traversal in download.php

## Metadata
- **Source:** HackerOne
- **Report:** 1639364 | https://hackerone.com/reports/1639364
- **Submitted:** 2022-07-17
- **Reporter:** tokyoenigma
- **Program:** U.S. Department of Defense (bug bounty program)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Local File Inclusion (LFI), Path Traversal, Arbitrary File Download
- **CVEs:** None
- **Category:** uncategorised

## Summary
The download.php endpoint is vulnerable to directory traversal attacks through the filePathDownload parameter, allowing attackers to download arbitrary files from the server. By prepending a valid externally-facing directory path before traversal sequences (../ ), an attacker can escape the intended directory and access sensitive system files like /etc/passwd.

## Attack scenario
1. Attacker identifies a valid externally-facing directory path (e.g., data_products/MISC/frida_cal/)
2. Attacker constructs a malicious URL incorporating directory traversal sequences (../../../../) after the valid path
3. Attacker appends target file path to traverse to sensitive locations (e.g., /etc/passwd)
4. Attacker requests the crafted URL via download.php?filePathDownload parameter
5. Server fails to validate input and processes the traversal, returning the requested file
6. Attacker downloads sensitive information or, in certain configurations, executes arbitrary code

## Root cause
Insufficient input validation on the filePathDownload parameter combined with lack of path canonicalization. The application trusts user-supplied file paths directly without sanitizing directory traversal sequences or verifying that resolved paths remain within intended directories.

## Attacker mindset
An adversary would first enumerate valid externally-facing directory structures through standard web reconnaissance, then systematically test directory traversal payloads to discover which sensitive files are accessible. Knowledge of the file system structure (e.g., /etc/passwd existence) enables targeted attacks for information disclosure or privilege escalation.

## Defensive takeaways
- Implement file-by-ID mapping instead of direct file path exposure; use UUIDs or sequential IDs to reference downloadable documents
- Apply strict input validation using whitelisting of allowed file paths or directories
- Implement path canonicalization and verify that resolved paths remain within the intended base directory using realpath() or equivalent
- Disable directory listing and use access control lists to restrict file system exposure
- Implement logging and monitoring for suspicious download patterns or failed file access attempts
- Consider using a dedicated file serving mechanism or content delivery system that abstracts file paths from user input

## Variant hunting
Test other file download endpoints with similar parameter names (file, path, filePath, downloadPath)
Attempt null byte injection (....%00.jpg) on older PHP versions
Test double URL encoding (..%252f..%252f) to bypass basic filters
Check for similar traversal vulnerabilities in upload, view, or preview functionality
Test with URL-encoded traversal sequences (%2e%2e%2f) and case variations
Examine error messages and timing differences to infer file system structure

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1040

## Notes
This vulnerability is particularly severe on government (.mil) systems due to potential exposure of classified or sensitive defense information. The restriction that valid directory paths must precede traversal sequences suggests the application attempts basic security through path anchoring, but fails to properly validate. The mention of potential code execution suggests the server may serve executable content or use downloaded files in subsequent processing pipelines.

## Full report
<details><summary>Expand</summary>

Able to download arbitrary files using directory traversal via *filePathDownload* parameter provided the attacker knows a valid file path of an externally-facing document.

To reproduce:
1. Go to https://███████.mil/download.php?filePathDownload=data_products/MISC/frida_cal/../../../../../../../../etc/passwd

This appears to only work if a valid file directory that is externally-facing is utilized before the directory traversal (in this case, data_products/MISC/frida_cal/)

## Impact

The ability to download arbitrary files could lead to:
-Sensitive information disclosure
-In certain cases, code execution on the server

## System Host(s)
████.mil

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Go to https://███.mil/download.php?filePathDownload=data_products/MISC/frida_cal/../../../../../../../../etc/passwd

This appears to only work if a valid file directory that is externally-facing is utilized before the directory traversal (in this case, data_products/MISC/frida_cal/)

## Suggested Mitigation/Remediation Actions
Implement the parameter in such a way that externally-facing files are identified and referred to by IDs instead of by file path. In this way, directory traversal is not possible.
Ex. download.php?docID=d14fb1aa-dd71-4c76-8e41-ba047efb7dfe

Additionally, avoid trusting user input by validating that only expect values are submitted and accepted.



</details>

---
*Analysed by Claude on 2026-05-24*
