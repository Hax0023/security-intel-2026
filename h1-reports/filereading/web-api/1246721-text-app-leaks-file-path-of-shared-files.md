# Text App File Path Disclosure via Missing README.md in Share

## Metadata
- **Source:** HackerOne
- **Report:** 1246721 | https://hackerone.com/reports/1246721
- **Submitted:** 2021-06-28
- **Reporter:** lukasreschkenc
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Error-Based Information Disclosure
- **CVEs:** CVE-2021-32734
- **Category:** web-api

## Summary
The Nextcloud Text application leaks the full file system path of shared files when requesting a share that lacks a README.md file. By sending a crafted PUT request to /apps/text/public/session/create, an attacker can trigger a 500 error that returns the complete absolute path including parent directories. This reveals sensitive directory structure information such as usernames and folder names that should not be exposed to unauthorized users.

## Attack scenario
1. Attacker obtains a valid share token for a public share (legitimate or through other means)
2. Attacker crafts a PUT request to /apps/text/public/session/create endpoint with the share token and a non-existent README.md filepath
3. Server processes the request and encounters an error condition when trying to locate the README.md file
4. Error handler returns an unfiltered exception message containing the full absolute path to the share location
5. Attacker receives response containing sensitive path information like '/lukas/files/Private/test-public/Readme.md'
6. Attacker now has knowledge of directory structure, usernames, and folder hierarchies for targeted reconnaissance

## Root cause
Insufficient input validation and error handling in the Text app's session creation endpoint. When a README.md file is not found, the error response exposes the full file path instead of returning a generic error or properly sanitizing the output before sending to the client.

## Attacker mindset
An attacker would use this information disclosure to map out the target's file structure, identify user directories, and discover folder names that could be leveraged for further attacks. This reconnaissance data helps plan targeted social engineering, identifies private folders that might contain sensitive information, and reveals the server's internal directory layout.

## Defensive takeaways
- Implement strict output filtering/sanitization for all error messages returned to clients, especially those handling file paths
- Never expose internal file paths in API responses or error messages to unauthenticated or insufficiently authenticated users
- Use generic error messages ('File not found') instead of detailed exception information for public-facing APIs
- Validate that requested file paths are within expected directories and return errors without revealing path information
- Implement proper exception handling that logs detailed errors server-side while returning minimal information to clients
- Apply principle of least privilege - verify user has permission to access share before processing file requests
- Add security headers and rate limiting to prevent enumeration attacks against share endpoints
- Conduct security code review of file handling in public share endpoints

## Variant hunting
Search for other endpoints in Nextcloud apps that handle file operations on public shares, particularly in collaborative apps (Text, Deck, Notes). Look for any endpoint accepting filePath parameters that could trigger error messages. Check if other apps have similar patterns where missing files return detailed paths. Test other file types (Readme.txt, .md variants) to see if different error handlers leak information.

## MITRE ATT&CK
- T1526 - Reconnaissance (Active Scanning - Enumerating application resources)
- T1592 - Reconnaissance (Gather victim host information - System information discovery)
- T1087 - Discovery (Account Discovery - Cloud accounts/directory structure)
- T1538 - Discovery (Cloud service discovery - Identifying share structure)

## Notes
This vulnerability requires an attacker to already have a valid share token, making it a post-authentication or post-social-engineering attack vector. The severity is Medium rather than High because it requires prior access to a share link. However, the information leaked could be valuable for targeted attacks. The vulnerability was disclosed on HackerOne report 1246721 against Nextcloud. Consider checking if this affects other Nextcloud apps with similar file handling patterns.

## Full report
<details><summary>Expand</summary>

By sending a request for a share without a README.md, the whole file path will be returned to the user:

```
PUT /apps/text/public/session/create?token=EHTs4P7kATowiMg HTTP/1.1
Host: cloud.nextcloud.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json;charset=utf-8
Content-Length: 93
Origin: https://cloud.nextcloud.com
Te: trailers
Connection: close

{"filePath":"//Readme.md","token":"EHTs4P7kATowiMg","guestName":"Bean","forceRecreate":false}
```

```
HTTP/1.1 500 Internal Server Error
Date: Mon, 28 Jun 2021 17:33:58 GMT
Server: Apache/2.4.41 (Ubuntu)
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Pragma: no-cache
Cache-Control: no-cache, no-store, must-revalidate
Content-Security-Policy: default-src 'none';base-uri 'none';manifest-src 'self';frame-ancestors 'none'
Feature-Policy: autoplay 'none';camera 'none';fullscreen 'none';geolocation 'none';microphone 'none';payment 'none'
X-Robots-Tag: none
Strict-Transport-Security: max-age=15768000; includeSubDomains; preload
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
X-Download-Options: noopen
X-Frame-Options: SAMEORIGIN
X-Permitted-Cross-Domain-Policies: none
X-XSS-Protection: 1; mode=block
Content-Length: 49
Connection: close
Content-Type: application/json; charset=utf-8

"\/lukas\/files\/Private\/test-public\/Readme.md"
```

## Impact

Disclosure of the full file path. Here shared is "test-public" but it also states "Private" which is the parent folder.

</details>

---
*Analysed by Claude on 2026-05-24*
