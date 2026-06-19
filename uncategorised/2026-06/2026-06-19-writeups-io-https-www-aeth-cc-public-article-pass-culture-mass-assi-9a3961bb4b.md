# Privileged Account Creation via Mass Assignment and Stored XSS in pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private, via YesWeHack)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Mass Assignment, Privilege Escalation, Stored Cross-Site Scripting (XSS), Insecure Direct Object References
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for user signup allowed attackers to create accounts with elevated privileges through mass assignment by injecting undocumented roles like 'JOUVE' that bypassed validation logic. The privileged account could then inject stored XSS payloads into the administration panel to compromise administrator accounts.

## Attack scenario (step by step)
1. Attacker identifies a deprecated /users/signup/webapp endpoint that accepts user input directly mapped to the User model
2. Attacker discovers the JOUVE role exists in the UserRole enumeration but is not explicitly removed by the validation logic (unlike ADMIN and BENEFICIARY)
3. Attacker crafts a POST request to the signup endpoint with roles array containing 'JOUVE' to create a privileged account
4. Attacker logs in with the newly created JOUVE account gaining access to restricted functionality
5. Attacker exploits a separate stored XSS vulnerability to inject malicious payload through the JOUVE account
6. When an administrator views the injected content, the XSS payload executes in their session, achieving full compromise

## Root cause
The application used a blacklist approach for privilege removal (explicitly removing ADMIN and BENEFICIARY roles) rather than a whitelist approach. When new roles were added to the enum (like JOUVE), they were not added to the removal logic, creating a gap. The direct instantiation of database models from user input (User(from_dict=request.json)) without strict field filtering enabled mass assignment of the roles array.

## Attacker mindset
The attacker methodically analyzed deprecated endpoints, reviewed the source code for role definitions, and identified a gap in the privilege removal logic. By chaining two vulnerabilities (mass assignment + stored XSS), they escalated from unauthenticated user to full administrative compromise, demonstrating defense-in-depth weaknesses.

## Defensive takeaways
- Use whitelist approach for allowed fields/roles rather than blacklist - explicitly define what can be modified
- Never use direct from_dict() or similar auto-mapping of user input to ORM models without explicit field validation
- Implement enum-driven validation that checks against all defined roles, not hardcoded role names
- Remove or properly deprecate old endpoints rather than leaving them functional with weaker security
- Apply the principle of least privilege - new roles should default to minimal permissions
- Use separate DTOs (Data Transfer Objects) for API input vs database models to prevent mass assignment
- Implement input validation before any data persistence operations
- Layer security controls - even if mass assignment succeeds, additional authorization checks at functional level

## Variant hunting
['Search for other endpoints using from_dict() or similar auto-mapping patterns without field whitelisting', 'Review all enum definitions for deprecated or unvalidated values that might grant unintended privileges', 'Test all deprecated API endpoints for similar mass assignment weaknesses', 'Check for other boolean flags (like isAdmin) that might have dual control mechanisms with arrays', 'Look for similar TODO/debt comments indicating incomplete security implementations', 'Test role-based access control enforcement at database constraint level vs application level', 'Search for stored XSS in admin panels that could be combined with any privilege escalation', 'Review all user creation endpoints (not just signup) for similar patterns']

## MITRE ATT&CK
- T1190
- T1078.001
- T1547.015
- T1598.003
- T1552.007

## Notes
This is a well-researched vulnerability chain demonstrating why security must be layered. The mass assignment alone was risky, but combined with stored XSS created critical impact. The use of TODO comments in code is a red flag for security auditors. The dual role management system (boolean isAdmin + roles array) increased complexity and created inconsistency that was exploited. The JOUVE role appears to be a temporary identification mechanism that should have been removed per the TODO comment. The writeup is incomplete in the provided excerpt but demonstrates excellent vulnerability analysis methodology.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
