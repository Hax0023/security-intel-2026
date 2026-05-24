# Python Installation Path Disclosure via Malformed URL Encoding

## Metadata
- **Source:** HackerOne
- **Report:** 138659 | https://hackerone.com/reports/138659
- **Submitted:** 2016-05-13
- **Reporter:** tbehroz
- **Program:** Gratipay
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Path Traversal, Error Message Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
The application exposes the full Python installation path when processing URLs with three or more percent-encoded characters in a specific format. This information disclosure occurs due to improper error handling when decoding malformed UTF-8 sequences, revealing the internal directory structure.

## Attack scenario
1. Attacker crafts a URL with three or more percent-encoded characters (e.g., /%ff/)
2. Attacker sends the malformed request to the web server
3. The server attempts to decode the URL using UTF-8 decoding
4. Invalid UTF-8 sequence triggers an unhandled exception
5. Error message is returned to the attacker containing full Python path
6. Attacker gains knowledge of server infrastructure and Python installation location

## Root cause
The application lacks proper error handling for malformed URL-encoded characters during path decoding. When the UTF-8 decoder encounters an invalid sequence (like %ff), it raises an unhandled exception that includes the full stack trace with filesystem paths.

## Attacker mindset
Reconnaissance-focused attacker seeking to map server infrastructure and understand the deployment environment. By discovering the Python path and version, the attacker can identify potential vulnerabilities specific to that Python version and deployment configuration.

## Defensive takeaways
- Implement centralized error handling that catches decoding exceptions without exposing stack traces
- Return generic error messages to clients while logging detailed errors server-side
- Validate and sanitize URL input before processing
- Disable verbose error reporting in production environments
- Use a Web Application Firewall to normalize and validate request URLs
- Implement proper logging and monitoring for decoding errors

## Variant hunting
Test other special characters and encoding schemes (double encoding, different charsets), investigate if similar path disclosure occurs in other URL components (query strings, headers), check if other framework components leak paths through error messages

## MITRE ATT&CK
- T1190
- T1592
- T1538

## Notes
This is a relatively low-severity issue as it only provides information disclosure without direct system compromise. However, it can aid in reconnaissance for more targeted attacks. The vulnerability demonstrates the importance of secure error handling in web applications. The fix is straightforward: catch encoding exceptions and return generic error responses.

## Full report
<details><summary>Expand</summary>

Hello Team,
While testing the web application I've found that if you enter the 3 or more strings including % then web application is exposing the path of Python in error.Application exposing path of Python in error when you enter the 3 or more strings including % .. if you only enter the 2 strings it will show you the 404 not found page

### POC : 
 
`https://gratipay.com/%ff/` [3 strings]  
**Request is undecodable.(/app/.heroku/python/lib/python2.7/encodings/utf_8.py:16)**

 
`https://gratipay.com/%f/` [ 2 strings] - **404 Not Found**

</details>

---
*Analysed by Claude on 2026-05-24*
