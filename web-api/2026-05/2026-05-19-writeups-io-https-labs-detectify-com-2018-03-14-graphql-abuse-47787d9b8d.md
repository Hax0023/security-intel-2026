# GraphQL Abuse and Security Vulnerabilities

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Detectify Crowdsource
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln types:** Information Disclosure, Introspection Abuse, Query Complexity Attacks, Denial of Service, Unauthorized Data Access
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints can be abused through introspection queries and malicious query construction to extract sensitive data, enumerate schema structures, and launch denial-of-service attacks. Unprotected GraphQL implementations expose internal API structures and data models, allowing attackers to craft targeted queries that bypass business logic controls.

## Attack scenario (step by step)
1. Attacker discovers GraphQL endpoint through reconnaissance or common paths (/graphql, /api/graphql, /query)
2. Attacker executes introspection query to fully enumerate the schema, data types, fields, and relationships
3. Attacker analyzes schema to identify sensitive data fields and authentication weaknesses
4. Attacker crafts deeply nested or computationally expensive queries to cause resource exhaustion
5. Attacker uses exposed schema knowledge to perform targeted data extraction queries bypassing UI controls
6. Attacker exfiltrates sensitive information or triggers DoS conditions without proper rate limiting

## Root cause
GraphQL endpoints are deployed without proper security controls including: disabled or unrestricted introspection queries, lack of query complexity analysis, missing rate limiting, insufficient authentication/authorization on resolvers, and absence of query depth limits. Default configurations often expose full schema details publicly.

## Attacker mindset
GraphQL abuse represents a paradigm shift from REST API attacks. Attackers recognize that introspection provides complete API documentation automatically, eliminating reconnaissance time. The query language's flexibility allows construction of surgical, efficient attacks that extract maximum data with minimal requests. Schema enumeration immediately reveals data relationships and sensitive fields developers may have assumed were protected.

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict to authenticated users only
- Implement query complexity analysis and depth limits to prevent expensive traversals
- Enforce strict rate limiting per user/IP on GraphQL endpoints
- Apply authorization checks at field resolver level, not just at query entry point
- Monitor and log GraphQL queries for anomalous patterns (deeply nested queries, repeated introspection attempts)
- Validate and sanitize all GraphQL input parameters
- Never expose internal schema details through error messages
- Use allow-lists for approved queries in sensitive contexts
- Implement timeout mechanisms for long-running queries
- Separate public and private GraphQL endpoints with different security policies

## Variant hunting
['Test introspection via __schema and __type queries on suspected GraphQL endpoints', 'Attempt alias abuse to bypass rate limiting on queries', 'Chain multiple queries to cause N+1 query problems and resource exhaustion', 'Search for mutations that trigger unvalidated side effects', 'Test batch queries to process multiple requests as single operation', 'Probe for overfetching vulnerabilities where sensitive adjacent data is accessible', 'Enumerate hidden mutations through schema introspection', 'Test subscription endpoints for similar abuse patterns']

## MITRE ATT&CK
- T1190
- T1526
- T1592
- T1538
- T1541
- T1006

## Notes
GraphQL has become increasingly attractive to attackers due to its powerful introspection capabilities and flexible query language. Unlike REST APIs with fixed endpoints, GraphQL's single endpoint and schema-driven design centralizes the API surface but also concentrates risk if poorly secured. The Detectify Crowdsource platform highlights this as a common vulnerability pattern across modern web applications. Organizations adopting GraphQL must treat schema exposure with same severity as database credential leakage.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
