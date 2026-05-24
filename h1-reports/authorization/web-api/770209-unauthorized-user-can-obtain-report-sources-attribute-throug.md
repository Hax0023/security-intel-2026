# Unauthorized user can obtain report_sources attribute through Team GraphQL object

## Metadata
- **Source:** HackerOne
- **Report:** 770209 | https://hackerone.com/reports/770209
- **Submitted:** 2020-01-08
- **Reporter:** haxta4ok00
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** medium
- **Vuln:** Information Disclosure, Improper Access Control, GraphQL Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An unauthenticated or low-privileged user can query the GraphQL API to retrieve the 'report_sources' attribute of any team, which reveals whether a program is private and has external links configured. The presence of 'HackerOne Platform' in report_sources indicates a private program with external reporting capabilities, allowing attackers to enumerate and identify private programs.

## Attack scenario
1. Attacker discovers the GraphQL endpoint at hackerone.com/graphql is accessible without authentication
2. Attacker crafts a simple GraphQL query requesting team(handle) with report_sources field
3. Attacker iterates through known or guessed team handles to enumerate programs
4. Attacker observes that report_sources field contains ['HackerOne Platform'] for private programs with external links
5. Attacker builds a list of private programs and their configurations without authorization
6. Attacker uses this information to target specific private programs or understand program scope

## Root cause
The GraphQL API lacks proper field-level authorization checks on the 'report_sources' attribute. The resolver for the Team object does not validate whether the requesting user has permission to view sensitive program configuration details before returning the data.

## Attacker mindset
An attacker seeks to enumerate all programs on the platform, especially private ones. By discovering which programs accept external reports through the report_sources field, they can identify less-monitored private programs or gain competitive intelligence about which organizations run private bug bounty programs.

## Defensive takeaways
- Implement field-level authorization checks in GraphQL resolvers to prevent returning sensitive configuration data to unauthorized users
- Sanitize all GraphQL responses based on user permissions - even if an object is queryable, sensitive nested fields should be restricted
- Audit all GraphQL schema for sensitive fields that should require authentication or specific authorization levels
- Consider implementing query complexity analysis and rate limiting on GraphQL endpoints to prevent enumeration attacks
- Test GraphQL endpoints with both authenticated and unauthenticated requests for information disclosure
- Use schema directives or middleware to automatically enforce authorization rules across sensitive fields

## Variant hunting
Check other team/program attributes exposed through GraphQL (e.g., members, settings, policy details, invitation tokens)
Test REST API endpoints for similar report_sources or program configuration exposure
Attempt to query nested objects (e.g., reports, submissions) within private teams
Test if other sensitive fields like 'private', 'is_public', or 'external_program_url' are exposed
Enumerate user objects for sensitive field exposure through GraphQL
Test for authorization bypass on mutation operations that might create or modify program settings

## MITRE ATT&CK
- T1526 - Reconnaissance: Passive Scanning (GraphQL introspection)
- T1590 - Gather Victim Identity Information (enumeration of programs/organizations)
- T1538 - SaaS Software Discovery (identifying private programs)
- T1589 - Gather Victim Identity Information (collecting program configurations)
- T1040 - Network Sniffing (observing GraphQL queries)

## Notes
The researcher notes poor English communication but clearly demonstrates the vulnerability with multiple examples showing private vs non-private programs. The impact is well-defined - disclosure of private programs. This is a classic information disclosure vulnerability where authorization checks are missing at the GraphQL field level rather than just the object level. The fact that sensitive program configuration details leak through an unauthenticated API endpoint is a significant security issue for the platform.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hi team. And Happy New Year!
**Description:**
If I am not mistaken, then through this parameter we can define private programs with an external link.

If this parameter is not empty, then the program is private. - `["HackerOne Platform"]`
### Steps To Reproduce

https://hackerone.com/graphql
POST:


1){"query": "query {team(handle:\\"████████\\"){_id,report_sources}}"}
`{"data":{"team":{"_id":"██████████","report_sources":[]}}}` - not private program

2){"query": "query {team(handle:\\"███\\"){_id,report_sources}}"}
`{"data":{"team":{"_id":"█████","report_sources":["HackerOne Platform"]}}}` - `["HackerOne Platform"]` - private program

3){"query": "query {team(handle:\\"█████████\\"){_id,report_sources}}"}
`{"data":{"team":{"_id":"█████████","report_sources":["HackerOne Platform"]}}}` - `["HackerOne Platform"]` - private program

4){"query": "query {team(handle:\\"█████\\"){_id,report_sources}}"}
`{"data":{"team":{"_id":"███","report_sources":[]}}}` - not private program

Sorry i bad speak english
I hope you understand me
Thank you,haxta4ok00

## Impact

disclosed of private programs who have external link

</details>

---
*Analysed by Claude on 2026-05-24*
