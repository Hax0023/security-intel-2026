# Privileged Account Creation via Mass Assignment and Stored XSS in pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private, YesWeHack)
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln types:** Mass Assignment, Privilege Escalation, Stored Cross-Site Scripting (XSS), Broken Access Control
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated user signup endpoint was vulnerable to mass assignment attacks, allowing attackers to create accounts with privileged JOUVE role by bypassing insufficient input validation. Combined with a stored XSS vulnerability in the admin panel, this enabled full compromise of administrator accounts.

## Attack scenario (step by step)
1. Attacker discovers deprecated /users/signup/webapp endpoint that accepts raw JSON input directly mapped to User model
2. Attacker crafts POST request with JOUVE role in the roles array, bypassing only ADMIN and BENEFICIARY role removal
3. Application creates user with JOUVE privilege role due to incomplete role filtering logic
4. Attacker logs in with privileged JOUVE account and accesses restricted functionality
5. Attacker injects malicious XSS payload through a form field stored in database
6. When administrator views the affected data in admin panel, stored XSS executes in their browser context, compromising their session

## Root cause
The endpoint used a defensive blacklist approach (removing specific roles) rather than whitelisting allowed roles. New JOUVE role was not included in the removal logic. Additionally, the application failed to sanitize user input before storage, allowing injection of XSS payloads that execute in privileged admin contexts.

## Attacker mindset
An attacker would recognize that deprecated endpoints often have weaker security controls. By analyzing the role removal logic, they'd identify the JOUVE role as not being filtered. The combination with stored XSS creates a lateral privilege escalation path from low-privileged user to full admin compromise through social engineering or persistence.

## Defensive takeaways
- Use whitelist approach for privilege assignment: only allow specific safe roles rather than blacklisting dangerous ones
- Implement explicit role assignment separate from mass assignment; never auto-populate security-sensitive fields from user input
- Retire deprecated endpoints promptly or apply identical security controls as current endpoints
- Perform output encoding/sanitization for all user-controlled data displayed in admin panels
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Use parameterized queries and ORM security features to prevent direct object mapping vulnerabilities
- Regular security audits of role/permission mechanisms to ensure consistency across all roles

## Variant hunting
['Check for other deprecated endpoints with similar mass assignment patterns', 'Search for other roles in UserRole enum not explicitly removed in privilege functions', 'Look for other endpoints that accept role parameters and may have incomplete filtering', 'Test if isAdmin boolean field can be directly set via mass assignment (separate attack vector)', 'Scan for other stored XSS vectors in admin panels or privileged user interfaces', 'Review other account creation/modification endpoints for mass assignment vulnerabilities', 'Test privilege escalation through role array manipulation on user profile update endpoints']

## MITRE ATT&CK
- T1190
- T1548
- T1547
- T1059
- T1021
- T1566
- T1598

## Notes
This writeup demonstrates a realistic multi-stage attack chain combining two vulnerability types. The JOUVE role appears to be a legacy authentication mechanism (TODO comment suggests awareness of the technical debt). The vulnerability chain was particularly critical because it allowed privilege escalation from unprivileged user to admin compromise. The researcher's previous article also identified XSS, suggesting this application had systemic input validation issues across multiple endpoints.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
