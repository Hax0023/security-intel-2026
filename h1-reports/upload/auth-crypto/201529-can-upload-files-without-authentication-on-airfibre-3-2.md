# Unauthenticated File Upload in AirFibre 3.2

## Metadata
- **Source:** HackerOne
- **Report:** 201529 | https://hackerone.com/reports/201529
- **Submitted:** 2017-01-27
- **Reporter:** simongurney
- **Program:** AirFibre 3.2
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Authentication, Unrestricted File Upload, Denial of Service
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The AirFibre 3.2 device allows unauthenticated file uploads to the /tmp/upload directory through the login.cgi endpoint. An attacker can exploit this to fill disk space causing denial of service, and potentially chain it with local file inclusion vulnerabilities for greater impact.

## Attack scenario
1. Attacker identifies the login.cgi endpoint on the AirFibre device at the target IP address
2. Attacker crafts a multipart/form-data POST request with a file payload without providing authentication credentials
3. The request is sent directly to login.cgi which fails to validate authentication before processing file uploads
4. File is accepted and written to /tmp/upload directory on the device
5. Attacker uploads multiple large files repeatedly to exhaust disk space
6. Device disk becomes full, causing system instability, service degradation, or complete denial of service

## Root cause
The login.cgi endpoint implements file upload functionality but fails to check authentication status before accepting and storing uploaded files. The endpoint processes file submissions without validating user credentials.

## Attacker mindset
An attacker would recognize that authentication bypass on file upload functionality provides immediate DoS capability. They would also consider chaining this with other vulnerabilities (LFI, path traversal) to achieve code execution or data exfiltration, viewing this as a stepping stone for multi-stage attacks.

## Defensive takeaways
- Implement authentication checks BEFORE any file processing logic in upload handlers
- Validate authentication tokens/sessions at the earliest point of request processing
- Implement upload quotas and disk space monitoring to prevent DoS via resource exhaustion
- Restrict upload directories to non-executable locations and use randomized file names
- Apply strict file type validation and disallow executable extensions
- Implement rate limiting on upload endpoints
- Use Web Application Firewalls to block unauthenticated file upload attempts
- Regularly audit authentication logic in administrative and sensitive endpoints

## Variant hunting
Search for other CGI endpoints that may bypass authentication (admin.cgi, upload.cgi, config.cgi, backup.cgi). Test POST requests to authenticated-only endpoints without credentials. Check for path traversal in upload functionality to write to sensitive directories.

## MITRE ATT&CK
- T1190
- T1190
- T1499
- T1600

## Notes
The vulnerability is particularly concerning because it leverages the login.cgi endpoint itself—typically a critical authentication mechanism—to bypass security. The researcher notes inability to achieve RCE directly but acknowledges chaining potential with LFI, indicating this is part of a larger attack surface.

## Full report
<details><summary>Expand</summary>

A POST submission such as below will upload a file to the tmp/upload directory without requiring authentication.  I have been unable to redirect the upload to another directory so cannot utilize for RCE however an attacker is able to use this to fill the disk space on the device which could cause a DoS.  

This could be combined with another vulnerability such as an LFI.

POST http://1[ip]/login.cgi HTTP/1.1
Proxy-Connection: keep-alive
Content-Length: 5179
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryRfhSBNfoYzLOvXnc
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.8
Host: 1[ip]

------WebKitFormBoundaryRfhSBNfoYzLOvXnc
Content-Disposition: form-data; name="file"; filename="test6.txt"
Content-Type: text/plain

aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

------WebKitFormBoundaryRfhSBNfoYzLOvXnc--




</details>

---
*Analysed by Claude on 2026-05-24*
