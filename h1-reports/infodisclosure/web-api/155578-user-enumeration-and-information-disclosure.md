# User Enumeration and Information Disclosure via Squarespace Admin Console

## Metadata
- **Source:** HackerOne
- **Report:** 155578 | https://hackerone.com/reports/155578
- **Submitted:** 2016-07-31
- **Reporter:** pl_bounty
- **Program:** Uber Movement / Squarespace
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** User Enumeration, Information Disclosure, Improper Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
The Uber Movement Squarespace admin console was vulnerable to user enumeration through the /?format=json endpoint, which exposed administrative email addresses. An attacker could enumerate valid user accounts and access configuration details via the /config endpoint without proper authentication controls.

## Attack scenario
1. Attacker discovers that the Squarespace instance supports JSON output format via /?format=json parameter
2. Attacker requests the endpoint with JSON format and receives structured data containing user information
3. Attacker accesses /config endpoint which leaks additional user details and system configuration
4. Attacker enumerates multiple administrative email addresses (admin@gmail.com, jason@jasonbarone.com)
5. Attacker uses enumerated usernames for credential stuffing, password spraying, or social engineering attacks
6. Attacker gains knowledge of admin structure to plan further targeted attacks on the Squarespace installation

## Root cause
Missing authentication/authorization checks on the /?format=json and /config endpoints, combined with failure to restrict sensitive data serialization formats. The application exposed administrative user information without verifying user permissions.

## Attacker mindset
An attacker seeking to compromise the Uber Movement platform would recognize that enumerating valid administrative accounts significantly reduces the attack surface for credential-based attacks. The JSON format endpoint likely wasn't intended for public consumption, making it an attractive low-effort reconnaissance vector.

## Defensive takeaways
- Implement proper authentication and authorization checks on all endpoints, including those serving alternative content types (JSON, XML, etc.)
- Avoid exposing sensitive user information in public-facing configuration endpoints
- Disable or restrict format parameter functionality (?format=json) unless explicitly required and properly protected
- Implement consistent access controls across all content negotiation methods
- Audit Squarespace instances for exposed /config or similar administrative endpoints
- Use security headers and rate limiting to prevent enumeration attacks
- Sanitize and filter user data in API responses based on authentication context

## Variant hunting
Test other Squarespace installations for similar /?format=json leakage patterns
Check for /?format=xml, /?format=csv, and other alternative serialization formats
Enumerate other configuration endpoints: /admin/config, /settings, /users, /.well-known/configuration
Test for user enumeration via error message differences in login endpoints
Search for exposed .json files or backup files in root directory
Test Squarespace API endpoints for unauthorized access to user lists
Check for IDOR vulnerabilities in user profile or admin account endpoints

## MITRE ATT&CK
- T1592
- T1589
- T1598
- T1087

## Notes
The vulnerability demonstrates a common Squarespace misconfiguration. The reporter provided proof of concept documentation (attached). This is a practical example of how content negotiation parameters can bypass access controls if not properly validated. The exposure of admin email addresses significantly lowers the barrier for social engineering and credential-based attacks.

## Full report
<details><summary>Expand</summary>

Vulnerability Name: User Enumeration and Information Disclosure
Description:
It was possible to enumerate users for SquareSpace admin console in uber-movement.
Please find below details of users enumerated:
1.	admin@gmail.com
2.	jason@jasonbarone.com
Information Disclosure in https://uber-movement.squarespace.com/?format=json helped me enumerate user for https://uber-movement.squarespace.com/config

Please find attach document for proof of concept.

</details>

---
*Analysed by Claude on 2026-05-24*
