# Path Traversal in file:// Protocol Handler Allows Arbitrary File Read

## Metadata
- **Source:** HackerOne
- **Report:** 3445174 | https://hackerone.com/reports/3445174
- **Submitted:** 2025-11-30
- **Reporter:** qss
- **Program:** curl
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Arbitrary File Read, Input Validation Failure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The curl file:// protocol handler fails to sanitize path traversal sequences (../) in URLs, allowing attackers to escape intended directories and read arbitrary files on the filesystem. When libcurl is used by applications processing untrusted user-supplied URLs, this becomes a remote arbitrary file read vulnerability with high impact on confidentiality.

## Attack scenario
1. Attacker identifies a web application using libcurl to fetch files based on user-provided URL parameters
2. Attacker crafts a malicious file:// URL containing path traversal sequences (e.g., file:///intended/path/../../../../../../etc/passwd)
3. Attacker submits the crafted URL through the application's input mechanism (API parameter, file path field, etc.)
4. The application passes the untrusted URL to libcurl for processing without additional validation
5. curl's file:// handler fails to strip or block the ../ sequences and resolves them, accessing files outside intended scope
6. Sensitive files (/etc/passwd, .env, database configs, private keys) are read and returned to the attacker

## Root cause
The file:// protocol handler in curl does not implement proper path normalization or validation to block directory traversal sequences before resolving file paths. The handler appears to pass directory traversal characters through without sanitization, allowing the OS filesystem to interpret them literally.

## Attacker mindset
An attacker exploiting this would recognize that many applications use curl as a library to handle URLs transparently, often in backend services processing user input. By crafting malicious file:// URLs with traversal sequences, they can bypass intended access controls and achieve unauthorized information disclosure without requiring authentication or special privileges beyond the user's own filesystem permissions.

## Defensive takeaways
- Implement strict path canonicalization and normalization for file:// URLs before accessing the filesystem, resolving all .. and . sequences
- Validate that the final resolved path remains within the intended/allowed directory scope using realpath() or equivalent
- Consider restricting file:// protocol support entirely if not explicitly needed, or require explicit allowlisting of accessible directories
- Applications using libcurl should validate and sanitize URLs from untrusted sources before passing to curl
- Apply principle of least privilege - run applications using libcurl with minimal required filesystem permissions
- Implement defense-in-depth with chroot/containerization to limit blast radius of file:// traversal attacks
- Add security warnings in libcurl documentation about dangers of processing untrusted URLs

## Variant hunting
Hunt for similar path traversal issues in other protocol handlers (gopher://, ftp://, custom protocols). Check for symlink following vulnerabilities in file:// handler. Test with URL-encoded traversal sequences (%2e%2e/). Examine whether other archive/compression protocols in curl (if any) have traversal protections. Review how other HTTP clients (urllib, requests, httpx) handle file:// URLs.

## MITRE ATT&CK
- T1190
- T1083
- T1557
- T1040

## Notes
Report demonstrates clear understanding of vulnerability scope - acknowledges limited direct impact from command-line usage but correctly identifies critical risk when libcurl is used as a library. The reproduction case is straightforward and effective. No CVE or bounty amount specified in report indicates either recent discovery or pending resolution. The vulnerability affects the file:// handler specifically, suggesting it may not impact other protocols if they have proper validation.

## Full report
<details><summary>Expand</summary>

## Summary:
The `file://` protocol handler in curl does not properly sanitise or block path traversal sequences (`../`). This allows a maliciously crafted `file://` URL to escape the intended directory and access arbitrary files on the filesystem with the permissions of the user running curl.

When curl is used as a library by another application (e.g., a web server backend) that processes user-supplied URLs, this can be escalated to a remote, arbitrary file read vulnerability.

No AI was used to find this issue or generate this report.

## Affected version
This was reproduced on the latest master branch, commit `[c3add7130d7d81add205edbbb75fdfd1f38b3c68]`.
`curl -V` output:
curl 8.18.0-DEV (x86_64-pc-linux-gnu) libcurl/8.18.0-DEV OpenSSL/3.5.4 zlib/1.3.1 libpsl/0.21.2
Release-Date: [unreleased]
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns mqtt pop3 pop3s rtsp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS HSTS HTTPS-proxy IPv6 Largefile libz NTLM PSL SSL threadsafe TLS-SRP UnixSockets

Platform: Debian GNU/Linux 13 (trixie ) running on x86_64.

## Steps To Reproduce:
1.  Clone and build the latest version of curl from the master branch.
2.  From the project's root directory, run the following command:
    ```bash
    ./src/curl "file:///any/dummy/path/../../../../../../etc/passwd"
    ```
3.  **Expected Result:** curl should fail with an error, stating that the file was not found or that the path is invalid, as it should sanitise the `../` sequences.
4.  **Actual Result:** curl successfully traverses up the directory tree and prints the contents of the `/etc/passwd` file to standard output.

## Supporting Material/References:
A screenshot of the terminal output is attached.

## Impact

This path traversal vulnerability allows for arbitrary file read. While the impact is limited when run directly by a user on the command line, it becomes **High** or **Critical** when libcurl is used by another application that constructs `file://` URLs from untrusted user input.

A remote attacker could abuse this to:
- Read sensitive configuration files (e.g., `config.php`, `.env`) containing database credentials, API keys, etc.
- Read application source code to find other vulnerabilities.
- Read system files like `/etc/passwd`, `/etc/shadow` (if running with sufficient privileges).
- Read private SSH keys or other sensitive user data.

This breaks the security boundary that should be enforced by the `file://` handler, turning any application that uses it for local file access into a potential vector for total server information disclosure.

</details>

---
*Analysed by Claude on 2026-05-24*
