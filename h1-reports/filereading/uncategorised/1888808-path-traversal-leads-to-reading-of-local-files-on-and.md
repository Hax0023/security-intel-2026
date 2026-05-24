# Path Traversal in Download Endpoint Allows Reading Arbitrary Files

## Metadata
- **Source:** HackerOne
- **Report:** 1888808 | https://hackerone.com/reports/1888808
- **Submitted:** 2023-02-28
- **Reporter:** rodriguezjorgex
- **Program:** Private program (redacted)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Directory Traversal, CWE-22: Improper Limitation of a Pathname to a Restricted Directory
- **CVEs:** None
- **Category:** uncategorised

## Summary
The downloadForm endpoint on the login page accepts a filename parameter that is vulnerable to path traversal attacks, allowing unauthenticated attackers to read arbitrary files from the server filesystem. An attacker can use relative path sequences (../) to traverse parent directories and access sensitive files such as /etc/hosts and potentially /etc/passwd.

## Attack scenario
1. Attacker discovers the downloadForm endpoint is accessible from the unauthenticated login page
2. Attacker identifies that the filename parameter is not properly validated or sanitized
3. Attacker crafts a malicious URL with directory traversal sequences (../../../../etc/hosts) to access files outside the intended download directory
4. Server processes the request without proper path validation and returns the requested file
5. Attacker downloads sensitive system files like /etc/hosts or configuration files containing credentials
6. Attacker uses disclosed information to escalate privileges or gain unauthorized system access (e.g., via SSH keys)

## Root cause
The application fails to validate and sanitize the filename parameter, allowing directory traversal sequences to navigate the filesystem. The file serving mechanism directly uses user-supplied input to construct file paths without using secure functions like basename() or realpath() to constrain access to the intended directory.

## Attacker mindset
An attacker would view this as a low-effort, high-impact vulnerability accessible without authentication. The attacker would systematically traverse the filesystem to enumerate available files, with particular interest in configuration files, credentials, SSH keys, and other sensitive data that could enable lateral movement or privilege escalation.

## Defensive takeaways
- Implement strict input validation on all file operation parameters, rejecting or encoding special characters like dots and slashes
- Use whitelist-based validation to only allow alphanumeric filenames or known safe patterns
- Employ secure file handling functions (basename(), realpath(), Path.resolve()) that prevent directory traversal
- Store downloadable files in a dedicated directory outside the web root and use an internal mapping system (ID-to-filename) instead of accepting raw filenames
- Implement proper authentication and authorization checks for file download endpoints, even on login pages
- Configure WAF rules to detect and block common path traversal patterns across all endpoints
- Apply principle of least privilege to the application's file system access permissions
- Conduct regular security testing including path traversal fuzzing on all file operation endpoints

## Variant hunting
Search for similar download/export endpoints accepting file parameters; check for path traversal in document preview, export, report generation, and attachment download features; test for traversal bypasses using encoding (URL encoding, double encoding, Unicode), null bytes, backslashes vs forward slashes, and alternate path separators; verify if other parameters like folder/directory are also vulnerable

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1005: Data from Local System
- T1552: Unsecured Credentials

## Notes
The report indicates WAF protection may be blocking /etc/passwd access, suggesting the organization has some defensive measures in place but incomplete coverage. The vulnerability is unauthenticated and requires no special privileges, making it easily exploitable. The attacker demonstrates good understanding of escalation potential (SSH keys via user enumeration). The redacted nature of the target suggests the program may be a private/enterprise program with responsible disclosure practices.

## Full report
<details><summary>Expand</summary>

**Description:**
The ██████████ web application has a feature that allows the downloading of files when you first go to the login screen. The endpoint that manages those downloads is the downloadForm endpoint with the filename parameter.

https://███/████/login/downloadForm?filename=█████

The filename parameter has a directory traversal vulnerability which allows an attacker to add two (2) dots and a backslash (../) to traverse parent directories and view files that are not meant to be viewed.

POC:
Viewing /etc/hosts file

Using bash, run the following command:
curl https://█████████/███/login/downloadForm?filename=../../../../../../../../etc/hosts

Or simply access the POC URL in a web browser, and the hosts file will be downloaded to the workstation.

Initially, I attempted to read the /etc/passwd file, but I believe there's some form of WAF blocking the request. I didn't attempt to bypass the WAF, but if the WAF is bypassed the /etc/passwd file contains sensitive information about the users in the system. Furthermore, with the user information, an attacker can attempt to view the id_rsa keys of users in the system to gain ssh access to the server.

## References
https://portswigger.net/web-security/file-path-traversal

## Impact

A directory traversal vulnerability that allows an attacker to read files on a system can have serious consequences, depending on the sensitivity of the information that can be accessed. Here are a few examples of the potential impact:

Disclosure of sensitive information: An attacker who can read files on a system can potentially access sensitive information such as user credentials, financial records, confidential business information, or other sensitive data. This could lead to identity theft, data breaches, or other forms of fraud.

System compromise: In some cases, directory traversal vulnerabilities can be used to read sensitive configuration files or scripts that can be used to gain full access to the system. Once an attacker has access to the system, they can execute arbitrary code, install malware, or take other actions that can compromise the system's security.

Reputation damage: If sensitive information is leaked due to a directory traversal vulnerability, it can damage the reputation of the organization responsible for the system. This can have serious consequences for businesses, particularly those in industries where trust and confidentiality are critical.
Overall, a directory traversal vulnerability that allows an attacker to read files can be a serious security risk that should be addressed as soon as possible to minimize the potential impact.

## System Host(s)
██████,███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Visit https://██████████/████/login/downloadForm?filename=../../../../../../../../etc/hosts

## Suggested Mitigation/Remediation Actions
Validate user input: One of the most common causes of directory traversal vulnerabilities is insufficient validation of user input. To prevent this, all user input should be validated to ensure that it is within expected bounds and does not contain characters that could be used to navigate outside of the intended directory.

Sanitize file paths: Before accessing files, all file paths should be sanitized to remove any characters that could be used to navigate outside of the intended directory.

Use secure coding practices: Developers should follow secure coding practices to prevent common vulnerabilities, such as directory traversal attacks. This includes using functions that are designed to handle file operations safely, such as realpath() or basename(), and avoiding the use of user input to construct file paths.



</details>

---
*Analysed by Claude on 2026-05-24*
