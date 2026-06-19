# GraphQL Abuse - Authentication and Information Disclosure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Detectify Crowdsource
- **Bounty:** Variable (Crowdsource program)
- **Severity:** High
- **Vuln types:** Information Disclosure, Authentication Bypass, Broken Access Control, Insufficient Rate Limiting
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints can be abused to bypass authentication mechanisms and disclose sensitive information that should be restricted. Attackers can craft queries to access protected data and user information without proper authorization, exploiting weak or missing access controls on GraphQL resolvers.

## Attack scenario (step by step)
1. Attacker identifies a GraphQL endpoint exposed on the target application
2. Attacker performs introspection queries to discover schema, types, and available fields without authentication
3. Attacker crafts queries to request sensitive fields (user data, emails, IDs) across multiple users
4. Attacker bypasses authorization checks by directly querying protected resources through GraphQL mutations or nested queries
5. Attacker exploits missing rate limiting to perform enumeration attacks or batch extract large datasets
6. Attacker obtains sensitive information or escalates privileges through data access not available via normal UI

## Root cause
GraphQL endpoints often lack proper field-level access controls and authentication validation. Developers may assume authorization inherited from REST API layer applies uniformly, fail to implement per-resolver auth checks, or leave introspection enabled in production. Missing rate limiting on GraphQL queries enables brute-force and enumeration attacks.

## Attacker mindset
GraphQL is attractive because it provides a single endpoint for data queries with powerful introspection capabilities. An attacker views this as an opportunity to discover the full API surface, bypass coarse-grained access controls, and extract data through creative query construction that bypasses UI-level restrictions.

## Defensive takeaways
- Disable GraphQL introspection in production environments
- Implement field-level authorization checks in every resolver, not just at the endpoint level
- Apply consistent authentication validation across all GraphQL queries and mutations
- Implement rate limiting and query complexity analysis to prevent enumeration and DoS attacks
- Validate and sanitize all GraphQL inputs to prevent injection attacks
- Use allowlisting for permitted queries in sensitive applications
- Audit GraphQL schema for unintended exposure of sensitive fields or relationships
- Log and monitor unusual GraphQL query patterns and introspection attempts

## Variant hunting
['Search for GraphQL endpoints with enabled introspection queries', 'Test for bypass of authentication on mutations and nested query fields', 'Enumerate user data across multiple users via batch queries', 'Attempt to access deleted or archived data through GraphQL', 'Test for NoSQL injection and SQL injection in GraphQL arguments', 'Check for information disclosure in error messages from GraphQL resolvers', 'Look for GraphQL endpoints accepting queries without CSRF tokens', 'Test query complexity and cost analysis implementation gaps']

## MITRE ATT&CK
- T1190
- T1526
- T1087
- T1059
- T1040
- T1557

## Notes
GraphQL security was relatively immature when this writeup was published in 2018. The attack surface of GraphQL applications often exceeds REST APIs due to the flexibility and power of query language. Organizations adopting GraphQL frequently overlook security implications of introspection, batching, and complex nested queries. This vulnerability class continues to be relevant as GraphQL adoption grows.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
