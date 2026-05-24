# Full Path Disclosure via CSS Rendering Error

## Metadata
- **Source:** HackerOne
- **Report:** 9137 | https://hackerone.com/reports/9137
- **Submitted:** 2014-04-22
- **Reporter:** mohamed_fouad
- **Program:** Respond.ly
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal, Full Path Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The application discloses full server file paths in error messages when CSS stylesheet rendering fails. An attacker can craft requests to non-existent CSS files and observe detailed file system paths including application directory structure, release version numbers, and absolute paths. This information can facilitate further reconnaissance for additional vulnerabilities.

## Attack scenario
1. Attacker sends GET request to /css/shared/ endpoint with crafted parameters containing special characters
2. Application attempts to render CSS stylesheet from the provided path
3. File is not found, triggering a 500 Internal Server Error
4. Error handler returns detailed JSON response containing full file system path: /srv/www/respondly/releases/20140421220734/marketing_bundle/programs/server/assets/packages/app/shared/css/
5. Attacker maps out directory structure and identifies application root, release versions, and internal path organization
6. Attacker uses disclosed paths to identify other potential attack vectors or sensitive file locations

## Root cause
Error messages are not sanitized before being sent to clients. The application returns raw filesystem error details including full absolute paths in JSON error responses instead of generic error messages.

## Attacker mindset
Information gathering and reconnaissance. The attacker is mapping the application's internal structure to identify potential weaknesses, version numbers, and file locations that could be leveraged in subsequent attacks.

## Defensive takeaways
- Implement generic error messages for client-facing responses, logging detailed errors server-side only
- Sanitize all error output to remove absolute file paths, system information, and software versions
- Configure centralized error handling that never exposes internal paths or infrastructure details
- Use relative paths or abstract identifiers in error messages
- Implement input validation on CSS file requests to prevent traversal attempts
- Set appropriate error response codes and messages in production environments

## Variant hunting
Search for other endpoints that render resources (images, scripts, fonts) and trigger similar error conditions. Test API endpoints that return file metadata or operation results. Look for error handlers in file upload, export, or template rendering features.

## MITRE ATT&CK
- T1526
- T1592
- T1518

## Notes
The vulnerability combines path traversal input with information disclosure. The special characters in the request (%22ns=%22alert(9)) suggest the attacker may also be testing for injection vulnerabilities. While the bounty amount is not specified in the report, full path disclosure is typically low severity but valuable for reconnaissance phases of more complex attacks.

## Full report
<details><summary>Expand</summary>

{"code":500,"error":"Failed to render CSS stylesheet.","file":"/assets/packages/app/shared/css/","message":"ENOENT, open '/srv/www/respondly/releases/20140421220734/marketing_bundle/programs/server/assets/packages/app/shared/css/"}

Request
------------
GET /css/shared/%22ns=%22alert(9) HTTP/1.1
Cache-Control: no-cache
Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
User-Agent: Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0;)
Accept-Language: en-us,en;q=0.5
Host: respond.ly
Accept-Encoding: gzip, deflate

Response
--------------
HTTP/1.1 500 Internal Server Error
Connection: keep-alive
Date: Tue, 22 Apr 2014 16:36:00 GMT
Transfer-Encoding: chunked
Server: nginx
Vary: Accept-Encoding
X-Frame-Options: DENY
Content-Type: application/json

{"code":500,"error":"Failed to render CSS stylesheet.","file":"/assets/packages/app/shared/css/","message":"ENOENT, open '/srv/www/respondly/releases/20140421220734/marketing_bundle/programs/server/assets/packages/app/shared/css/"}



</details>

---
*Analysed by Claude on 2026-05-24*
