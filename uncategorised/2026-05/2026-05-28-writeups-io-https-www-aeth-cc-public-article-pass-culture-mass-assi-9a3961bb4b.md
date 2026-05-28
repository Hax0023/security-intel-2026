# Privileged Account Creation via Mass Assignment and Stored XSS in Pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Pass Culture Bug Bounty (Private, via YesWeHack)
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln types:** Mass Assignment, Privilege Escalation, Stored XSS, Insecure Direct Object References
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated account creation endpoint vulnerable to mass assignment allowed attackers to create accounts with privileged roles (JOUVE) by directly assigning values to the database model before sanitization. Combined with a stored XSS vulnerability in the administration panel, this enabled full compromise of administrator accounts.

## Attack scenario (step by step)
1. Attacker discovers deprecated /users/signup/webapp endpoint that accepts user input directly into User model instantiation
2. Attacker crafts POST request to signup endpoint with JOUVE role included in roles array parameter
3. Application removes only ADMIN and BENEFICIARY roles but fails to remove JOUVE role due to whitelist approach vulnerability
4. Attacker gains account with JOUVE privileges (administrative functionality)
5. Attacker injects stored XSS payload through privileged account interface into administration panel
6. When administrator views compromised data, XSS payload executes in their browser session, enabling account takeover

## Root cause
Insecure design pattern: creating database objects with all user-supplied input first, then attempting to remove sensitive attributes via blacklist, rather than using a whitelist approach. Combined with incomplete role enumeration in removal logic - JOUVE role was not included in the remove_admin_role() and remove_beneficiary_role() cleanup functions. The dual isAdmin boolean and roles array authentication mechanism created additional confusion.

## Attacker mindset
An experienced code reviewer identifying architectural anti-patterns and role-based access control flaws. The attacker recognized that the 'remove-after-creation' pattern is fundamentally flawed and that newly added roles (JOUVE with TODO comment) were not protected. They chained the privilege escalation with XSS to achieve horizontal privilege escalation to administrator level.

## Defensive takeaways
- Use whitelist approach: only assign explicitly allowed attributes to objects, never create with all user input then remove sensitive fields
- Implement proper input validation and model binding that restricts assignable fields at the framework level (e.g., DTO/VO pattern)
- Consolidate authentication mechanisms - avoid dual isAdmin boolean and roles array, use single source of truth
- Review TODO comments and deprecated code paths regularly - these are high-risk attack surfaces
- Apply principle of least privilege: default accounts should have no roles unless explicitly granted
- Implement Content Security Policy (CSP) headers to mitigate stored XSS impact
- Add database-level constraints and triggers to enforce role consistency
- Sanitize and validate all user input regardless of endpoint deprecation status
- Include comprehensive role coverage in removal/filtering logic with explicit comments for each role

## Variant hunting
["Search for other endpoints using 'from_dict' or similar bulk assignment patterns with post-creation filtering", 'Identify all role enums and verify each is explicitly handled in filtering logic', 'Look for deprecated endpoints marked with @debt or TODO comments that may bypass newer security controls', 'Check for other dual-mechanism access controls (multiple fields determining same permission)', 'Hunt for XSS in other admin panels or privileged interfaces that might be accessible via other privilege escalation vectors', 'Review all User model assignments for incomplete sanitization of roles, permissions, or sensitive fields']

## MITRE ATT&CK
- T1190
- T1548.002
- T1548.004
- T1087.001
- T1176
- T1566.002

## Notes
This is a well-documented real-world example of mass assignment vulnerability in Python/Flask application with SQLAlchemy ORM. The writeup explicitly notes the @debt api-migration decorator indicating legacy code, which is a red flag for incomplete security controls. The attacker's understanding of the dual authentication mechanism and identification of the TODO comment around the JOUVE role demonstrates thorough code analysis. The chaining of two vulnerabilities (privilege escalation + XSS) to achieve full compromise is a sophisticated attack scenario. Pass Culture is a French government initiative, making this a high-impact disclosure for a public service.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
