# Information Disclosure via Directory Structure Exposure through Cookie Injection

## Metadata
- **Source:** HackerOne
- **Report:** 7930 | https://hackerone.com/reports/7930
- **Submitted:** 2014-04-17
- **Reporter:** rajuraju14
- **Program:** localize.io
- **Bounty:** undisclosed
- **Severity:** medium
- **Vuln:** Information Disclosure, Path Traversal/Injection, Error-Based Information Leakage, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The application fails to properly validate the PHPSESSID cookie value, allowing attackers to inject special characters that trigger PHP errors revealing the full directory structure and server paths. By appending ']]>>' to a valid session ID, an attacker can cause the application to expose sensitive path information through error messages in the HTTP response.

## Attack scenario
1. Attacker observes typical PHPSESSID cookie format used by the application
2. Attacker crafts malicious cookie value by appending special characters ']]>>' to a valid session ID
3. Attacker sends HTTP request with modified PHPSESSID cookie to www.localize.io
4. Server-side PHP processing fails to sanitize the cookie input properly
5. PHP notices/errors are triggered and displayed in the response body
6. Full directory paths including vhost, domain, and application structure are revealed to the attacker

## Root cause
Insufficient input validation on the PHPSESSID cookie parameter. The application likely uses the cookie value in an unsafe manner (possibly in XML/templating context given the ']]>>' injection pattern) without proper escaping or validation. Error reporting is enabled in production, causing detailed error messages with full paths to be displayed to users.

## Attacker mindset
An attacker would recognize that injecting XML/parsing-termination sequences into session cookies could break application logic and trigger error conditions. The discovery that special characters cause PHP notices reveals that path information is being logged/processed insecurely, making this a valuable reconnaissance technique for mapping server structure before launching more targeted attacks.

## Defensive takeaways
- Implement strict whitelist validation for session IDs (alphanumeric only)
- Disable verbose error reporting in production environments; log errors securely server-side instead
- Sanitize and escape all user inputs including cookies before use in any context
- Use prepared statements and parameterized queries to prevent injection attacks
- Implement Content Security Policy headers to prevent information disclosure
- Never expose file paths in error messages visible to clients
- Validate cookie format and length before processing
- Consider using secure session token generation with cryptographic randomness

## Variant hunting
Test other cookie parameters with XML/parser-breaking sequences: PHPSESSID=test]]>, PHPSESSID=test<!--
Try other injection patterns: XML tags, comment sequences, encoding bypasses in all cookie values
Check if other parameters accept similar malicious input (GET/POST parameters, headers)
Attempt to trigger different types of errors by injecting syntax that breaks different contexts (SQL, template engines, etc.)
Look for similar path disclosure on other endpoints or with different HTTP methods
Test with different session states (authenticated vs. unauthenticated) to see if error handling differs

## MITRE ATT&CK
- T1090
- T1592
- T1590
- T1046

## Notes
This is a classic information disclosure vulnerability from the early 2010s era. The vulnerability chain shows poor separation of concerns: input validation failures combined with debug information leakage. The ']]>>' sequence suggests the application was processing session data in an XML context without proper parsing safety. This type of vulnerability was common before security-first development practices became standard. The 2014 report date indicates this was submitted years after the vulnerability likely existed undetected.

## Full report
<details><summary>Expand</summary>

The /var/www/ directory structure is exposed if you add "]]>>" to the PHPSESSID in the cookie.

Request:
GET / HTTP/1.1
Host: www.localize.io
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Referer: http://www.localize.io/
Cookie: PHPSESSID=bomb3ogic5qur05apsq25nq821]]>>

Response:
HTTP/1.1 200 OK
Date: Thu, 17 Apr 2014 21:15:53 GMT
Server: Apache
Pragma: no-cache
Expires: Mon, 24 Mar 2008 00:00:00 GMT
Cache-Control: no-cache
X-Powered-By: PleskLin
Vary: Accept-Encoding
Content-Type: text/html; charset=utf-8
Connection: close
Set-Cookie: PHPSESSID=mg5to8huhbv7bpk3q0003d5kg3; path=/; HttpOnly
Content-Length: 5819


Notice: Undefined index: HTTP_ACCEPT_ENCODING in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/classes/UI.php on line 147

Notice: Undefined index: HTTP_ACCEPT_ENCODING in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/classes/UI.php on line 147

</details>

---
*Analysed by Claude on 2026-05-24*
