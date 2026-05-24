# Directory Traversal in File Download Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1641148 | https://hackerone.com/reports/1641148
- **Submitted:** 2022-07-18
- **Reporter:** 0x45
- **Program:** DoD (Department of Defense)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Directory Traversal, Path Traversal, Arbitrary File Read
- **CVEs:** None
- **Category:** uncategorised

## Summary
A directory traversal vulnerability exists in the /File/Download endpoint where the 'path' parameter accepts absolute Windows file paths without validation, allowing attackers to read arbitrary sensitive files from the server. An attacker can directly access system files such as C:/WINDOWS/System32/drivers/etc/hosts and other sensitive configuration files by manipulating the path parameter.

## Attack scenario
1. Attacker discovers the /File/Download endpoint accepts a 'path' parameter
2. Attacker crafts a GET request with an absolute Windows path (e.g., C:/WINDOWS/System32/drivers/etc/hosts)
3. Server fails to validate or sanitize the path parameter
4. Application processes the absolute path and returns the file contents
5. Attacker gains access to sensitive system files, configuration data, or application secrets
6. Attacker escalates by enumerating other sensitive paths (web.config, application binaries, etc.)

## Root cause
The application directly uses user-supplied 'path' parameter to construct file system requests without implementing proper input validation, path normalization, or restricting access to intended directories. The endpoint does not enforce a whitelist of allowed paths or use secure file serving patterns.

## Attacker mindset
Information gathering and reconnaissance. An attacker seeks to extract sensitive system information, credentials in configuration files, or application source code to plan further attacks. The ease of exploitation makes this an attractive initial vector for lateral movement or privilege escalation.

## Defensive takeaways
- Implement strict input validation: reject absolute paths and only accept relative paths within a designated safe directory
- Use a whitelist of allowed files/directories rather than blacklist approaches
- Implement path canonicalization and verify resolved paths are within the intended base directory
- Run application with minimal file system permissions and disable access to system directories
- Use secure file serving APIs that abstract path handling rather than direct file system access
- Log and monitor suspicious path patterns (../, absolute paths, system directories)
- Consider using a dedicated secure file download handler or CDN rather than raw file system access

## Variant hunting
Test with URL encoding: %2e%2e%2f (../) and double encoding
Test with backslashes: C:\WINDOWS\System32 on Windows servers
Test with case variations and alternate path separators
Check if path parameter appears in other endpoints (Download, View, Export, Get, Retrieve)
Test symbolic link following behavior
Verify if authentication/authorization checks are bypassed for certain system paths
Test parameters like: filepath, file, filePath, document, resource, content, etc.

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1057

## Notes
The report is from a DoD program, indicating critical infrastructure or government systems. ASP.NET Core technology stack identified from antiforgery token naming. Report quality is low with redacted information; however, the vulnerability is clearly reproducible and critical. The presence of antiforgery tokens suggests some CSRF protection but no path validation. Windows-specific paths indicate the server OS. This is a classic OWASP A01:2021 (Broken Access Control) vulnerability that should be immediately remediated in DoD systems.

## Full report
<details><summary>Expand</summary>

Hi  DoD!

I found directory traversal vulnerability at ████. I didn't find available title for this issue that's why I selected remote file inclusion.

###  Host: ██████
###  Vulnerability: Directory Traversal in Windows Server
###  Tool Used: BurpSuite

### Parameter:  ==path==

###HTTP GET Request###
==GET /File/Download?path=C:/WINDOWS/System32/drivers/etc/hosts==

### Response

███

## Impact

Attacker could read sensitive file in server

## System Host(s)
███████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Make HTTP Request like that;

GET /File/Download?path=C:/WINDOWS/System32/drivers/etc/hosts HTTP/1.1
Host: ███
Cookie: .AspNetCore.Antiforgery.GupjSGuR2ZQ=CfDJ8GfYfRi9j8NNoBU6zVTpTKTbaG72CuADzxVVYVr9efssbxXYtgzCMF2H6PvdOcF0RxMExCsaObiVNuop1ouJa2Nb0k3z4KYTy2ih_nRbxREcZZo-3LBJPXq05kvRrRF6p02TakoqGzC6VUTdPRw-bo8; TimeZoneOffset=-240
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="103", ".Not/A)Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

## Suggested Mitigation/Remediation Actions
Input Validation for path parameter



</details>

---
*Analysed by Claude on 2026-05-24*
