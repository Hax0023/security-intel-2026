# Privileged Account Creation via Mass Assignment and Stored XSS in Pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Pass Culture (Private Bug Bounty via YesWeHack)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Mass Assignment, Stored XSS, Privilege Escalation, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for user signup was vulnerable to mass assignment, allowing attackers to inject the JOUVE role (not explicitly removed) to create privileged accounts. From this elevated position, attackers could inject stored XSS payloads into the administration panel to compromise administrator accounts.

## Attack scenario (step by step)
1. Attacker discovers deprecated /users/signup/webapp endpoint through API enumeration
2. Attacker crafts signup request with user input containing JOUVE role in roles array
3. Application creates User object with all input fields including roles (mass assignment)
4. Application only removes ADMIN and BENEFICIARY roles, but misses JOUVE role
5. JOUVE role persists in database granting elevated privileges to attacker account
6. Attacker uses JOUVE account to access admin panel and inject stored XSS payload targeting administrators

## Root cause
Insecure object instantiation pattern: application creates database object with all user-supplied input, then attempts to sanitize by removing sensitive attributes post-creation. This approach is fragile because new roles added to the UserRole enum are not automatically removed unless explicitly coded. The JOUVE role was legacy code marked for removal but not included in the removal logic.

## Attacker mindset
Methodical code analyzer identifying deprecated endpoints and role enumeration. Recognizes the anti-pattern of blacklist-based sanitization (remove specific roles) versus whitelist approach (only allow specific roles). Exploits the gap between intended and actual role removals to escalate privileges, then chains to stored XSS for lateral admin account compromise.

## Defensive takeaways
- Use whitelist approach: explicitly define which fields are user-assignable, reject all others
- Implement allowlist-based role assignment rather than blacklist removal of sensitive roles
- Decommission deprecated endpoints completely rather than leaving them functional with comment debt markers
- Separate role assignment into dedicated, strictly-validated methods rather than generic object hydration
- Add database constraints to prevent unauthorized role combinations (application-level and database-level)
- Implement request validation schemas that explicitly enumerate permitted fields per endpoint
- Remove legacy roles (like JOUVE marked TODO) proactively before they become security debt
- Use input validation frameworks that support strict schema definition and reject unknown fields

## Variant hunting
['Search for other User object creation endpoints using similar from_dict patterns without strict field whitelisting', 'Identify other deprecated endpoints marked with @debt or TODO comments that may have weaker validation', 'Check for other role enum values marked for removal that may not be stripped in any code path', 'Test endpoints accepting arbitrary JSON input without explicit schema validation', 'Hunt for dual privilege mechanisms (boolean + array) that may have inconsistent enforcement', 'Examine other deprecated features or roles throughout codebase that became security gaps', 'Test mass assignment patterns on endpoints for other models (BeneficiaryAccount, ProfessionalAccount, etc.)']

## MITRE ATT&CK
- T1190
- T1078
- T1566
- T1098
- T1548

## Notes
This vulnerability chain demonstrates the dangers of technical debt and legacy code. The JOUVE role was explicitly marked TODO for removal but remained functional and unprotected. The writeup highlights that deprecated endpoints should be removed entirely, not merely marked in comments. The combination with stored XSS shows how initial privilege escalation can be weaponized for lateral movement and admin account compromise. The researcher methodically analyzed API routes and source code rather than relying solely on application behavior testing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
