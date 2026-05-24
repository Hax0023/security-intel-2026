# Information Disclosure: System Username and Server Metadata in x-amz-meta-s3cmd-attrs Header

## Metadata
- **Source:** HackerOne
- **Report:** 667032 | https://hackerone.com/reports/667032
- **Submitted:** 2019-08-04
- **Reporter:** ninja_cyber007
- **Program:** data.gov
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Improper Access Control, Server Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
The x-amz-meta-s3cmd-attrs response header on data.gov exposes sensitive system metadata including username (root), group information, file permissions, and timestamps through S3 custom metadata attributes. This information was stored during file uploads using s3cmd without the --no-preserve flag, leaking Unix file ownership and permission details to any requester.

## Attack scenario
1. Attacker sends HTTP POST request to https://www.data.gov/app/plugins/advanced-custom-fields/core/api.php
2. Server responds with S3 object containing custom metadata headers
3. Attacker examines x-amz-meta-s3cmd-attrs response header in HTTP response
4. Attacker extracts sensitive information: uid:0 (root user), gname:root, gid:0, file permissions (mode:33184)
5. Attacker correlates username 'root' with other reconnaissance data to identify running processes or privilege levels
6. Information aids in privilege escalation planning or social engineering attacks targeting system administrators

## Root cause
Files were uploaded to AWS S3 using s3cmd tool without the --no-preserve flag, causing Unix file metadata (ownership, permissions, timestamps) to be stored as custom x-amz-meta-s3cmd-attrs headers. These headers are accessible in HTTP responses to any client requesting the S3 object, violating the principle of least privilege for metadata exposure.

## Attacker mindset
Reconnaissance and information gathering. An attacker searches for publicly accessible data on government websites, discovering that S3 metadata leaks system-level information. While a single username may seem low-impact, it provides reconnaissance value: confirming file ownership by root suggests privileged processes, identifying naming conventions used by the organization, and potentially mapping infrastructure details.

## Defensive takeaways
- Never use s3cmd upload without the --no-preserve flag when uploading to public or semi-public S3 buckets
- Implement S3 bucket policies to prevent inclusion of sensitive metadata in object responses
- Review and sanitize all custom metadata headers before exposing objects publicly
- Use AWS S3 Block Public Access settings and ensure bucket policies don't expose sensitive headers
- Implement header filtering at CloudFront or WAF layer to strip x-amz-meta-* headers from public responses
- Regularly audit S3 object metadata and headers for unintended information disclosure
- Establish guidelines for secure file uploads specifying metadata preservation restrictions
- Use AWS S3 Object Metadata Lock or versioning to prevent inadvertent metadata exposure during migrations

## Variant hunting
Look for other x-amz-meta-* custom headers on public S3 buckets or CloudFront distributions that may leak application secrets, internal paths, build information, or database credentials. Check for similar metadata leaks in other government/public sector cloud deployments using s3cmd or similar tools. Search for instances where backup tools, deployment scripts, or file sync utilities preserve system metadata on cloud-hosted files.

## MITRE ATT&CK
- T1526 - Exposure of Sensitive System Information (reconnaissance)
- T1592.004 - Gather Victim Host Information (system details)
- T1087 - Account Discovery (username enumeration)
- T1580 - Cloud Infrastructure Discovery

## Notes
The severity is marked as Low because the exposed information (root username) alone has limited exploitability. However, this is a clear example of unintended information leakage that violates security best practices. In combination with other vulnerabilities or reconnaissance data, revealing the root user could facilitate privilege escalation attacks. The issue stems from a deployment/configuration error rather than application code vulnerability. The referenced s3tools/s3cmd GitHub issue #67 provides context on the underlying tool behavior.

## Full report
<details><summary>Expand</summary>

Hi Team,

I noticed, that the x-amz-meta-s3cmd-attrs  response header returns sensitive information, like system username on data.gov

x-amz-meta-s3cmd-attrs: uid:0/gname:root/uname:root/gid:0/mode:33184/mtime:1513269652/atime:1513269652/md5:2049644b6b833f5dbb826f60a4721f64/ctime:1513269652

Server: AmazonS3

Steps to reproduce:

1. POST  https://www.data.gov/app/plugins/advanced-custom-fields/core/api.php
2. Intercept the request in burp and see the response header values with system username information



Suggested fix
This issue lies in the s3cmd repository: https://github.com/s3tools/s3cmd/issues/67
where suggested fix is adding the -- no-preserve command.

## Impact

The attacker can gain sensitive information about system username. In this case it was root, so i marked impact as Low. Still, the developers can have a good reason to not expose this information in the response header.

</details>

---
*Analysed by Claude on 2026-05-24*
