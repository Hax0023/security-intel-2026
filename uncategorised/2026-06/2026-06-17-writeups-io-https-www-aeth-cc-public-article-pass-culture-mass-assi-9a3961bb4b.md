# Privileged Account Creation via Mass Assignment to Full Compromise using Stored XSS

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** pass Culture Bug Bounty (YesWeHack, invitation-only)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Mass Assignment, Stored XSS, Privilege Escalation, Insecure Direct Object References
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for account creation was vulnerable to mass assignment, allowing attackers to inject arbitrary user roles including the JOUVE privileged role that was not explicitly removed. This granted elevated permissions which could then be leveraged to inject stored XSS payloads affecting administrator accounts.

## Attack scenario (step by step)
1. Attacker identifies deprecated /users/signup/webapp endpoint designed for beneficiary account creation
2. Attacker sends POST request with custom JSON payload containing JOUVE role in roles array
3. Application creates User object from request.json via mass assignment, only explicitly removing ADMIN and BENEFICIARY roles
4. JOUVE role persists unfiltered into database, granting attacker elevated privileges
5. Attacker uses JOUVE account to access admin panel and inject stored XSS payload
6. Administrator views page with XSS payload, compromising their account and enabling full application compromise

## Root cause
The endpoint implemented insecure mass assignment by directly instantiating a User database model from untrusted user input, then using a blacklist approach to remove sensitive attributes. Since only ADMIN and BENEFICIARY roles were explicitly removed, the JOUVE role (a legacy administrative role) persisted undetected, bypassing privilege restrictions.

## Attacker mindset
An attacker conducting comprehensive API reconnaissance discovered a deprecated endpoint still active in production. Recognizing the code's flawed blacklist approach to role removal, the attacker identified an overlooked role (JOUVE) that granted administrative access. This enabled privilege escalation combined with stored XSS for lateral movement to administrator accounts.

## Defensive takeaways
- Use whitelist-based validation instead of blacklist when filtering sensitive attributes; explicitly define allowed fields for user input
- Avoid instantiating security-sensitive database objects directly from user input; use data transfer objects or explicit field mapping
- Implement a single, unified role/permission system rather than dual mechanisms (isAdmin boolean + roles array)
- Remove deprecated code paths from production or maintain strict feature flags with security controls
- Enforce database constraints at the schema level to prevent invalid role combinations
- Regular security audits of all API endpoints including deprecated/internal ones
- Implement comprehensive input validation and sanitization for all user-supplied data fields
- Use parameterized queries and prepared statements to prevent injection attacks

## Variant hunting
Search codebase for: (1) Other endpoints using from_dict() pattern on sensitive models, (2) Incomplete role removal logic in other account creation flows, (3) Deprecated endpoints still accessible in production, (4) Dual authorization mechanisms (boolean flags + enums), (5) TODO comments indicating incomplete security implementations, (6) Other legacy role enums that may bypass removal functions

## MITRE ATT&CK
- T1190
- T1199
- T1021
- T1078
- T1548
- T1598

## Notes
The vulnerability chain demonstrates how two distinct flaws (mass assignment + incomplete role filtering) combine for severe impact. The JOUVE role appears to be a legacy authentication mechanism with TODO comments indicating known technical debt. The writeup emphasizes proper disclosure practices and legal bug bounty context. This is a well-documented example of why deprecated code must be actively removed rather than left dormant.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
