# GraphQL API Abuse and Information Disclosure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Detectify Crowdsource
- **Bounty:** Not specified in content
- **Severity:** High
- **Vuln types:** Information Disclosure, API Abuse, Insufficient Access Controls, Introspection Exposure
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints were vulnerable to schema introspection attacks allowing attackers to enumerate the entire API structure, including sensitive fields and operations. Lack of proper access controls on GraphQL queries enabled unauthorized data access and information disclosure through graph traversal.

## Attack scenario (step by step)
1. Attacker discovers a GraphQL endpoint exposed on the target application
2. Attacker executes introspection queries to map the entire GraphQL schema without authentication
3. Schema mapping reveals sensitive data fields, user objects, and administrative operations
4. Attacker crafts targeted queries to access sensitive information bypassing business logic
5. Attacker traverses object relationships to extract related sensitive data across the API
6. Attacker identifies and abuses operations that lack proper authorization checks

## Root cause
GraphQL introspection enabled by default without authentication requirements, combined with missing field-level authorization checks and inadequate query complexity validation

## Attacker mindset
Methodical API reconnaissance to identify data exposure opportunities; leveraging GraphQL's self-documenting nature to map attack surface without traditional scanning; exploiting design assumption that API complexity provides security

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict to authenticated users only
- Implement field-level authorization checks independent of query selection
- Enforce query complexity limits and depth restrictions to prevent abuse
- Apply rate limiting and monitoring to GraphQL endpoints
- Validate and sanitize all user inputs in GraphQL queries
- Use allowlisting for permitted queries in high-security contexts
- Regular security audits of GraphQL schema and resolver implementations

## Variant hunting
Search for exposed GraphQL endpoints via directives like @auth, @deprecated without validation; test for alias abuse to bypass rate limits; probe for batch query execution without throttling; examine subscription endpoints for authentication gaps; fuzz query depth/breadth parameters

## MITRE ATT&CK
- T1190
- T1526
- T1592
- T1589
- T1592.004

## Notes
GraphQL's introspection feature is powerful for developers but creates significant security risks when exposed. Many organizations underestimate GraphQL attack surface compared to REST APIs. The vulnerability demonstrates importance of treating API security holistically rather than assuming complexity = security. Detectify Crowdsource program highlights real-world GraphQL exposure patterns across organizations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
