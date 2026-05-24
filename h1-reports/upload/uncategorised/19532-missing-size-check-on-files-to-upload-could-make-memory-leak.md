# Missing File Size Validation on Upload Functionality Leading to DoS and Memory Exhaustion

## Metadata
- **Source:** HackerOne
- **Report:** 19532 | https://hackerone.com/reports/19532
- **Submitted:** 2014-07-09
- **Reporter:** eth3real
- **Program:** Uzbey
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Improper Input Validation, Missing Resource Limits, Denial of Service, Memory Exhaustion
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application lacks file size validation on the upload picture functionality, allowing attackers to upload arbitrarily large files (tested with 2.52 GB). This causes severe memory exhaustion, connection slowdown, and potential DoS conditions without any 413 or similar error responses.

## Attack scenario
1. Attacker identifies the upload picture feature on staging.uzbey.com
2. Attacker crafts or prepares an extremely large file (multi-gigabyte)
3. Attacker initiates upload without encountering size validation or warnings
4. Server begins processing the oversized file, consuming heap memory
5. Memory exhaustion occurs, causing application slowdown and connection failures
6. Legitimate users experience service degradation or complete unavailability

## Root cause
Application developers failed to implement server-side file size validation before accepting and processing uploaded files. No maximum file size limits were configured, and no HTTP 413 (Payload Too Large) or similar error handling was implemented.

## Attacker mindset
Resource exhaustion through automation: an attacker could weaponize this into a low-effort DoS tool by scripting repeated large file uploads, bypassing traditional rate-limiting since the vulnerability exists at the validation layer rather than request rate.

## Defensive takeaways
- Implement strict file size limits at multiple layers: client-side for UX, server-side validation before file acceptance
- Return appropriate HTTP 413 (Payload Too Large) errors when size limits are exceeded
- Configure web server and framework upload limits (e.g., nginx client_max_body_size, Apache LimitRequestBody)
- Set memory limits per request/upload process to prevent unbounded consumption
- Implement streaming/chunked upload processing instead of loading entire file into memory
- Add request timeout limits to abort excessively long operations
- Monitor and alert on unusual upload patterns or resource consumption spikes
- Validate file sizes against whitelist of permitted sizes for specific use cases

## Variant hunting
Check other file upload endpoints (profile pictures, documents, attachments) for same validation gaps
Test image resize/thumbnail generation endpoints for similar memory issues
Investigate backup/export functionality that might read and transmit large files
Examine any form submission endpoints accepting binary data
Probe for XXE, zip bomb, or recursive archive handling vulnerabilities in upload processing
Test HTTP range requests on uploaded files to identify partial consumption bypasses

## MITRE ATT&CK
- T1190
- T1499.1
- T1499.4
- T1565.2

## Notes
This is a foundational resource exhaustion vulnerability. The researcher demonstrated impact through direct testing. Severity could escalate to Critical if combined with automated attack tooling or if the staging environment mirrors production infrastructure. The lack of any validation response (no 413 error) suggests the issue exists in application logic rather than web server configuration, making it more difficult to mitigate through infrastructure-only changes.

## Full report
<details><summary>Expand</summary>

I noticed that there isn't any "size check" when someone tries to upload a flie through the "upload picture" option, this could generate a memory leak or also a kind of DoS and is deangerous with bigger and bigger files. So i first tried to upload a file of about 2,52 GB (see the pic) and no warning messaege about the size wasn't displayed (such as a 413 error message), and the site was unable to charge the page, it generated an huge solwdown of the connection to https://staging.uzbey.com. 

------Risks------

Someone interested could exploit that to make a designed wepay dosser software to take the website down and that colud also make a dangerous memory leak or exploitable overflows .

</details>

---
*Analysed by Claude on 2026-05-24*
