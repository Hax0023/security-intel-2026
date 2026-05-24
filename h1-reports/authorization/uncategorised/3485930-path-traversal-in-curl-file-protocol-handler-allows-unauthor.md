# Path Traversal in curl file:// Protocol Handler Allows Unauthorized File Access

## Metadata
- **Source:** HackerOne
- **Report:** 3485930 | https://hackerone.com/reports/3485930
- **Submitted:** 2026-01-03
- **Reporter:** 7hackerstar
- **Program:** curl
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Arbitrary File Read, Input Validation Failure
- **CVEs:** CVE-2021-22901
- **Category:** uncategorised

## Summary
curl's file:// protocol handler fails to validate directory traversal sequences (../) in file paths, allowing attackers to read arbitrary files on the system. The vulnerability exists in lib/file.c where paths are opened without sanitization. This affects curl 8.13.0 on Windows and potentially other platforms, enabling unauthorized access to sensitive system files.

## Attack scenario
1. Attacker crafts a malicious file:// URL containing directory traversal sequences (e.g., file://../../../../test/poc_test.txt)
2. Attacker provides this URL to an application that uses curl as its URL handler (web scraper, download manager, API client)
3. User or automated system processes the malicious URL through curl
4. curl's file:// handler fails to validate the path and does not block traversal sequences
5. The traversal sequences navigate outside the intended directory structure to access arbitrary files
6. Sensitive files (system files, private keys, configuration files, credentials) are read and returned to the attacker

## Root cause
Missing input validation in lib/file.c (lines 229-262) where file paths are directly passed to curlx_open() without sanitization or validation of directory traversal sequences. The code does not normalize or filter paths containing '../' before opening files.

## Attacker mindset
An attacker would recognize that curl is widely used in applications and systems worldwide. By exploiting the file:// protocol handler, they can gain unauthorized access to sensitive data without authentication. The simplicity of exploitation (basic path traversal syntax) combined with the widespread usage of curl makes this an attractive target for information gathering, credential harvesting, and reconnaissance.

## Defensive takeaways
- Implement strict path validation and normalization before opening files - reject or sanitize directory traversal sequences like '../' and './'
- Use canonicalization functions to resolve the absolute path and verify it remains within expected boundaries
- Implement a whitelist-based approach for allowed file paths when using file:// protocol
- Consider restricting or disabling file:// protocol support in applications where it is not required
- Add unit tests specifically for path traversal attempts in file handling code
- Apply principle of least privilege - limit file access to specific directories only
- Regularly audit protocol handlers and path manipulation code for similar vulnerabilities
- Update curl to patched versions and monitor security advisories

## Variant hunting
Search for similar path validation issues in: (1) Other protocol handlers in curl (ftp://, smb://, etc.), (2) File handling in libraries that depend on curl, (3) Other URL processing utilities and downloaders, (4) Custom implementations of file protocol handlers, (5) Path normalization logic across codebase for incomplete sanitization

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1005 - Data from Local System
- T1552 - Unsecured Credentials
- T1087 - Account Discovery

## Notes
The researcher demonstrates solid vulnerability analysis with code location identification and practical reproduction. However, the writeup references CVE-2021-22901 as a similar prior vulnerability, suggesting this may not be a novel finding or the patch from that CVE was incomplete. The Windows-specific reproduction should be tested on other platforms (Linux, macOS) to confirm scope. The severity assessment as 'High' appears appropriate given unauthenticated arbitrary file read capability, though 'Critical' may be warranted depending on default curl usage patterns and exposure. The actual HackerOne report ID (3485930) should be verified for official program response and bounty information.

## Full report
<details><summary>Expand</summary>

## Summary
During my manual review of the file path handling logic in curl's source code, I noticed the absence of proper validation for directory traversal sequences, which I then verified through practical testing. I discovered that curl allows unauthorized access to arbitrary files through the file:// protocol handler when directory traversal sequences (`../`) are used.

## Affected version
curl 8.13.0_8 (official Windows build)
Platform: Windows 10
curl version output:
curl 8.13.0 (x86_64-pc-win32) libcurl/8.13.0 OpenSSL/3.0.16 (Schannel) zlib/1.3.1 brotli/1.1.0 zstd/1.5.7 libidn2/2.3.7 libpsl/0.21.5 (+libidn2/2.3.7) libssh2/1.11.1 nghttp2/1.64.0 ngtcp2/1.12.0 nghttp3/1.8.0
Release-Date: 2025-04-02
Protocols: dict file ftp ftps gopher gophers http https imap imaps ldap ldaps mqtt pop3 pop3s rtsp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz MultiSSL NTLM PSL SPNEGO SSL SSPI TLS-SRP UnixSockets zstd

## Vulnerable Code Location
The vulnerability exists in `lib/file.c` at lines 229-262 where file paths are not properly validated before opening:

```c
/* Line 229: No validation of "../" sequences */
fd = curlx_open(actual_path, O_RDONLY | CURL_O_BINARY);

/* Similar issues at lines 253, 258, 262 */
fd = curlx_open(real_path + 1, O_RDONLY);  // Line 253
fd = curlx_open(real_path, O_RDONLY);     // Line 258
fd = curlx_open(real_path, O_RDONLY);     // Line 262

This code fails to check for directory traversal sequences before opening files. When I reviewed these lines, I noticed there's no validation to prevent paths containing `../` from accessing files outside the intended directory structure.

## Steps To Reproduce
1. Download the official curl Windows build from: https://curl.se/windows/dl-8.13.0_8/curl-8.13.0_8-win64-mingw.zip
2. Extract the archive and navigate to the `bin` directory
3. Create a test file at `C:\test\poc_test.txt` with content:
This is a test file for Path Traversal vulnerability
4. Execute the following command in the same directory as curl.exe:
```bash
curl "file://../../../../test/poc_test.txt"
During my testing, I observed the file contents displayed successfully, proving unauthorized access to files outside the intended directory.
Supporting Material/References
Screenshot showing successful file access (Capture.PNG) - captured during my actual testing on Windows 10
Proof of Concept script (final_poc.bat) demonstrating the vulnerability step by step
Test file used in reproduction (poc_test.txt) with the exact content I tested with
Reference to similar vulnerability: CVE-2021-22901 (shows this pattern has occurred before)

## Impact

This vulnerability allows attackers to read arbitrary files from the system when processing malicious file:// URLs. The impact includes:

Sensitive data exposure: System files (hosts, password databases), user documents, and private keys can be accessed. During my testing, I was able to read files from completely different directories, which shows how serious this is.
Information disclosure: System configuration, installed software details, and network settings can be enumerated. This could provide attackers with detailed information about the target system.
Chained attacks: Can be combined with other vulnerabilities for full system compromise. For example, reading configuration files might reveal credentials for other services.
Remote exploitation: Applications that process user-supplied URLs with curl (web scrapers, API clients, download managers) can be exploited remotely. Many developers don't realize that file:// URLs can be dangerous.
The severity is High because:

No authentication required for exploitation - any attacker can craft a malicious URL
Affects confidentiality of sensitive system data - the core security boundary is violated
Present in the latest official release - affects all Windows users of the current version
Simple to exploit with minimal technical skill - I was able to reproduce it with just a few simple commands
This isn't just a theoretical issue. In my hands-on testing on Windows 10, I successfully accessed files outside the intended directory structure, proving real-world exploitability. The vulnerability is particularly concerning because curl is used in countless applications and systems worldwide.

</details>

---
*Analysed by Claude on 2026-05-24*
