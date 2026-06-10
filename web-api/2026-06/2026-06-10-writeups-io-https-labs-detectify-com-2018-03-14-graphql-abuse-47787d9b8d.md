# GraphQL Abuse and Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Detectify Crowdsource
- **Bounty:** Varies (Crowdsource program dependent)
- **Severity:** High
- **Vuln types:** Information Disclosure, Denial of Service, Authorization Bypass, Introspection Abuse
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints can be abused through introspection queries to extract sensitive schema information and API structure without authentication. Attackers can leverage this to craft targeted queries causing resource exhaustion or accessing unauthorized data.

## Attack scenario (step by step)
1. Attacker identifies GraphQL endpoint on target application
2. Attacker queries __schema introspection to map entire API structure and available operations
3. Attacker analyzes schema to identify sensitive fields and queries lacking proper authorization checks
4. Attacker constructs deeply nested or recursive queries to cause Denial of Service
5. Attacker bypasses rate limiting or authentication to access sensitive data through unprotected queries
6. Attacker exfiltrates data or triggers resource exhaustion on backend systems

## Root cause
Improper GraphQL security configuration including: enabled introspection in production, missing field-level authorization checks, lack of query complexity analysis, insufficient rate limiting, and inadequate input validation on GraphQL queries

## Attacker mindset
GraphQL presents an attractive target because it exposes complete API surface through introspection, provides flexible query language for crafting attacks, often less protected than REST endpoints, and enables batch operations for amplified impact

## Defensive takeaways
- Disable introspection queries in production environments
- Implement field-level authorization and validation on all GraphQL queries
- Add query complexity analysis and depth limiting to prevent resource exhaustion
- Enforce strict rate limiting and query throttling
- Sanitize and validate all input parameters
- Monitor and log suspicious GraphQL query patterns
- Use allowlisting for permitted queries when possible
- Implement timeout mechanisms for long-running queries

## Variant hunting
Search for: GraphQL introspection exposure, N+1 query vulnerabilities, recursive query attacks, batch query DOS, unauthorized data access through GraphQL aliases, batching attacks combining multiple queries, fragment spread vulnerabilities, circular schema traversal

## MITRE ATT&CK
- T1190
- T1526
- T1566
- T1592
- T1040
- T1083

## Notes
GraphQL abuse is particularly dangerous because it centralizes API access and exposes comprehensive schema information by design. Many developers treat GraphQL as inherently secure without implementing API-level security controls. Introspection should be treated as sensitive as schema documentation and protected accordingly.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
