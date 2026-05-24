# Improper Authorization on /api/as/v1/credentials/ for Dev Role User with Limited Engine Access

## Metadata
- **Source:** HackerOne
- **Report:** 1218680 | https://hackerone.com/reports/1218680
- **Submitted:** 2021-06-06
- **Reporter:** superman85
- **Program:** Elastic Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper Authorization, Privilege Escalation, Broken Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
A Dev role user with Limited Engine Access can bypass authorization controls to access the /api/as/v1/credentials/ API endpoint, allowing them to retrieve all API keys (private keys, search keys, etc.) across the entire App Search instance. This represents a privilege escalation vulnerability where users should only manage credentials for engines they have access to.

## Attack scenario
1. Attacker creates a standard Dev role user account in Kibana with limited engine access to no specific engines
2. Attacker maps this user through role-mappings with Limited Engine Access settings
3. Attacker logs into App Search with the Dev role credentials
4. Attacker directly accesses the /api/as/v1/credentials/ API endpoint via HTTP request
5. Attacker retrieves sensitive API keys including Private Admin Keys with read/write access to all engines
6. Attacker uses obtained Private Admin Keys to create, modify, or delete credentials across all engines

## Root cause
The API endpoint /api/as/v1/credentials/ lacks proper authorization validation to check if the requesting user has appropriate permissions before returning all credentials. The authorization checks implemented for Limited Engine Access role are not enforced at the API layer, only at the UI layer.

## Attacker mindset
An insider or compromised account with Dev role permissions could escalate privileges by extracting sensitive credentials. The attacker recognizes that UI-based restrictions can be bypassed by directly calling APIs, a common pattern in authorization bypasses.

## Defensive takeaways
- Implement server-side authorization checks for all API endpoints, not relying on UI-based restrictions
- Enforce role-based access control (RBAC) at the API layer to validate user permissions before returning sensitive data
- Implement credential filtering based on user's assigned engines - Dev users should only access credentials for their permitted engines
- Add audit logging for sensitive API credential access and retrieval attempts
- Conduct security review of all role-based permission implementations to identify similar bypasses
- Implement consistent authorization enforcement across both UI and API layers

## Variant hunting
Check other API endpoints that may be missing authorization checks (/api/as/v1/engines/, /api/as/v1/logs/, etc.)
Test other role types (Analyst, Editor) for similar authorization bypasses
Verify if credentials can be accessed through other HTTP methods (PUT, DELETE, PATCH)
Check if API keys themselves can be used to access credentials beyond their intended scope
Test whether user can access credentials through engine-specific endpoints with modified parameters

## MITRE ATT&CK
- T1190
- T1078
- T1548
- T1555

## Notes
This is a follow-up to issue #1168528, indicating previous authorization issues in the same component. The vulnerability demonstrates the critical importance of server-side authorization validation and the inadequacy of client-side/UI-based access restrictions. The presence of a Private Admin Key with full permissions makes this particularly severe.

## Full report
<details><summary>Expand</summary>

**Summary:**
Dear Team,

Since  #1168528 was resolved. I have checking again for other roles. At Dev Role with Limited Engine Access, an user still can access API endpoint 
`/api/as/v1/credentials/` to get all API keys (private-key, search-key ... )

## Steps To Reproduce:

1 - Log in Kibana with the admin (elastic) user and go to the Stack Management > Users page (/app/management/security/users/)
2 - Choose an username , password and role for this user. For example you can choose username: **dev**
3 - Log in App Search with the admin (elastic) user and go to the Users & roles page (/as#/role-mappings/)
4 - Click Add mapping
5 - External Attribute choose **username** , in the Attribute value field enter **dev**
6 - In the Role box select Dev
7 - In Engine Access select Limited Engine Access, no need to select any engine
8 - Login to App Search with user **dev**
9 - Go to endpoint https://your_app_search_instance/api/as/v1/credentials/
10 - You still can get all api keys 

I have attached video PoC
█████████

## Impact

Privilege escalation. The default App Search install has a Private API Key with read/write access to all engines. If a Private Admin Key has been created before. the attacker can use it to create new API keys or delete existing ones.

With Limited Engine Acess, an user should create and managed their own api keys

</details>

---
*Analysed by Claude on 2026-05-24*
