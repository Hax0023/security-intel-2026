# Information Disclosure: Private Program Asset Groups Exposed via GraphQL Node Query

## Metadata
- **Source:** HackerOne
- **Report:** 1618347 | https://hackerone.com/reports/1618347
- **Submitted:** 2022-06-28
- **Reporter:** haxta4ok00
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Improper Access Control, Information Disclosure, Broken Object Level Authorization (BOLA), GraphQL Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A GraphQL endpoint fails to properly validate authorization when querying PolicyPageAssetGroup nodes, allowing unauthenticated attackers to retrieve sensitive asset scope information from private bug bounty programs. By crafting a direct node query with a known asset group ID, attackers can bypass access controls and disclose program assets that should only be visible to program members.

## Attack scenario
1. Attacker discovers or enumerates a valid PolicyPageAssetGroup ID (e.g., gid://hackerone/PolicyPageAssetGroupsIndex::PolicyPageAssetGroup/3981-41287)
2. Attacker crafts a GraphQL query using the node() endpoint with the asset group ID
3. Attacker sends the query without authentication headers or with minimal/invalid credentials
4. GraphQL endpoint executes the query and returns asset group details including the name field
5. Attacker gains visibility into private program asset scope that should be restricted
6. Attacker leverages disclosed asset information for targeted reconnaissance or to prioritize vulnerability research

## Root cause
The GraphQL node() endpoint implements insufficient authorization checks at the field/object level. While the endpoint may verify basic authentication, it fails to enforce proper access control rules when retrieving specific PolicyPageAssetGroup objects. The authorization logic likely checks permissions at the query level but not at the object resolution level, allowing direct node access to bypass program membership restrictions.

## Attacker mindset
An attacker with knowledge of GraphQL internals or who has discovered asset group ID patterns would systematically query the node endpoint to enumerate and collect asset scopes from private programs. This enables competitive intelligence gathering, vulnerability research prioritization, or identification of high-value targets without being invited to the program.

## Defensive takeaways
- Implement field-level authorization checks in GraphQL resolvers, not just at the query level
- Validate that the requesting user has explicit access to parent objects (programs) before returning related objects (asset groups)
- Add authorization middleware to the node() query that verifies the user can access the requested object type and specific instance
- Implement rate limiting and monitoring on GraphQL queries to detect enumeration attempts
- Conduct a full audit of GraphQL schema to identify other object types that may have similar authorization bypass vulnerabilities
- Use allowlists or restricted aliases for sensitive queries rather than generic node() endpoints
- Add logging and alerting for unauthorized or suspicious GraphQL query patterns

## Variant hunting
Test other asset-related GraphQL objects (PolicyPageAssetDocument, AssetGroup) for similar BOLA vulnerabilities
Attempt to query sensitive program fields through node() endpoint (e.g., program name, description, bounty amounts)
Test if asset group IDs are sequential or follow predictable patterns to enable bulk enumeration
Check if other entity types in HackerOne's GraphQL schema (Reports, Programs, Users) have similar node() authorization flaws
Attempt to retrieve deleted or archived asset groups through node() endpoint
Test if cursor-based pagination queries bypass authorization on asset group listings

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1526: Reconnaissance
- T1592: Gather Victim Identity Information
- T1040: Traffic Sniffing

## Notes
The report uses redaction (██████) for sensitive program names, indicating the researcher responsibly disclosed without exposing full details. The vulnerability is a classic case of broken object-level authorization (OWASP API3:2019). The fact that a 'recent update' introduced this suggests the authorization checks may have been modified or refactored improperly. The sequential-looking ID format (3981-41287) suggests potential for ID enumeration attacks. The vulnerability is particularly concerning for private programs as they typically involve unpaid or early-stage security research where confidentiality is critical.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hi team, I understand what's going on
**Description:**
Just a recent update gives the results of private programs
### Steps To Reproduce

Without authorization

GraphQL: 
`{"query":"{node(id:\"gid://hackerone/PolicyPageAssetGroupsIndex::PolicyPageAssetGroup/3981-41287\"){... on PolicyPageAssetGroupDocument{id,name}}}"}`

Answer:
`{"data":{"node":{"id":"Z2lkOi8vaGFja2Vyb25lL1BvbGljeVBhZ2VBc3NldEdyb3Vwc0luZGV4OjpQb2xpY3lQYWdlQXNzZXRHcm91cC8zOTgxLTQxMjg3","name":"██████"}}}`

This is Asset program - █████████

Thanks!

## Impact

Disclosing Sсope(Assets) in Private Programs

</details>

---
*Analysed by Claude on 2026-05-11*
