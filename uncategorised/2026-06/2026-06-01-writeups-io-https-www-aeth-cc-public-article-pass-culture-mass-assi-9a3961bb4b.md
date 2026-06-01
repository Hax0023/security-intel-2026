# Privileged Account Creation via Mass Assignment and Stored XSS in pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private, via YesWeHack)
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln types:** Mass Assignment, Privilege Escalation, Stored XSS, Insecure Direct Object References
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for user signup allowed mass assignment of sensitive attributes including privileged roles (JOUVE role). An attacker could create accounts with elevated privileges and subsequently inject stored XSS payloads into the administration panel to compromise administrator accounts. This vulnerability chained together account privilege escalation with persistent XSS to achieve full application compromise.

## Attack scenario (step by step)
1. Attacker discovers deprecated /users/signup/webapp endpoint that accepts arbitrary user attributes via JSON
2. Attacker sends POST request with malicious JSON including JOUVE role in the roles array
3. Application instantiates User object from attacker-controlled dictionary via mass assignment
4. Code removes ADMIN and BENEFICIARY roles but fails to remove JOUVE role (not in blocklist)
5. Attacker gains account with JOUVE privilege and accesses administration functions
6. Attacker injects malicious XSS payload into administrative fields, compromising admin accounts when they view the data

## Root cause
Insecure mass assignment pattern where the application creates database objects from untrusted user input first, then attempts to remove sensitive attributes. The blocklist approach (removing specific roles) is fragile - when new roles like JOUVE exist but aren't explicitly removed, they bypass the mitigation. Additionally, dual privilege mechanisms (isAdmin boolean + roles array) create complexity.

## Attacker mindset
Opportunistic security researcher exploiting common web framework patterns. Recognition that deprecated endpoints often lack security hardening. Identifying that whitelist-based role assignment exists but relies on incomplete role enumeration in the removal logic. Chaining multiple vulnerabilities (privilege escalation + XSS) to maximize impact.

## Defensive takeaways
- Use whitelist approach (explicitly define allowed fields) rather than blacklist when binding user input to models
- Implement explicit DTOs/schemas that exclude sensitive fields entirely rather than removing them post-instantiation
- Consolidate privilege mechanisms - avoid dual isAdmin/roles patterns that increase attack surface
- Remove deprecated endpoints promptly or apply equal security rigor as active endpoints
- Implement comprehensive input validation and output encoding to prevent injection attacks in privileged accounts
- Use database constraints and application-level checks to enforce role invariants
- Conduct threat modeling around privilege escalation paths when adding new roles

## Variant hunting
['Search for other endpoints using User(from_dict=request.json) pattern without proper field validation', 'Identify all database models accepting mass assignment and audit their sensitive field removal logic', 'Enumerate all UserRole values and verify each is properly restricted in signup endpoints', 'Check for other dual-mechanism privilege systems (boolean flag + array/enum) in codebase', 'Test account creation endpoints for undocumented role types or future-proofing issues', 'Review all administrative endpoints for stored XSS vulnerabilities when accessed by elevated accounts', 'Examine backup/legacy API versions for inconsistent security controls']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1070 - Indicator Removal
- T1059 - Command and Scripting Interpreter
- T1555 - Credentials from Password Stores

## Notes
This is a sophisticated chained vulnerability requiring knowledge of both backend privilege mechanisms and frontend XSS injection. The writeup demonstrates excellent security research methodology by discovering deprecated code paths and understanding dual privilege mechanisms. The JOUVE role appears to be a TODO for proper identification mechanism, suggesting incomplete refactoring. Disclosure followed responsible vulnerability reporting timeline with vendor patch before publication.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
