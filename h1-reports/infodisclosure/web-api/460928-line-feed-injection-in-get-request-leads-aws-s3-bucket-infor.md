# Line Feed Injection in GET Request Leads to AWS S3 Bucket Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 460928 | https://hackerone.com/reports/460928
- **Submitted:** 2018-12-12
- **Reporter:** aty
- **Program:** HackerOne (Private Program)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** HTTP Request Smuggling, Line Feed Injection (CRLF Injection), Access Control Misconfiguration, Information Disclosure, AWS S3 ACL Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
A line feed injection vulnerability in the application's GET request handler allows attackers to bypass URL filtering and directly access AWS S3 bucket operations. By appending a line feed character (%0A) to the URL path, attackers can enumerate S3 bucket contents and read arbitrary PHP files stored in the bucket, including source code from open-source libraries.

## Attack scenario
1. Attacker crafts a GET request to https://ratelimited.me/migration/%0A/ injecting a line feed character before the path traversal
2. The line feed character causes the URL parser to treat the request as accessing a different resource, bypassing application-level access controls
3. The request reaches the AWS S3 bucket directly, which has overly permissive ACLs allowing unauthenticated LIST operations
4. Attacker receives XML response containing complete bucket contents with up to 1000 object keys
5. Attacker uses marker parameter to paginate through all objects in the bucket and identifies PHP files
6. Attacker requests individual PHP files with %0a/ injection, causing the application to append .php extension and return file contents from the S3 bucket

## Root cause
The application fails to properly sanitize and validate user input containing line feed characters (LF, %0A) in URL paths before proxying requests to AWS S3. The combination of insufficient input validation, improper URL parsing, and overly permissive S3 bucket ACLs allows the injection to bypass access controls. Additionally, the S3 bucket is misconfigured with public LIST permissions and the application's file extension handling (.php appending) creates an unintended disclosure vector.

## Attacker mindset
An attacker recognizes that HTTP control characters like line feeds can manipulate request routing and access control decisions. They experiment with URL encoding schemes to bypass security controls and discover that injecting %0A creates a pathway to the underlying S3 bucket. Once bucket enumeration is possible, they systematically map the bucket contents and exploit the application's .php file handling to read arbitrary source code, all without authentication.

## Defensive takeaways
- Implement strict input validation on all URL parameters and paths, explicitly rejecting HTTP control characters (CR, LF, NULL) using allowlist-based filtering
- Sanitize URLs before proxying requests to cloud storage services; normalize and validate all path components
- Apply the principle of least privilege to AWS S3 bucket ACLs; remove public LIST permissions unless absolutely necessary and use bucket policies instead
- Implement proper authentication and authorization checks in the application layer regardless of S3 ACL configuration
- Avoid dynamic file extension appending based on user-controlled input; use explicit content-type headers and MIME type validation
- Implement request logging and monitoring to detect unusual S3 operation patterns and potential enumeration attempts
- Use AWS S3 bucket versioning and access logging to audit and track unauthorized access attempts
- Consider using S3 access points and blocking public access settings at the account level

## Variant hunting
Test with other HTTP control characters: %0D (CR), %09 (tab), %20 (space) in various URL positions to bypass filters
Attempt double encoding: %250A (encoded %0A) to evade single-pass sanitization
Try unicode encoding variants of line feed characters if UTF-8 is processed differently
Test with path traversal sequences combined with line feed injection: ../%0A/, ..\%0A\
Probe for similar issues on other application endpoints that proxy to cloud storage (GCS, Azure Blob)
Check if other HTTP methods (HEAD, OPTIONS, DELETE) are affected by the injection vulnerability
Test S3 bucket operations other than LIST: GET ?acl, GET ?cors, GET ?versioning, PUT operations
Investigate if the vulnerability exists in other request headers (Host, Referer) that might be processed as part of S3 request construction

## MITRE ATT&CK
- T1190
- T1566
- T1199
- T1526
- T1040

## Notes
The report demonstrates a sophisticated attack combining multiple security weaknesses: HTTP request smuggling via CRLF injection, cloud service misconfiguration, and improper input handling. The attacker exploited the 1000-object limitation in S3 LIST responses by using the marker parameter for pagination, showing thorough understanding of AWS S3 API behavior. The disclosure of publicly available libraries (HTMLPurifier) reduced the actual impact, but the vulnerability could expose sensitive source code if other files were stored in the bucket. The report was well-researched with clear reproduction steps and demonstrates good security research methodology.

## Full report
<details><summary>Expand</summary>

**Summary:** 
By added line feed control character to the end of url https://ratelimited.me/migration/
it is possible to list elements of bucket name "████████" , also it is possible to view source code of any php file in the bucket such as the php file with key "██████████" which is the "URIDefinition.php" from the open source HTMLPurifier , so no sensitive source code disclosure here unless this bucket directory contain sensitive .php files other than the HTMLPurifier library . 

**Description:** 
There seems to be an ACL misconfiguration with a bucket name "█████" that can be listed by issuing a GET request to https://ratelimited.me/migration/%0A/  , the response will return  XML document that list the content of this bucket , i tried to see if i can acces some of the files listed in the bucket but it seems the request append .php to any name after the  "%0A/" soo the only files i can access are php files such as the one from this link  https://ratelimited.me/migration/%0a/00f776  , it is also possible to issue some limited S3 REST requests such as https://ratelimited.me/migration/%0A/?location  which will show the AWS region of the bucket [according to aws documentation this should be only allowed to bucket owner https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETlocation.html ], also "PUT" and "POST" are not allowed so attacker can  not change the content of the bucket 

Also note that the bucket list that return from the GET request is limited to 1000 but we can view all the files using the last elements as a marker to view the next 1000 elements https://ratelimited.me/migration/%0A/?marker=02ff70.png
## Steps To Reproduce:
open the provided links in any browser 

https://ratelimited.me/migration/%0A/ 
 https://ratelimited.me/migration/%0a/00f776
https://ratelimited.me/migration/%0A/?location 
https://ratelimited.me/migration/%0A/?marker=02ff70.png

## Impact

Attacker can list the content of AWS S3 bucket list "███" and read the content of any .php file inside

</details>

---
*Analysed by Claude on 2026-05-24*
