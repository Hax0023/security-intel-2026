# GraphQL Abuse and Information Disclosure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Unknown (Detectify Labs research)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Information Disclosure, Introspection Attack, API Abuse, Unauthorized Data Access
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints often expose sensitive schema information through introspection queries, allowing attackers to enumerate available types, fields, and operations. This reconnaissance capability can lead to discovery of undocumented or internal API endpoints that leak sensitive data or enable unauthorized operations.

## Attack scenario (step by step)
1. Attacker identifies a GraphQL endpoint on the target application (typically /graphql or similar)
2. Attacker sends an introspection query to enumerate the entire GraphQL schema without authentication
3. Schema inspection reveals internal fields, mutations, or types not intended for public use
4. Attacker crafts targeted queries to extract sensitive data (user information, API keys, etc.) from exposed fields
5. Attacker discovers and abuses internal mutations to modify data or perform unauthorized operations
6. Information gathered enables lateral movement or privilege escalation within the application

## Root cause
GraphQL introspection is enabled by default and lacks proper access controls, exposing the complete API schema and implementation details to unauthenticated users

## Attacker mindset
An attacker recognizes that GraphQL's self-documenting nature is a double-edged sword—while developers appreciate schema introspection for legitimate API consumption, it becomes a reconnaissance goldmine. By querying the schema directly, attackers bypass traditional API documentation and discover hidden or internal endpoints that developers may have forgotten to secure or intended as private.

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict it to authenticated users
- Implement authentication and authorization checks for introspection queries
- Use field-level permissions to prevent exposure of sensitive types and fields
- Audit GraphQL schema regularly for unintended public fields or mutations
- Monitor introspection query patterns for reconnaissance activity
- Document and remove deprecated or internal APIs from the schema
- Implement rate limiting and query complexity analysis to prevent abuse
- Use security-first schema design principles; avoid exposing internal implementation details

## Variant hunting
['Test for aliased introspection queries (__schema wrapped in aliases)', 'Check if introspection is blocked via query name but accessible via aliases or fragments', 'Identify information disclosure through error messages revealing schema structure', 'Hunt for deprecated fields or hidden mutations not advertised in documentation', 'Test for partial introspection restrictions (some queries allowed, others blocked)', 'Look for GraphQL batching that bypasses single-query rate limits', 'Search for federation endpoints that expose upstream schema details']

## MITRE ATT&CK
- T1526
- T1592
- T1589
- T1591
- T1613

## Notes
This is foundational research from Detectify Labs on GraphQL security. The writeup addresses a common misconfiguration affecting modern APIs. GraphQL's introspection feature, while developer-friendly, represents a significant reconnaissance vector. The research likely introduced many security practitioners to GraphQL-specific attack vectors during the 2018 timeframe when GraphQL adoption was rapidly increasing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
