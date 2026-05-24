# No Password Length Restriction leads to Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 1243009 | https://hackerone.com/reports/1243009
- **Submitted:** 2021-06-24
- **Reporter:** c_j_27
- **Program:** Hackerone (Undisclosed Program)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service, Missing Input Validation, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
The application lacks password length restrictions during account registration, allowing attackers to submit extremely long passwords that consume excessive server resources during hashing operations. An attacker could exploit this by submitting numerous requests with very long passwords to exhaust server CPU and memory, causing denial of service to legitimate users.

## Attack scenario
1. Attacker identifies registration endpoint with no password length validation
2. Attacker crafts HTTP requests with passwords exceeding typical limits (tested with ~3500+ character string)
3. Attacker sends multiple concurrent registration requests with long passwords from different IP addresses
4. Server attempts to hash extremely long password strings, consuming significant CPU cycles
5. Cumulative resource exhaustion from multiple long-password hashing operations degrades server performance
6. Legitimate users experience timeouts and service unavailability

## Root cause
Missing input validation and length constraints on password field in registration endpoint. No maximum password length enforced before password hashing algorithm processes the data.

## Attacker mindset
Resource exhaustion attacker seeking to identify computationally expensive operations that lack rate limiting or input validation to amplify impact of relatively simple requests.

## Defensive takeaways
- Implement strict password length limits (typically 8-128 characters) at both client and server validation layers
- Enforce maximum input length before cryptographic operations to prevent algorithmic complexity attacks
- Consider rate limiting on registration endpoints to throttle high-volume requests
- Implement request timeouts on password hashing operations
- Monitor CPU/memory usage on authentication services for anomalies
- Use adaptive hashing algorithms with iteration limits to prevent resource exhaustion
- Validate and sanitize all user inputs with explicit length constraints

## Variant hunting
Check other user input fields (username, email) for similar length validation gaps
Test password reset functionality for identical vulnerability
Examine login endpoints for same issue allowing long password submissions
Review API endpoints accepting user credentials for length restrictions
Test other computational operations (image processing, file uploads) for unbounded resource consumption

## MITRE ATT&CK
- T1499.4 - Denial of Service: Application/Endpoint Exhaustion
- T1190 - Exploit Public-Facing Application
- T1498 - Network Denial of Service

## Notes
This vulnerability is a precursor to DoS rather than DoS itself, requiring multiple concurrent requests to manifest as practical attack. Modern bcrypt implementations have built-in truncation at 72 bytes, partially mitigating this in systems using bcrypt. However, systems using other hashing algorithms (PBKDF2, Argon2 without limits) remain vulnerable. The reporter appropriately noted this is a design flaw enabling DoS rather than direct DoS vulnerability.

## Full report
<details><summary>Expand</summary>

Hey when I try to set the password while creating account I noticed that you haven't kept any password limit.
You need to decrease password length :There are two reasons for limiting the password size. For one, hashing a large amount of data can cause significant resource consumption on behalf of the server and would be an easy target for Denial Of Service attack.
Normally all sites have a password minimum to maximum length like 72 characters limit or 48 limit to prevent Denial Of Service attack. But in your  registration page there are no limitation. Let me know if you need any more details.

This is typically not DoS, but a vulnerability which may lead to DoS attack.

The password I tried is:

Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40Crissrock3%40

## Impact

As the response is seen, the server might not be able to handle such lengthy passwords coming from different machines simultaneously. The attacker can perform a DDOS attack by using this vulnerability.

</details>

---
*Analysed by Claude on 2026-05-24*
