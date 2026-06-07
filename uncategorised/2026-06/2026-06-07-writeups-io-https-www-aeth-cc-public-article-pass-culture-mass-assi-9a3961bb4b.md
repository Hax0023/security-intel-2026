# Privileged Account Creation via Mass Assignment and Stored XSS in pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private)
- **Bounty:** Not publicly disclosed
- **Severity:** critical
- **Vuln types:** Mass Assignment, Privilege Escalation, Stored Cross-Site Scripting (XSS), Insecure Direct Object References
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for user account creation was vulnerable to mass assignment, allowing attackers to assign privileged roles (JOUVE) to newly created accounts. By combining this privilege escalation with a stored XSS vulnerability in the administration panel, an attacker could achieve full compromise by injecting malicious payloads that would execute in administrator contexts.

## Attack scenario (step by step)
1. Attacker discovers a deprecated /users/signup/webapp endpoint still active in the API
2. Attacker crafts a POST request to the signup endpoint with custom JSON payload including the JOUVE role in the roles array
3. The endpoint creates a User object from the entire request.json without proper validation, then only removes ADMIN and BENEFICIARY roles
4. The JOUVE role is not removed, allowing the attacker to obtain a privileged account with special permissions
5. Attacker logs in with the privileged JOUVE account and injects a malicious payload into a field that is stored in the database
6. When an administrator views the affected content in the admin panel, the stored XSS payload executes in their browser context, allowing session hijacking or further compromise

## Root cause
The application implements a dangerous pattern: creating a database model object from untrusted user input and then attempting to remove sensitive attributes rather than using an allowlist of permitted fields. The coexistence of two privilege mechanisms (isAdmin boolean and roles array) created inconsistency. The deprecated endpoint was not properly decommissioned and lacked input validation on the roles parameter.

## Attacker mindset
An attacker analyzing the API for deprecated or poorly maintained endpoints would recognize that legacy code often lacks modern security controls. The attacker would understand that mass assignment vulnerabilities arise from overly permissive object deserialization and would test for overlooked roles during account creation. By chaining this with stored XSS, the attacker escalates from account creation to administrative account compromise.

## Defensive takeaways
- Use allowlists (whitelist) for model binding instead of blacklists - explicitly define which fields users can set during account creation
- Implement strict input validation on enumeration fields like roles; validate against defined enum values only
- Remove or properly decommission deprecated API endpoints rather than leaving them active; use HTTP 410 Gone or 404
- Unify privilege mechanisms - avoid having multiple ways to represent the same privilege (isAdmin boolean AND roles array)
- Apply consistent output encoding for stored data before rendering in admin panels to prevent XSS
- Implement a deny-by-default approach for sensitive operations, requiring explicit opt-in rather than removal of unwanted attributes
- Add automated tests to verify that users created via signup endpoints have exactly the expected permissions
- Use database constraints and triggers as a secondary defense layer for privilege validation
- Conduct regular code audits specifically targeting mass assignment patterns and deprecated functionality

## Variant hunting
['Search for other deprecated endpoints marked with @debt or TODO comments that might accept user input for object creation', 'Test all account creation endpoints with payloads containing different role values (test each enum value in UserRole class)', 'Check for other boolean/array privilege duplication patterns in the codebase that might allow similar bypass', 'Identify other endpoints accepting from_dict patterns and test for mass assignment across the entire API surface', 'Look for stored user-controlled data reflected in admin panels or reporting features as XSS sinks', 'Test other user modification endpoints for mass assignment (profile updates, preference changes, etc.)', 'Check if similar privilege escalation exists for PRO or UNDERAGE_BENEFICIARY roles through different endpoints']

## MITRE ATT&CK
- T1190
- T1548
- T1547
- T1195

## Notes
This writeup demonstrates the importance of API security hygiene. The researcher discovered this after previously finding a stored XSS, showing how chaining vulnerabilities creates critical impact. The disclosure was coordinated responsibly through the YesWeHack platform. The JOUVE role appears to be for a third-party identification mechanism (Jouve is a French service provider) that was never properly secured. The bug bounty was private and required special invitation, limiting public discussion until after patching.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
