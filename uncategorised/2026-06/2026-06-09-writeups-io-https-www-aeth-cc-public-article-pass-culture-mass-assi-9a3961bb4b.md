# Privileged Account Creation via Mass Assignment + Stored XSS in Pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Pass Culture Bug Bounty (Private Program via YesWeHack)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Mass Assignment, Privilege Escalation, Stored Cross-Site Scripting (XSS), Insecure Direct Object References
- **Category:** uncategorised
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/mass-assignment-article-en.html

## Summary
A deprecated API endpoint for user account creation was vulnerable to mass assignment, allowing attackers to inject arbitrary roles (specifically the JOUVE role) during signup. This granted elevated privileges that could be leveraged to inject malicious payloads into admin panels, resulting in stored XSS affecting administrator accounts.

## Attack scenario (step by step)
1. Attacker identifies deprecated /users/signup/webapp endpoint that accepts raw JSON for User object creation
2. Attacker includes arbitrary role values (e.g., JOUVE) in signup request, exploiting mass assignment vulnerability
3. Application creates User object from attacker-controlled JSON, then only removes ADMIN and BENEFICIARY roles but misses JOUVE role
4. Attacker's account is created with elevated JOUVE privileges, bypassing intended role restrictions
5. Attacker uses elevated privileges to access restricted functionality and inject stored XSS payload
6. Administrator accesses affected panel, payload executes in admin context, enabling full account compromise

## Root cause
Unsafe mass assignment pattern: application creates database model from raw user input via 'from_dict=request.json', then attempts to sanitize by removing known dangerous roles. This blacklist approach fails when new roles exist or when multiple privilege escalation paths are available. Two concurrent authorization mechanisms (isAdmin boolean + roles array) created inconsistency.

## Attacker mindset
Opportunistic source code auditor identifying deprecated endpoints and weak authorization patterns. Recognized that blacklist-based role removal is fragile and that leftover roles like JOUVE could provide stepping stones to admin functionality. Chained vulnerabilities for maximum impact.

## Defensive takeaways
- Never use mass assignment from untrusted input to hydrate ORM objects; use explicit field mapping/whitelisting instead
- Use whitelist (allow) rather than blacklist (deny) approaches for sensitive attributes like roles
- Consolidate multiple authorization mechanisms (isAdmin boolean + roles array) into single source of truth
- Regularly audit and remove deprecated endpoints, especially those with differing security controls
- Implement role validation at database schema level with CHECK constraints beyond application logic
- Apply input validation before ORM object creation, not after
- Sanitize all user input that reaches templates/admin panels to prevent stored XSS chaining

## Variant hunting
['Search for other deprecated signup endpoints with similar mass assignment patterns', 'Check for other roles in UserRole enum that may not be explicitly removed (UNDERAGE_BENEFICIARY, PRO)', 'Hunt for inconsistencies between isAdmin boolean checks and roles array membership across codebase', "Identify other endpoints accepting 'from_dict=request.json' pattern without explicit field whitelisting", 'Test if roles can be injected via other endpoints (profile update, admin creation flows)', 'Check if database constraints properly enforce role constraints at schema level']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts (account creation with elevated privileges)
- T1647 - Plist File Modification (if configuration files exploitable)
- T1539 - Steal Web Session Cookie (via stored XSS)
- T1057 - Process Discovery (post-compromise via admin panel)

## Notes
This is a well-researched vulnerability chain combining two distinct flaws: mass assignment for privilege escalation and stored XSS for admin compromise. The writeup demonstrates excellent source code analysis skills. The existence of TODO comments in code (JOUVE role removal pending) and deprecated endpoints suggests the application was undergoing active development. The dual authorization mechanism (isAdmin + roles array) is particularly concerning as it created multiple code paths for privilege checking. Pass Culture's public-facing nature as a French government service makes this a high-impact finding. Timeline and full disclosure process followed responsible disclosure practices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
