# Privileged Account Creation via Mass Assignment and Stored XSS in pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private Program via YesWeHack)
- **Bounty:** Not Disclosed
- **Severity:** Critical
- **Vuln types:** Mass Assignment, Stored XSS, Privilege Escalation, Inadequate Input Validation
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for account creation was vulnerable to mass assignment, allowing attackers to assign themselves privileged roles (specifically the JOUVE role) that were not properly validated during account creation. An attacker could leverage this privileged account to inject a stored XSS payload into the administration panel, compromising administrator accounts.

## Attack scenario (step by step)
1. Attacker discovers the deprecated /users/signup/webapp endpoint by analyzing API routes
2. Attacker crafts a POST request to the endpoint with malicious JSON payload including the 'JOUVE' role in the roles array
3. The endpoint creates a User object from the request.json and only removes ADMIN and BENEFICIARY roles, missing the JOUVE role validation
4. Attacker receives an account with JOUVE privileges, bypassing intended access controls
5. Attacker uses the privileged JOUVE account to access restricted functionality and inject XSS payload
6. Stored XSS payload executes when an administrator views the compromised content, leading to full compromise of the admin account

## Root cause
The application implemented a blacklist-based approach (removing specific roles) rather than a whitelist approach when creating user accounts. When the User model was instantiated from request.json via mass assignment, all provided attributes including the roles array were accepted. The removal of ADMIN and BENEFICIARY roles was insufficient because it didn't account for other privileged roles like JOUVE. This is a classic mass assignment vulnerability combined with inadequate input validation.

## Attacker mindset
The attacker methodically analyzed the source code to identify deprecated endpoints with weaker security controls. Upon recognizing the mass assignment vulnerability and the insufficient role validation logic, the attacker realized they could assign themselves an overlooked privileged role (JOUVE). The attacker then escalated this to full account compromise by leveraging the elevated privileges to inject a stored XSS payload that would compromise administrator accounts.

## Defensive takeaways
- Use whitelist-based validation for sensitive attributes instead of blacklist-based removal
- Implement strict input validation at the model level, explicitly defining which fields users can set
- Avoid direct instantiation of database models from untrusted input (User(from_dict=request.json))
- Use data transfer objects (DTOs) or serialization libraries that restrict field assignment
- Consolidate privilege mechanisms - the dual isAdmin boolean and roles array creates confusion and maintenance issues
- Retire deprecated endpoints promptly rather than maintaining them alongside newer versions
- Implement comprehensive role-based access control testing for all roles in the enumeration
- Apply principle of least privilege when creating accounts - set default roles explicitly rather than removing unwanted ones
- Implement output encoding to prevent stored XSS even if privilege escalation occurs

## Variant hunting
['Check other account creation endpoints for similar mass assignment vulnerabilities with different role types', 'Search for other endpoints accepting User(from_dict=...) pattern that may have similar issues', 'Analyze all role enums for overlooked/legacy roles that might bypass current validation', 'Test other deprecated API endpoints marked with @debt comments for security bypasses', 'Look for endpoints that modify user roles/permissions and check if they have similar blacklist-based validation', 'Review if JOUVE role is used in other privilege checks that could be chained with mass assignment', "Test account update/patch endpoints to see if they're also vulnerable to mass assignment"]

## MITRE ATT&CK
- T1190
- T1548
- T1566
- T1059

## Notes
This is a well-documented vulnerability chain: mass assignment leading to privilege escalation, which then enables stored XSS for admin account compromise. The vulnerability highlights the dangers of: (1) maintaining deprecated code with weaker controls, (2) using blacklist-based validation, (3) dual/conflicting authorization mechanisms, and (4) direct model hydration from user input. The writeup is from a legitimate bug bounty disclosed post-patch. The JOUVE role appears to be a legacy authentication mechanism pending removal based on the TODO comment in the code.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
