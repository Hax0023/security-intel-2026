# No Password Length Restriction leads to Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 223854 | https://hackerone.com/reports/223854
- **Submitted:** 2017-04-25
- **Reporter:** ant_pyne
- **Program:** Weblate
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Denial of Service, Resource Exhaustion, Input Validation Bypass
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Weblate registration page lacks password length restrictions, allowing attackers to submit extremely large passwords that cause excessive server resource consumption during hashing operations, resulting in 500 Internal Server Errors. This design flaw can be exploited to perform denial of service attacks by repeatedly submitting oversized password payloads. The vulnerability could be mitigated by implementing standard password length limits (typically 72-128 characters) similar to industry practices.

## Attack scenario
1. Attacker identifies the password registration endpoint at https://demo.weblate.org/accounts/password
2. Attacker crafts a registration request with an extremely large password payload (megabytes in size)
3. Server attempts to hash the massive password using bcrypt/similar algorithms, consuming significant CPU and memory resources
4. Hash operation times out or exhausts server resources, returning 500 Internal Server Error
5. Attacker repeats this with multiple concurrent requests to amplify resource exhaustion
6. Legitimate users cannot register or access password reset functionality due to server unavailability

## Root cause
The application fails to implement input validation for password length on the registration endpoint. Without an enforced maximum length limit, the server attempts to process arbitrarily large passwords through resource-intensive cryptographic hashing algorithms without protection mechanisms or rate limiting.

## Attacker mindset
An attacker recognizes that password hashing is computationally expensive and exploits the absence of length restrictions to trigger algorithmic complexity denial of service. The attack requires minimal effort—just sending a single large payload—making it an attractive low-effort DoS vector. The attacker may aim to disrupt service availability during critical business periods or as part of a larger attack campaign.

## Defensive takeaways
- Implement strict maximum password length limits (recommended 128 characters, minimum 72 for bcrypt compatibility)
- Enforce both client-side and server-side password validation rules consistently
- Add rate limiting and account lockout mechanisms to registration endpoints
- Set timeouts on cryptographic operations to prevent indefinite resource consumption
- Monitor for repeated failed registration attempts from single IP addresses
- Implement resource quotas and circuit breakers for CPU-intensive operations
- Use modern password hashing algorithms with built-in length handling (e.g., bcrypt's 72-byte limit)
- Log and alert on suspicious registration patterns indicating DoS attempts

## Variant hunting
Check if other authentication endpoints (password reset, change password) have the same vulnerability
Test for similar input validation bypasses in other user-submitted fields (username, email)
Verify if rate limiting exists on registration attempts to mitigate bulk submissions
Examine if the vulnerability affects other Weblate instances or self-hosted deployments
Test POST/PUT endpoints that accept file uploads without size restrictions
Check API endpoints for similar password handling issues
Test if specially crafted character encodings (UTF-8 multi-byte) bypass length checks

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
The vulnerability demonstrates a common OWASP A04:2021 (Insecure Design) issue. While the bounty amount is not disclosed in the report, this is a legitimate DoS vector. The reporter provided clear reproduction steps. Weblate likely patched this by adding maximum length validation (commonly 128 or 256 characters). The fix is straightforward but the impact is significant as registration/authentication endpoints are critical infrastructure. This highlights the importance of secure defaults in password field handling across frameworks.

## Full report
<details><summary>Expand</summary>

Hi Weblate,

I am trying to register for an account when I came across a page where the password was required to be set up. The url is https://demo.weblate.org/accounts/password where the password was to be created after one provides his or her initial details.

There is no limit to the length of the password that can be created for this site. Hence, I tried with a big payload and everytime server responded me with a 500 internal server error. But when I registered with Antara007! password, it was accepted gleefully. Password length is something that might sound quite insignificant but is quite important.

You need to decrease password length :There are two reasons for limiting the password size. For one, hashing a large amount of data can cause significant resource consumption on behalf of the server and would be an easy target for Denial Of Service attack.

Normally all sites have a password minimum to maximum length like 72 characters limit or 48 limit to prevent Denial Of Service attack. in my sql but in weblate registration page there are no limitation. Let me know if you need any more details.

I am attaching some screenshots so that it can be understood properly.

Thanks,
Dipmalya Pyne.

</details>

---
*Analysed by Claude on 2026-05-24*
