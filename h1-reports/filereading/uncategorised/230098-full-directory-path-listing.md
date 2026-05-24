# Full Directory Path Listing via PHPSESSID Cookie Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 230098 | https://hackerone.com/reports/230098
- **Submitted:** 2017-05-20
- **Reporter:** test_this
- **Program:** Casper Network (bridge.cspr.ng)
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can disclose the full server directory path by manipulating the PHPSESSID cookie value with a single quote character during login. This information disclosure vulnerability exposes sensitive path information that could aid further reconnaissance attacks.

## Attack scenario
1. Attacker navigates to the login page at https://bridge.cspr.ng/login
2. Attacker enters valid credentials and initiates login request
3. Attacker intercepts the HTTP request using a proxy tool (Burp Suite, etc.)
4. Attacker modifies the PHPSESSID cookie by appending a single quote (') to the existing value
5. Attacker forwards the modified request to the server
6. Server responds with error message containing full file system path disclosure

## Root cause
Insufficient input validation on the PHPSESSID cookie parameter. When an invalid session ID is provided, the application likely generates an error message that includes the full file path, indicating poor error handling and lack of output sanitization.

## Attacker mindset
An attacker would use this technique for reconnaissance to understand the server's directory structure and potentially identify locations of configuration files, application source code, or other sensitive resources that could be targeted in subsequent attacks.

## Defensive takeaways
- Implement strict input validation for all cookie values
- Never disclose full file paths in error messages to end users
- Use generic error messages for authentication/session failures
- Implement proper exception handling that logs detailed errors server-side only
- Sanitize and validate session IDs before processing
- Use security headers and prevent information leakage through error pages

## Variant hunting
Similar path disclosure vulnerabilities may exist in other authentication endpoints, file upload handlers, or API endpoints. Test injection of special characters (quotes, null bytes, path traversal sequences) in other cookie parameters and POST data.

## MITRE ATT&CK
- T1592
- T1526
- T1087

## Notes
This is a low-severity information disclosure issue. While it exposes directory paths, it requires authentication and manual interception. The vulnerability appears to stem from PHP error messages being exposed to users. The impact is limited but could facilitate further reconnaissance for more severe attacks.

## Full report
<details><summary>Expand</summary>

STEP:
====================
1. goto https://bridge.cspr.ng/login and enter your username,password
2.  click "LogIn" and intercept the request
3.   change the value in cookie header and add '(single quote) in PHPSESSID field
      eg: PHPSESSID=kn7e21dpp2ocai2ckn1v147qev'
4.  Forward the packet and see full path is disclose
{F186342}

</details>

---
*Analysed by Claude on 2026-05-24*
