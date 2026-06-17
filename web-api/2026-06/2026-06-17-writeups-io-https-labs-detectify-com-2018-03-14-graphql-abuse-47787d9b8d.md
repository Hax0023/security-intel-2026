# GraphQL Abuse: Introspection and Information Disclosure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Not specified in provided content
- **Bounty:** Not specified in provided content
- **Severity:** Medium
- **Vuln types:** Information Disclosure, API Abuse, Introspection Exposure, Query Complexity Abuse
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints often expose introspection capabilities that allow attackers to enumerate the complete API schema, including available queries, mutations, and types. This information disclosure can be leveraged to discover sensitive operations and craft complex queries for Denial of Service attacks or unauthorized data access.

## Attack scenario (step by step)
1. Attacker identifies a GraphQL endpoint on the target application
2. Attacker sends an introspection query (e.g., __schema query) to enumerate all available operations
3. Attacker analyzes the returned schema to identify sensitive queries or mutations
4. Attacker crafts deeply nested or computationally expensive queries targeting discovered operations
5. Attacker executes complex queries to cause resource exhaustion or bypass rate limiting
6. Attacker uses schema knowledge to access sensitive data not otherwise discoverable

## Root cause
GraphQL introspection is enabled by default in many implementations, allowing unauthenticated or unauthorized users to query the API schema. Developers fail to disable introspection in production or implement proper access controls and query complexity limits.

## Attacker mindset
An attacker seeks to map the attack surface comprehensively before exploitation. By understanding the complete API structure through introspection, they can identify edge cases, hidden operations, and design efficient attacks without trial-and-error, significantly reducing detection risk.

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict it to authenticated users
- Implement query complexity analysis and depth limits to prevent DoS attacks
- Use rate limiting and query timeout mechanisms
- Monitor and log GraphQL introspection attempts and unusual query patterns
- Implement proper authentication and authorization on sensitive GraphQL operations
- Sanitize error messages to avoid leaking schema or data structure information
- Use allowlisting for permitted queries when possible

## Variant hunting
['Test for __schema, __type, and introspection query bypasses using aliases or fragments', 'Look for alternative GraphQL endpoints (e.g., /api/graphql, /graphql, /v1/graphql)', 'Check for introspection enabled on different HTTP methods (POST, GET, OPTIONS)', 'Test for schema stitching or federation vulnerabilities that expose internal schemas', 'Hunt for query complexity abuse combined with recursive queries or batch operations', 'Investigate schema directives that may enable additional abuse vectors']

## MITRE ATT&CK
- T1190
- T1526
- T1592
- T1613
- T1565

## Notes
This is a foundational GraphQL security issue affecting numerous SaaS and web applications. The article was published in 2018, making it a seminal work in GraphQL security awareness. GraphQL introspection abuse has become a standard reconnaissance technique in API security assessments and bug bounty programs.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
