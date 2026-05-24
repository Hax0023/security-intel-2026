# Unrestricted File Upload - HTML/SHTML Files on Starbucks China Recruitment Portal

## Metadata
- **Source:** HackerOne
- **Report:** 412481 | https://hackerone.com/reports/412481
- **Submitted:** 2018-09-21
- **Reporter:** b006e4ea768a5d1b5340969
- **Program:** Starbucks
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Unrestricted File Upload, Insufficient File Type Validation, Information Disclosure, Server-Side Template Injection
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Starbucks China recruitment portal (ecjobsdc.starbucks.com.cn) contains an unrestricted file upload vulnerability allowing attackers to upload HTML and SHTML files by bypassing file extension validation. Uploaded files can be accessed directly, enabling information disclosure of internal IP addresses, file paths, and potentially sensitive configuration data.

## Attack scenario
1. Attacker identifies the file upload endpoint at /recruitjob/hxpublic_v6/hxinterface6.aspx?_hxcategory=hx_filebox_upload_file
2. Attacker crafts a multipart POST request with a malicious SHTML file containing embedded code (PHP/ASP/etc.)
3. File extension bypass occurs - the application accepts .shtml extension instead of blocking dangerous formats
4. Server stores the file in accessible directory: /recruitjob/tempfiles/ with a temporary filename
5. Attacker accesses the uploaded file via direct URL, triggering server-side processing
6. Attacker extracts sensitive information (internal IPs, file paths, web.config) or performs phishing/malware distribution

## Root cause
The file upload handler uses insufficient validation - likely checking only the original filename extension in a blacklist manner without proper content-type validation, MIME type verification, or whitelisting safe extensions. The application processes SHTML files server-side, and stores uploads in a web-accessible directory without execution restrictions.

## Attacker mindset
An attacker would recognize this as a critical information gathering vector for a major corporation. The ability to extract internal network topology (10.92.29.50), server paths (D:\TrustHX\STBKSERM101\), and configuration details enables: (1) further reconnaissance for lateral movement, (2) phishing campaigns leveraging legitimate Starbucks infrastructure, (3) potential credential harvesting through malicious forms, and (4) supply chain attack preparation.

## Defensive takeaways
- Implement strict whitelist-based file extension validation (allow only: jpg, png, pdf, doc, docx)
- Validate MIME types on both client and server side using proper libraries, not just Content-Type headers
- Store uploaded files outside the web root or in a non-executable directory (e.g., /var/uploads/ with noexec mount)
- Rename uploaded files to random names and strip original extensions entirely
- Disable script execution in upload directories via web server config (.htaccess, web.config, nginx directives)
- Implement Content-Disposition: attachment headers to prevent inline execution
- Scan uploaded files with antivirus/malware detection before storage
- Use Content Security Policy (CSP) headers to restrict script execution origins
- Implement proper access controls and rate limiting on upload endpoints
- Regularly audit file upload functionality and monitor uploaded file access patterns

## Variant hunting
Search for similar upload endpoints in subdomains of starbucks.com.cn and other recruitment/HR portals. Check for: (1) other file extensions that bypass filters (.shtm, .xhtml, .jhtml, .sht), (2) double extension attacks (.html.jpg), (3) null byte injection (.shtml%00.jpg), (4) case variation (.SHTML, .ShTmL), (5) MIME type confusion, (6) path traversal in filename (../../malicious.html), (7) other HuaXun TrustHX systems in Starbucks infrastructure

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1583.002 - Acquire Infrastructure: Web Services
- T1562 - Indicator Removal
- T1589 - Gather Victim Identity Information
- T1592 - Gather Victim Host Information

## Notes
The vulnerability leverages a popular business HR system (HuaXun/TrustHX) suggesting potential systemic risks across multiple organizations using the same platform. The exposure of internal IP ranges (10.92.x.x) and Windows file paths indicates poor security hardening. The presence of web.config file exposure is particularly critical as it may contain connection strings and other sensitive configuration. This appears to be a Mainland China Starbucks-specific domain, limiting direct impact but still affecting HR/recruitment data security.

## Full report
<details><summary>Expand</summary>

### 1, Summary
During the test, I found ecjobsdc.starbucks.com.cn this site has an upload vulnerability, you can upload html and shtml format files, so you can read the server's intranet IP, the physical address of the website application and read the website web.config file.
###2, Vulnerability scope
https://ecjobsdc.starbucks.com.cn
###3, proof of exploit

By modifying the suffix of filename, this address can be uploaded to upload html and shtml files, so that you can read the server's intranet IP, the physical address of the website application, and the configuration file of the website.
Vulnerability certificate

```
POST /recruitjob/hxpublic_v6/hxinterface6.aspx?_hxcategory=hx_filebox_upload_file HTTP/1.1
Host: ecjobsdc.starbucks.com.cn
Connection: close
Content-Length: 234
Cache-Control: max-age=0
Origin: null
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryevPInYidBxSvSd06
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9

------WebKitFormBoundaryevPInYidBxSvSd06
Content-Disposition: form-data; name="hxwebfileboxcontrol_upload_file_inputbox"; filename="xxx.shtml"
Content-Type: text/html

<?php echo 1111;>
------WebKitFormBoundaryevPInYidBxSvSd06--
```

Successfully read the website's remoteaddr webpathinfo web.config file.

```
DOCUMENT_NAMED:\TrustHX\STBKSERM101\www_app\tempfiles\temp_uploaded_34afb246-02f1-4cb0-978d-15805c2a05c8.shtml
SERVER_SOFTWARE :Microsoft-IIS/8.5
SERVER_NAME :ecjobsdc.starbucks.com.cn
SERVER_PORT :80
REMOTE_ADDR:10.92.29.50
REMOTE_HOST:10.92.29.50
D:\TrustHX\STBKSERM101\www_app\tempfiles\temp_uploaded_34afb246-02f1-4cb0-978d-15805c2a05c8.shtml
PATH_INFO:/recruitjob/tempfiles/temp_uploaded_34afb246-02f1-4cb0-978d-15805c2a05c8.shtml
text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
/recruitjob/tempfiles/temp_uploaded_34afb246-02f1-4cb0-978d-15805c2a05c8.shtml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <httpRedirect enabled="false" destination="https://ecjobs.starbucks.net" exactDestination="false" />
    </system.webServer>
</configuration>
```
{F349302}
{F349303}

## Impact

Phishing attack, remote file reading

</details>

---
*Analysed by Claude on 2026-05-24*
