# Full Path Disclosure on OONI Explorer

## Metadata
- **Source:** HackerOne
- **Report:** 269426 | https://hackerone.com/reports/269426
- **Submitted:** 2017-09-19
- **Reporter:** yox
- **Program:** Tor Project
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Full Path Disclosure, CWE-209
- **CVEs:** None
- **Category:** uncategorised

## Summary
The OONI Explorer endpoint at explorer.ooni.torproject.org leaks full server file paths in 404 error responses when accessing non-existent resources. This information disclosure could aid attackers in reconnaissance and facilitate chaining with other vulnerabilities like path traversal.

## Attack scenario
1. Attacker sends requests to various non-existent paths on explorer.ooni.torproject.org (e.g., //x, /invalid)
2. Server returns 404 error pages containing full filesystem paths and internal directory structure
3. Attacker analyzes disclosed paths to understand server architecture and technology stack
4. Attacker uses path information to identify potential path traversal entry points or local file inclusion vectors
5. Attacker chains full path disclosure with path traversal vulnerability to access sensitive files
6. Attacker gains access to configuration files, source code, or other sensitive system information

## Root cause
Error handling and exception messages display verbose debugging information including full file paths instead of generic user-friendly error pages. The application lacks proper error handling configuration to suppress sensitive details in production environments.

## Attacker mindset
Reconnaissance and information gathering phase. An attacker maps the application architecture and internal file structure to identify weaknesses for subsequent exploitation. Full path disclosure significantly reduces the reconnaissance effort needed before attempting more sophisticated attacks.

## Defensive takeaways
- Implement custom error pages for 4xx and 5xx responses that do not leak system paths or internal details
- Configure application logging to capture full error details locally while displaying generic messages to users
- Disable stack traces, file paths, and debugging information in production environments
- Implement input validation and sanitization to prevent malformed requests from triggering verbose errors
- Use centralized error handling with proper separation between user-facing messages and internal logging
- Regularly audit error responses and exception handling across all endpoints

## Variant hunting
Search for similar information disclosure on other Tor Project subdomains and services. Test for path traversal vulnerabilities on endpoints that accept file paths. Check for verbose error messages on other web applications in the infrastructure. Look for directory listing enabled on web servers.

## MITRE ATT&CK
- T1592
- T1589
- T1598

## Notes
Low severity due to limited immediate impact, but significant value as a reconnaissance tool. This is a classic information disclosure vulnerability that serves as a stepping stone for more sophisticated attacks. The vulnerability affects the OONI Explorer application hosted by the Tor Project, not the Tor browser or core network infrastructure itself.

## Full report
<details><summary>Expand</summary>

Hi there,

While you are primarily interested in the network/browser issues, I would like to report a web bug I discovered and thought the best place to do that would be here.

# Vulnerability

Type: Full Path Disclosure [CWE-209]
Affected endpoint: https://explorer.ooni.torproject.org
Example: https://explorer.ooni.torproject.org//x

# Details
Vulnerability details as follows.

## Impact
This security vulnerability could potentially allow a malicious hacker to map an attack against internal systems. For example, if this were to be chained with another vulnerability such as path traversal; it may lead to compromise of internal systems.

## Mitigation
Typically these sort of errors occur from incorrect data types, in this case it seems like it is just a simple 404 page which is however leaking too much information to the user. 

A best practice method is to log these type of errors to a local text file, while showing the user a friendly 404 message. This is often achieved by disabling error reporting on the application side.

</details>

---
*Analysed by Claude on 2026-05-24*
