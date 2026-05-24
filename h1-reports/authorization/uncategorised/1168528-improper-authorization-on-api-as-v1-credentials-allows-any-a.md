# Improper Authorization on /api/as/v1/credentials/ Allows Privilege Escalation and API Key Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 1168528 | https://hackerone.com/reports/1168528
- **Submitted:** 2021-04-19
- **Reporter:** dee-see
- **Program:** Elastic Bug Bounty Program
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Broken Access Control, Improper Authorization, Privilege Escalation, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The App Search API endpoint `/api/as/v1/credentials/` fails to properly enforce role-based access controls, allowing any authenticated user to view all API keys regardless of their assigned role. This bypasses the UI-level authorization present on the credentials page and enables privilege escalation through access to highly privileged Private Admin Keys.

## Attack scenario
1. Attacker creates a low-privileged App Search user account with Analyst role and minimal engine access
2. Attacker authenticates as this limited user and navigates to /api/as/v1/credentials/ endpoint
3. API endpoint improperly returns all API keys in the system without role validation
4. Attacker retrieves Private Admin Keys with read/write access to all engines
5. Attacker uses the leaked Private Admin Key to create new administrative API keys or delete existing ones
6. Attacker gains unauthorized access to all engines and data, achieving full privilege escalation

## Root cause
Authorization checks are only implemented in the UI layer (credentials page) but missing from the API endpoint handler. The API endpoint `/api/as/v1/credentials/` does not validate user role/permissions before returning sensitive API key data, relying solely on authentication rather than authorization.

## Attacker mindset
An attacker with basic user access seeks to escalate privileges by discovering authorization bypass opportunities. API endpoints are probed for missing authorization checks that might bypass UI restrictions. Once privileged API keys are obtained, they enable lateral movement and full system compromise.

## Defensive takeaways
- Always implement authorization checks at the API handler level, not just in the UI layer
- Use a consistent authorization mechanism across both UI and API endpoints
- Apply principle of least privilege - API endpoints should return only data the authenticated user is authorized to access based on their role
- Implement role-based access control (RBAC) checks before returning sensitive resources like API keys
- Add comprehensive audit logging for API key access attempts and retrieval
- Regular security testing should include API endpoint authorization testing independent of UI testing
- Consider implementing scoped API keys with minimal permissions rather than master keys when possible

## Variant hunting
Search for other API endpoints in App Search that list or return sensitive data without proper role validation (e.g., engines list, user list, configuration endpoints). Check other Elastic products (Kibana, Elasticsearch) for similar patterns where UI authorization differs from API authorization. Look for endpoints that return lists of resources (keys, tokens, secrets) that should be filtered by user role.

## MITRE ATT&CK
- T1190
- T1556
- T1098
- T1087
- T1526

## Notes
This is a classic authorization bypass vulnerability where UI-level controls provide false security. The use of role-mapped users (Analyst, Editor roles) demonstrates the expected authorization model, making the API bypass more severe. The availability of Private Admin Keys with full engine access makes this vulnerability immediately exploitable for complete system compromise. This vulnerability likely affects all authenticated users with insufficient role checks.

## Full report
<details><summary>Expand</summary>

## Summary

Hello team, I hope you're doing well! App Search has a credentials page located at `/as#/credentials` that lists all the API keys a user has access to, if any. That same page will 404 for users with `Analyst` or `Editor` role. This is all working as intended, however there is also an [API endpoint](https://www.elastic.co/guide/en/app-search/current/credentials.html) to query that same data at `/api/as/v1/credentials/` and this will list all existing API keys for any authenticated user regardless of their App Search role.

## Steps to reproduce

I'm going to use the cloud environment for the reproduction

### Preparation

1. Log in App Search with the admin (`elastic`) user and go to the `Users & roles` page (`/as#/role-mappings/`)
1. Click `Add mapping`
1. In the `Attribute value` field enter `h1-repro`
1. In the `Role` box select `Analyst`
1. In the `Engine Access` select `Limited Engine Access`, no need to select any engine
    - We now have created the most limited role possible
1. Log in Kibana with the admin (`elastic`) user and go to the `Stack Management` > `Users` page (`/app/management/security/users/`)
1. Click `Create user`
1. In the `Username` field enter `hi-repro`
1. Set any password you like and then click `Create user`

### Reproduction

1. Log in App Search with the `h1-repro` user
1. Navigate to `/as#/role-mappings/` and observe that it's a 404 because you don't have access to this page
1. Navigate to `/api/as/v1/credentials/` and observe that you have access to all the API keys

## Impact

Privilege escalation. The default App Search install has a [Private API Key with read/write access to all engines](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-key-types). If a Private Admin Key has been created before. the attacker can use it to create new API keys or delete existing ones.

</details>

---
*Analysed by Claude on 2026-05-24*
