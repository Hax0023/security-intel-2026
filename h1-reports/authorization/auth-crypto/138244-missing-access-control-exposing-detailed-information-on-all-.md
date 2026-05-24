# Missing Access Control in WP REST API Users Endpoint Exposes All User Details

## Metadata
- **Source:** HackerOne
- **Report:** 138244 | https://hackerone.com/reports/138244
- **Submitted:** 2016-05-12
- **Reporter:** albinowax
- **Program:** WordPress REST API Plugin
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Missing Access Control, Information Disclosure, Broken Authentication
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The WP REST API plugin fails to enforce access controls on the users endpoint when accessed with the 'edit' context parameter, allowing unauthenticated attackers to retrieve sensitive information for all registered users including emails, names, and privilege levels. This information disclosure vulnerability enables attackers to target administrators and plan further attacks against WordPress installations.

## Attack scenario
1. Attacker discovers a WordPress site using the WP REST API plugin
2. Attacker sends unauthenticated GET request to /wp-json/wp/v2/users?context=edit
3. API responds with full user details for all registered accounts without requiring authentication
4. Attacker extracts email addresses, usernames, and privilege information from response
5. Attacker uses admin email addresses for targeted phishing or account takeover attempts
6. Attacker gains unauthorized administrative access to WordPress installation and webserver

## Root cause
The WP REST API plugin does not validate user authentication or authorization before returning user data in the 'edit' context. The access control checks are either missing entirely or not applied to the context parameter handling, allowing context escalation to expose sensitive fields normally restricted to authenticated users.

## Attacker mindset
Reconnaissance-focused attacker seeking to enumerate target infrastructure and identify high-value accounts (administrators) for targeted social engineering, credential stuffing, or brute force attacks. The detailed user information significantly reduces reconnaissance effort and increases attack precision.

## Defensive takeaways
- Always enforce authentication and authorization checks before exposing user data, regardless of API context parameters
- Apply principle of least privilege - different API contexts should validate permissions independently
- Implement role-based access control (RBAC) at the API endpoint level, not just in documentation
- Never trust client-supplied parameters (like 'context') to modify security boundaries without re-validation
- Restrict REST API user enumeration endpoints to authenticated requests only
- Regularly audit REST API endpoints for context-based access control bypasses
- Consider disabling REST API user discovery via /wp-json/wp/v2/users for public-facing sites

## Variant hunting
Check for similar context parameter bypasses in other REST API endpoints (/posts, /pages, /comments)
Test other WordPress REST API plugins for identical access control flaws
Review other query parameters that might bypass access controls (context, embed, _fields)
Investigate whether the vulnerability applies to single user endpoints (/wp-json/wp/v2/users/1)
Test if similar plugins have patched this issue and compare code paths
Check for bypass techniques using HTTP method overloading or header manipulation

## MITRE ATT&CK
- T1526 - Reconnaissance/Enumerate domain users
- T1589 - Gather Victim Identity Information
- T1087 - Account Discovery
- T1592 - Gather Victim Host Information
- T1190 - Exploit Public-Facing Application

## Notes
This is a critical reconnaissance vulnerability that enables attackers to identify high-value targets within an organization. The severity is elevated because it requires no authentication and provides comprehensive enumeration data. The researcher appropriately notified affected parties directly, showing responsible disclosure practices. The fix likely involves adding proper capability checks and authentication requirements to the users endpoint before returning sensitive data fields.

## Full report
<details><summary>Expand</summary>

The WP REST API WordPress plugin fails to apply access controls for the 'edit' context. This means that with a single HTTP request, an attacker can obtain the following information for every single registered user: username, email address, first name, last name, date of registration, and detailed privilege information. This is a treasure trove of information for someone planning an attack - they know exactly which email addresses to target in order to gain admin privileges and complete control over the webserver.

To replicate this issue, simply send the following request while unauthenticated:
GET /wp-json/wp/v2/users?context=edit

Please note that I've submitted this report to a couple of entities directly affected by this vulnerability so they can implement a workaround.

</details>

---
*Analysed by Claude on 2026-05-24*
