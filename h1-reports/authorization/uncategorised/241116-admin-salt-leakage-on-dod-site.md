# Admin Salt Leakage via Exposed ColdFusion Method

## Metadata
- **Source:** HackerOne
- **Report:** 241116 | https://hackerone.com/reports/241116
- **Submitted:** 2017-06-18
- **Reporter:** mr_r3boot
- **Program:** DoD Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Information Disclosure, Improper Access Control, Cryptographic Weakness, Authentication Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An exposed ColdFusion component method (getSalt) on the DoD administrative login page publicly discloses the administrator authentication salt without any access controls. This enables attackers to perform offline password cracking attacks against admin credentials using the leaked salt and standard hash-cracking tools.

## Attack scenario
1. Attacker discovers the administrative login endpoint at /adminapi/administrator.cfc
2. Attacker enumerates ColdFusion methods by appending ?method=getSalt to the URL
3. Attacker retrieves the admin salt value in plaintext from the response
4. Attacker uses the leaked salt with common hash-cracking tools (hashcat, John the Ripper) to perform offline dictionary/brute-force attacks
5. Attacker cracks admin password offline without rate limiting or account lockout protections
6. Attacker gains unauthorized administrative access to the DoD system

## Root cause
The ColdFusion component fails to implement proper access controls on the getSalt method, exposing a sensitive cryptographic material (salt) that should only be available during authenticated sessions or not exposed at all. The method is publicly callable without authentication verification.

## Attacker mindset
Reconnaissance-focused attacker looking for low-hanging fruit in authentication mechanisms. The exposure of salt dramatically reduces the computational cost of password cracking, making admin compromise a feasible attack path. The attacker likely used automated enumeration techniques to discover the exposed method.

## Defensive takeaways
- Implement strict access controls on all ColdFusion methods; default-deny unauthenticated access
- Never expose cryptographic materials (salts, keys) through public endpoints
- Use security annotations/filters to explicitly mark methods as private or requiring authentication
- Consider moving away from client-side salt requirements; use server-side password hashing only
- Implement rate limiting and account lockout on login endpoints to mitigate offline cracking
- Conduct security code review of ColdFusion components, especially in administrative interfaces
- Use Web Application Firewalls to restrict access to sensitive administrative paths
- Implement comprehensive input validation and method access whitelisting

## Variant hunting
Search for other exposed ColdFusion methods in /adminapi/ or /admin/ paths (getPassword, getHash, validateCredentials, etc.)
Test other ColdFusion components for similar information disclosure patterns
Enumerate common ColdFusion method names (login, authenticate, verify, getSalt, getUser) across the application
Check for other endpoints exposing authentication-related data (user enumeration, password reset tokens)
Test for similar salt/credential leakage in API endpoints or mobile application backends

## MITRE ATT&CK
- T1190
- T1526
- T1589
- T1110
- T1078

## Notes
This is a critical finding on a DoD system demonstrating inadequate security controls on authentication mechanisms. The report lacks specific metrics (complexity of password, salt length, hashing algorithm used) which could determine actual exploitation difficulty. ColdFusion is particularly vulnerable to method enumeration attacks when security controls are not explicitly configured. The fix recommendation is overly simplistic - proper implementation requires removing the salt exposure entirely or implementing framework-level access controls.

## Full report
<details><summary>Expand</summary>

Hi there, the login page located at https://█████████/████████/adminapi/administrator.cfc is leaking administrator salt which is required at authentication purpose.

#PoC:
Navigate to `https://████/████████/adminapi/administrator.cfc?method=getSalt` which will show you the admin salt  `████████` which is required for further authentication.

#Impact:
With help of salt and some other info an attacker easily bypass login by using simple hash cracking tools and get access to admin panel

#Fix:
Direct access to getSalt method should be prohibited.

Let me know if any further info is required.

Regards,
Mr_R3boot.


</details>

---
*Analysed by Claude on 2026-05-24*
