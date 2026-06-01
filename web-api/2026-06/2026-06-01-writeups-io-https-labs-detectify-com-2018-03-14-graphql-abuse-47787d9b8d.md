# GraphQL Abuse and Information Disclosure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Unknown - Detectify Labs Research
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Information Disclosure, Introspection Abuse, API Enumeration, Unauthorized Data Access
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints often expose their entire schema through introspection queries, allowing attackers to enumerate all available data types, fields, and operations without authentication. By abusing GraphQL introspection, attackers can discover sensitive fields and construct targeted queries to extract confidential information such as user data, internal records, and business intelligence.

## Attack scenario (step by step)
1. Attacker identifies a GraphQL endpoint exposed on the target application
2. Attacker sends an introspection query to retrieve the complete GraphQL schema definition
3. The schema reveals sensitive data types, fields, and operations including hidden or internal endpoints
4. Attacker constructs custom GraphQL queries targeting sensitive fields discovered in the schema
5. Attacker bypasses authorization checks by directly querying sensitive data (e.g., user profiles, financial records)
6. Attacker exfiltrates large volumes of data through batch queries or aliases

## Root cause
GraphQL introspection enabled by default without proper access controls, combined with insufficient field-level authorization checks allowing authenticated or unauthenticated users to query sensitive data

## Attacker mindset
An attacker seeks to enumerate the complete attack surface of an API to identify data exposure opportunities. GraphQL's introspection feature is a goldmine for reconnaissance, providing a roadmap of all available data and operations in a single query without traditional fuzzing.

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict it to authenticated, authorized users only
- Implement field-level authorization and validate all data access requests against user permissions
- Apply rate limiting and query complexity analysis to prevent large batch queries and denial of service
- Sanitize error messages to avoid leaking schema structure or sensitive information in responses
- Regularly audit exposed GraphQL schemas for unintended sensitive fields or internal operations
- Implement query depth and breadth limits to prevent information gathering attacks
- Use GraphQL security middleware and Web Application Firewalls configured for API abuse patterns

## Variant hunting
['Query for GraphQL endpoints via common paths: /graphql, /api/graphql, /v1/graphql, /.well-known/graphql', 'Test introspection with various query formats: __schema, __type, IntrospectionQuery', 'Attempt alias abuse to bypass rate limiting while extracting large datasets', 'Query mutations to identify unsafe operations (account takeover, data modification)', 'Fuzz GraphQL fields to discover hidden, deprecated, or internal operations', 'Test authorization bypass via query fragments, variables, and directives', 'Enumerate user/customer data through connection fields with pagination']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Reconnaissance
- T1087 - Account Discovery
- T1580 - Cloud Infrastructure Discovery
- T1538 - Cloud Service Discovery
- T1592 - Gather Victim Identity Information

## Notes
Detectify Labs published this research in 2018 when GraphQL security awareness was limited. GraphQL introspection abuse remains a critical issue in modern applications. The research likely demonstrated practical exploitation of real-world endpoints with inadequate access controls. This vulnerability class requires API-specific security practices distinct from traditional REST API security models.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
