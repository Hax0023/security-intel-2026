# Privileged Account Creation via Mass Assignment and Stored XSS in Pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Pass Culture Bug Bounty (Private, via YesWeHack)
- **Bounty:** Not disclosed
- **Severity:** Critical
- **Vuln types:** Mass Assignment, Privilege Escalation, Stored Cross-Site Scripting (XSS), Broken Access Control
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for user signup was vulnerable to mass assignment, allowing attackers to assign privileged roles (specifically the JOUVE role) during account creation. Combined with a stored XSS vulnerability in the administration panel, this enabled full compromise of administrator accounts and the application.

## Attack scenario (step by step)
1. Attacker discovers a deprecated /users/signup/webapp endpoint that accepts user input directly into a User model object
2. Attacker crafts a registration request including a roles array with the JOUVE privilege role, which was not explicitly removed like ADMIN and BENEFICIARY
3. Attacker successfully creates an account with JOUVE role, gaining elevated privileges beyond a standard beneficiary account
4. Attacker uses the privileged JOUVE account to inject a malicious payload into a field that gets stored in the database (likely a user profile field)
5. When an administrator views the stored payload (in the administration panel), the JavaScript executes in their browser context
6. Attacker achieves session hijacking, credential theft, or administrative action execution to fully compromise the application

## Root cause
The application used an insecure allowlist/blacklist pattern for access control: it created a User object from untrusted input and then removed only known-dangerous roles (ADMIN, BENEFICIARY) rather than whitelisting safe roles. The JOUVE role was overlooked in the removal logic. Additionally, insufficient input validation and sanitization allowed stored XSS in fields accessible to administrators.

## Attacker mindset
An attacker analyzing the source code during reconnaissance would identify the deprecated endpoint as a potential weak point. Recognizing the flawed privilege removal logic (blacklist vs whitelist), they would enumerate the UserRole enum to find unchecked roles. Combining this with knowledge of stored XSS vulnerabilities, they would chain both flaws for maximum impact—privilege escalation to compromise an admin account.

## Defensive takeaways
- Use whitelist/allow-list patterns for privilege assignment, never blacklist-based removal of sensitive attributes
- Remove or properly secure deprecated endpoints rather than leaving them accessible
- Validate and sanitize all user inputs, especially those that will be stored and later displayed to other users
- Apply input validation at the model/ORM layer to prevent mass assignment vulnerabilities
- Use Content Security Policy (CSP) headers to mitigate stored XSS impact
- Implement strict role-based access control (RBAC) with explicit privilege checking
- Perform regular security reviews of authentication and authorization logic, especially when roles/permissions are added
- Use automated testing to ensure new roles cannot be unexpectedly assigned via API endpoints

## Variant hunting
['Check for other deprecated API endpoints that may have similar mass assignment issues', 'Search for other fields where user input is stored and displayed to administrators (potential stored XSS vectors)', 'Test all role types in the enum against other user creation/modification endpoints', 'Enumerate all model fields to identify which ones are user-controllable and stored', 'Look for similar blacklist-based privilege removal patterns in other endpoints (update, patch, admin functions)', 'Test for other account types (PRO, UNDERAGE_BENEFICIARY) to see if they have similar mass assignment vulnerabilities', 'Check if the JOUVE role has specific permissions that could be exploited beyond standard beneficiary access']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1548: Abuse Elevation Control Mechanism
- T1078: Valid Accounts (privilege escalation via mass assignment)
- T1592: Gather Victim Identity Information (reconnaissance of enum values)
- T1059: Command and Scripting Interpreter (XSS payload execution)
- T1566: Phishing (potential admin-targeted payload delivery)
- T1021: Remote Service Session Hijacking (via stored XSS)

## Notes
This writeup demonstrates a chaining of two vulnerabilities for critical impact. The mass assignment vulnerability alone would be high-severity privilege escalation; combined with stored XSS, it achieves full application compromise. The use of deprecated endpoints in production is a common security hygiene issue. The dual mechanism (isAdmin boolean + roles array) suggests legacy code that wasn't fully refactored, increasing complexity and attack surface. The disclosure timeline and legal handling indicate responsible disclosure practices by the researcher.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
