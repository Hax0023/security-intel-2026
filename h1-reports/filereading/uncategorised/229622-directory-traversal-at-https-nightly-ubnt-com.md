# Directory Traversal at nightly.ubnt.com

## Metadata
- **Source:** HackerOne
- **Report:** 229622 | https://hackerone.com/reports/229622
- **Submitted:** 2017-05-18
- **Reporter:** grampae
- **Program:** Ubiquiti
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Arbitrary File Read
- **CVEs:** None
- **Category:** uncategorised

## Summary
A directory traversal vulnerability existed on nightly.ubnt.com that allowed unauthenticated attackers to read arbitrary files from the server filesystem, including sensitive system files like /etc/passwd and /etc/hosts. The vulnerability was discoverable through HTTP request manipulation tools and resulted in exposure of sensitive system configuration data.

## Attack scenario
1. Attacker identifies nightly.ubnt.com as a potential target during reconnaissance
2. Attacker uses automated HTTP testing tools (Acunetix, IronWasp) to probe for common vulnerabilities
3. Attacker crafts HTTP requests with path traversal sequences (e.g., ../ or encoded variants) in URL parameters
4. Server fails to properly sanitize or validate file path inputs
5. Attacker successfully retrieves sensitive files like /etc/passwd containing user account information
6. Attacker leverages disclosed system information for further attacks or privilege escalation

## Root cause
Insufficient input validation and path normalization in the application's file serving mechanism. The Express-based backend (evident from X-Powered-By header) did not properly restrict file access to intended directories or sanitize user-supplied paths before constructing filesystem paths.

## Attacker mindset
An attacker would recognize that nightly/staging builds often have reduced security controls compared to production. They would systematically test for path traversal using standard payloads, recognizing that file disclosure vulnerabilities provide reconnaissance data and potential credentials for lateral movement.

## Defensive takeaways
- Implement strict input validation and whitelist allowed file paths rather than blacklisting traversal sequences
- Use canonicalization to resolve all path references before validation to prevent bypass attempts
- Enforce filesystem access controls at the application level with a base directory restriction
- Never serve system files through web-accessible endpoints; separate static content storage from system directories
- Apply principle of least privilege - run web service with minimal filesystem permissions
- Implement security headers to restrict content delivery and add WAF rules for path traversal patterns
- Conduct regular security testing on non-production environments which often have weaker controls
- Use security scanning tools as part of CI/CD pipeline, not just as post-deployment verification

## Variant hunting
Search for similar patterns on other Ubiquiti subdomains (*.ubnt.com, *.ui.com), test staging/nightly builds of other vendors for directory traversal, examine other Node.js/Express applications for insufficient path normalization, test for traversal in API endpoints returning file content, check for Unicode or double-encoding bypasses

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1552

## Notes
Researcher noted difficulty reproducing via standard browsers, suggesting the vulnerability may have required specific HTTP manipulation tools or custom headers. The Content-Type application/octet-stream indicates successful file retrieval. Express.js default configurations often lack built-in path traversal protections, making this a common class of vulnerability in Node.js applications. Staging/nightly environments are frequently overlooked in security hardening practices.

## Full report
<details><summary>Expand</summary>

From within the http request function of the Acunetix and IronWasp programs I was able to view the passwd and hosts files at https://nightly.ubnt.com.  

Please see the attached screenshots for proof.

I have tried to reproduce from within firefox and internet explorer without much luck however if you need it I will try to come up with a work around.

For reference the response header is as follows:
HTTP/1.1 200 OK
Date: Thu, 18 May 2017 13:35:08 GMT
Content-Type: application/octet-stream
Content-Length: 1339
Connection: keep-alive
X-Powered-By: Express
Strict-Transport-Security: max-age=15552000; includeSubDomains
Last-Modified: Wed, 25 May 2016 20:30:37 GMT



</details>

---
*Analysed by Claude on 2026-05-24*
