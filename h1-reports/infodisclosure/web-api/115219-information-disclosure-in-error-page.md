# Information Disclosure via Unhandled URL Encoding Error Page

## Metadata
- **Source:** HackerOne
- **Report:** 115219 | https://hackerone.com/reports/115219
- **Submitted:** 2016-02-07
- **Reporter:** thsa
- **Program:** Paragon Initiative Enterprises (paragonie.com)
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Server Fingerprinting, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
The application fails to handle malformed URL-encoded characters (%PI) gracefully, resulting in an unhandled error page that discloses the web server type and version information. This allows attackers to perform server fingerprinting without additional reconnaissance tools.

## Attack scenario
1. Attacker crafts a URL with invalid URL encoding (e.g., %PI instead of valid hex codes like %20)
2. Request is sent to the target domain (paragonie.com)
3. The application's URL decoder processes the malformed character and fails
4. Instead of a generic error page, an unhandled exception error page is returned
5. Error page contains sensitive information such as server software and version number
6. Attacker uses this information to identify known vulnerabilities and plan further attacks

## Root cause
Missing or incomplete error handling for invalid URL-encoded characters in the request parsing layer. Custom error handlers cover most scenarios but fail to catch this specific case, falling back to a default error page that leaks server information.

## Attacker mindset
Reconnaissance-focused attacker seeking to identify the web server software and version for vulnerability research or targeted exploitation. The attacker tests edge cases in input validation to bypass custom error handling.

## Defensive takeaways
- Implement comprehensive error handling for all URL parsing and decoding operations
- Ensure ALL error pages (including framework defaults) display generic messages without server/version disclosure
- Use a Web Application Firewall (WAF) to normalize and validate URL-encoded input before processing
- Configure web server to suppress Server header and version information in HTTP responses
- Implement centralized error handling that catches exceptions at all layers
- Test error conditions systematically, including edge cases like invalid encoding sequences
- Remove or obfuscate stack traces and detailed error messages from production environments

## Variant hunting
Test other invalid URL encoding patterns: %ZZ, %GG, %1, %00
Try path traversal with bad encoding: /../../%PI
Test in different URL positions: query string, fragment, headers
Check if other special characters trigger similar unhandled errors
Attempt to bypass custom handlers with double-encoding: %25PI
Test across different endpoints to identify inconsistent error handling
Check for information disclosure in 403, 404, and 500 error pages

## MITRE ATT&CK
- T1190
- T1592.004
- T1598.004

## Notes
This is a low-severity issue but represents a common security anti-pattern. While server fingerprinting alone doesn't enable direct exploitation, it significantly reduces the attacker's work factor for identifying suitable exploits. The vulnerability demonstrates the importance of defense-in-depth error handling. Organizations should treat information disclosure seriously even when severity seems minimal, as it often chains with other vulnerabilities.

## Full report
<details><summary>Expand</summary>

Hello,

Here's an crafted URL which discloses web server used and version of same. 
> https://paragonie.com/%PI  

Even-though most error pages are handled by generic pages in paragonie.com, above given ```400 Bad Request``` sample is not handled. 
It seems this error page is because of Invalid URL Encoded (%PI) Value given in the request. 

</details>

---
*Analysed by Claude on 2026-05-24*
