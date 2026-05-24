# Full Path Disclosure on CSRF Validation Failure in Airship

## Metadata
- **Source:** HackerOne
- **Report:** 148890 | https://hackerone.com/reports/148890
- **Submitted:** 2016-07-02
- **Reporter:** abdullah
- **Program:** Airship
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
When CSRF token validation fails in Airship, the application discloses full file paths and system information in error responses. This information leakage can help attackers map the application structure and identify potential attack vectors. The vulnerability exists in the error handling mechanism that processes failed CSRF validation requests.

## Attack scenario
1. Attacker identifies a form or endpoint that performs CSRF validation
2. Attacker crafts a request with a missing or invalid CSRF token to trigger validation failure
3. Application returns error response containing full file paths and directory structure
4. Attacker analyzes exposed paths to understand application architecture and framework
5. Attacker uses path information to identify vulnerable scripts and components
6. Attacker leverages this intelligence to plan targeted attacks against specific endpoints

## Root cause
The application's error handling for failed CSRF validation displays verbose error messages containing full file paths instead of generic user-friendly error messages. Likely caused by exception handling that directly outputs stack traces or file paths without sanitization or wrapping in generic error responses.

## Attacker mindset
An attacker would view this as reconnaissance opportunity - full path disclosure significantly reduces the reconnaissance effort needed. It reveals the exact location of vulnerable components, helping to plan more targeted attacks. This is particularly valuable when combined with other vulnerabilities.

## Defensive takeaways
- Implement generic error messages for security-related failures (CSRF, auth, etc.) that do not disclose system paths
- Never display full file paths, stack traces, or system information in user-facing error responses
- Log detailed error information server-side only, separate from client responses
- Configure error handling to distinguish between development and production environments
- Sanitize all error messages before returning to clients
- Implement proper exception handling that catches and wraps exceptions in generic responses
- Disable debug modes and verbose error reporting in production

## Variant hunting
Check other authentication/security failure points (JWT validation, API key validation, rate limiting) for similar path disclosure
Test file upload endpoints with invalid tokens to see if paths are disclosed
Try requests to protected endpoints without proper headers to trigger validation errors
Examine error pages for other information disclosure vectors (version numbers, framework details)
Test API endpoints with invalid CSRF tokens to see if structured responses leak paths

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1518 - Gather System Network Configuration
- T1217 - Browser Bookmark Discovery

## Notes
This is a relatively low-severity issue but can be chained with other vulnerabilities. The disclosure of paths makes targeted attacks easier and significantly improves reconnaissance capabilities. The PoC shows a valid HTTP request with missing CSRF token that triggers the vulnerability. The issue specifically affects the author edit endpoint but likely exists across other CSRF-protected endpoints in Airship. The vulnerability requires no authentication in the scenario presented, making it more severe from a reconnaissance perspective.

## Full report
<details><summary>Expand</summary>

Hi again , 

There are Full path disclosure  in airship when the CSRF validation failed . It will show the full path with files  this is can be useful for an attacker if he need some information about files and path ,identified the script and path . 

 PoC : 

Host: bridge.cspr.ng
User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://bridge.cspr.ng/author/edit/7
Cookie: __cfduid=any; PHPSESSID=any; cf_clearance=any-any-any
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 199
If-Modified-Since: *


_CSRF_TOKEN=&name=%3Cxss%3E&byline=&format=Rich+Text&biography=%3Ch2%3Exxxxxx%3Cbr%3E%3C%2Fh2%3E&_wysihtml5_mode=1&save_btn=sav




{F102987}



The CSRF validation error should not show other info about the files path . 

Thanks 

</details>

---
*Analysed by Claude on 2026-05-24*
