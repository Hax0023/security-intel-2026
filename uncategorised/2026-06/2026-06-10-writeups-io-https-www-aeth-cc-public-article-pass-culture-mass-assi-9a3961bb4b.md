# Privileged Account Creation via Mass Assignment and Stored XSS in pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private Program via YesWeHack)
- **Bounty:** Not specified in article
- **Severity:** Critical
- **Vuln types:** Mass Assignment, Privilege Escalation, Stored Cross-Site Scripting (XSS), Inadequate Input Validation
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for user account creation was vulnerable to mass assignment, allowing attackers to inject arbitrary role values (specifically the JOUVE role) that were not properly sanitized during account creation. This enabled creation of privileged accounts that, combined with a stored XSS vulnerability in the administration panel, led to full compromise of administrator accounts.

## Attack scenario (step by step)
1. Attacker discovers a deprecated /users/signup/webapp endpoint intended for beneficiary account creation
2. Attacker crafts POST request with JSON payload including arbitrary roles array containing 'JOUVE' role (not explicitly removed in code)
3. User object is instantiated directly from request.json, populating all attributes including roles before sanitization occurs
4. Application only explicitly removes ADMIN and BENEFICIARY roles, missing the JOUVE role which provides elevated privileges
5. Attacker successfully creates account with JOUVE role, gaining privileged access to administration panel
6. Attacker injects stored XSS payload through available input fields, compromising administrator accounts that view the malicious content

## Root cause
Flawed security design pattern where the application creates a database model object with all user-supplied input (mass assignment) and then attempts to remove sensitive attributes afterward. This blacklist approach failed to account for additional privilege escalation roles like JOUVE. Additionally, the coexistence of two different privilege mechanisms (isAdmin boolean and roles array) created complexity and oversight opportunities.

## Attacker mindset
Opportunistic vulnerability researcher analyzing deprecated endpoints for overlooked security controls. Recognized that blacklist-based role removal is inherently brittle and that enum-based roles not explicitly validated present bypass opportunities. Chained two vulnerabilities together for maximum impact (privilege escalation + XSS) to achieve administrator compromise.

## Defensive takeaways
- Avoid mass assignment patterns - use explicit allowlisting of permitted fields rather than blacklisting sensitive ones
- Use whitelist-based validation for privilege assignment - only permit intended roles, reject everything else
- Consolidate privilege mechanisms - maintain single source of truth for user roles/permissions, not dual isAdmin+roles
- Immediately remove deprecated endpoints or properly secure them with equal rigor as active endpoints
- Apply defense-in-depth: even with privilege escalation, implement role-based access controls at each operation
- Store XSS prevention: validate and sanitize all user inputs before storage, use output encoding in templates
- Regular code audits focusing on enum handling and permission-checking logic
- Implement comprehensive authorization checks at business logic layer, not just at endpoint entry

## Variant hunting
['Test all deprecated/legacy API endpoints for removed security checks', 'Enumerate all role/permission enum values and test each individually for blacklist bypasses', 'Check for similar mass assignment patterns in other user type creation endpoints (professional, underage beneficiary)', 'Search for other endpoints accepting role arrays or privilege-related objects as direct input', 'Test for inconsistencies between isAdmin boolean and roles array in authorization checks throughout application', 'Audit other administrative functions for stored XSS when accessed by elevated privilege accounts', 'Check if JOUVE role appears elsewhere with additional unexploited privileges']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1548: Abuse Elevation Control Mechanism
- T1598: Phishing for Information
- T1059: Command and Scripting Interpreter
- T1070: Indicator Removal

## Notes
Article was incomplete in provided excerpt but clearly demonstrates chaining vulnerabilities for maximum impact. The JOUVE role appears to be a temporary authentication mechanism (TODO comment indicates it should be removed). The writeup demonstrates excellent vulnerability research methodology by analyzing deprecated endpoints and understanding the privilege model deeply. The combination of mass assignment + insufficient blacklisting + stored XSS represents a realistic attack chain that bypassed multiple security layers.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
