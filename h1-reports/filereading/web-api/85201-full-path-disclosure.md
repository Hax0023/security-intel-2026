# Full Path Disclosure in OwnCloud Files TextEditor

## Metadata
- **Source:** HackerOne
- **Report:** 85201 | https://hackerone.com/reports/85201
- **Submitted:** 2015-08-27
- **Reporter:** ishahriyar
- **Program:** OwnCloud
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Full Path Disclosure, Error-based Path Leakage
- **CVEs:** CVE-2016-1501
- **Category:** web-api

## Summary
The files_texteditor AJAX endpoint leaks the full server file path when attempting to load non-existent files. An attacker can enumerate the complete directory structure and discover the application's installation path by triggering error conditions through the loadfile endpoint.

## Attack scenario
1. Attacker accesses the OwnCloud instance and identifies the files_texteditor app is enabled
2. Attacker sends GET request to /apps/files_texteditor/ajax/loadfile with non-existent filename parameter
3. Server returns 400 error with JSON response containing full filesystem path
4. Attacker discovers installation location: /opt/lampp/htdocs/owncloud/data/admin/files/
5. Attacker can now map directory structure and identify sensitive paths for further exploitation
6. Information gathered can be used to chain with other vulnerabilities or conduct reconnaissance

## Root cause
Error handling in the loadfile AJAX endpoint does not sanitize or redact filesystem paths from error messages returned to the client. The application exposes internal path information directly in JSON error responses instead of generic error messages.

## Attacker mindset
An attacker gathering reconnaissance on the target system would probe various endpoints for information leakage. By testing with invalid parameters, they can map the application structure and determine installation paths, which aids in vulnerability assessment and planning further attacks.

## Defensive takeaways
- Implement generic error messages for client-facing APIs that do not expose filesystem paths
- Sanitize all error output in JSON responses before returning to client
- Use logging for detailed error information server-side only; return minimal details to users
- Implement proper exception handling that separates internal exceptions from user-facing messages
- Consider implementing path obfuscation or relative paths in error messages
- Apply input validation to prevent file access to non-existent files before error generation

## Variant hunting
Look for similar path disclosure vulnerabilities in: other AJAX endpoints handling file operations (upload, download, delete), API endpoints with file access logic, backup/recovery functions, and any location where file operations generate errors with path information in responses.

## MITRE ATT&CK
- T1526
- T1087
- T1592

## Notes
This is a low-severity information disclosure issue. While it doesn't directly compromise the system, it provides reconnaissance data that attackers can use in multi-stage attacks. The vulnerability was reported on HackerOne in 2015 against OwnCloud. Path disclosure vulnerabilities are often chained with other issues to maximize impact. The error occurs in a file locking mechanism, suggesting the application is attempting to acquire locks on files that don't exist before proper validation.

## Full report
<details><summary>Expand</summary>

When I was trying to load a file which is not actually exist then it shows 
{"message":"Could not obtain lock type 1 on \"\/opt\/lampp\/htdocs\/owncloud\/data\/admin\/files\/lol\"."}


Request 

GET /owncloud/index.php/apps/files_texteditor/ajax/loadfile?filename=lol HTTP/1.1
Host: 192.168.0.105
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
requesttoken: JsTZTCWPxW2INuw7Ur1bgkLlmwQY0a
OCS-APIREQUEST: true
X-Requested-With: XMLHttpRequest
Referer: http://192.168.0.105/owncloud/index.php/apps/files/
Cookie: ochwk513zixt=am12pvu6bbmi3u03jbbk64v5f2
Connection: keep-alive

Response 

HTTP/1.1 400 Bad request
Date: Thu, 27 Aug 2015 14:07:54 GMT
Server: Apache/2.4.16 (Unix) OpenSSL/1.0.1p PHP/5.6.11 mod_perl/2.0.8-dev Perl/v5.16.3
X-Powered-By: PHP/5.6.11
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-cache, must-revalidate
Pragma: no-cache
Content-Security-Policy: default-src 'none';script-src 'self' 'unsafe-eval';style-src 'self' 'unsafe-inline';img-src 'self';font-src 'self';connect-src 'self';media-src 'self'
Content-Length: 106
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
X-Robots-Tag: none
X-Frame-Options: SAMEORIGIN
Connection: close
Content-Type: application/json; charset=utf-8

{"message":"Could not obtain lock type 1 on \"\/opt\/lampp\/htdocs\/owncloud\/data\/admin\/files\/lol\"."}




Thanks.


</details>

---
*Analysed by Claude on 2026-05-24*
