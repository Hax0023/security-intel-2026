# GraphQL Abuse and Security Misconfiguration

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Detectify Bug Bounty Program
- **Bounty:** Not specified in provided content
- **Severity:** HIGH
- **Vuln types:** Information Disclosure, Insufficient Access Control, API Misuse, Query Complexity Attack, Introspection Exposure
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints frequently expose sensitive data through introspection queries and lack proper rate limiting or complexity analysis, allowing attackers to enumerate schema details and extract unauthorized information. Misconfigured GraphQL implementations enable denial of service attacks through deeply nested queries and unauthorized access to protected resources due to inadequate permission validation.

## Attack scenario (step by step)
1. Attacker discovers GraphQL endpoint (typically /graphql, /api/graphql, or /query)
2. Attacker enables introspection query to enumerate complete schema, field names, types, and available operations
3. Attacker identifies sensitive fields or objects lacking proper authorization checks
4. Attacker crafts malicious queries to extract sensitive data or performs deeply nested queries to consume resources
5. Attacker exploits lack of rate limiting to perform reconnaissance or denial of service attacks
6. Attacker leverages permission bypass to access data intended for other user roles or organizations

## Root cause
GraphQL implementations deployed with introspection enabled in production, insufficient query complexity analysis, lack of rate limiting, inadequate permission validation at field/resolver level, and default permissive configurations

## Attacker mindset
GraphQL presents an attractive target because it provides a machine-readable schema (via introspection) that maps the entire attack surface, eliminates guesswork in API enumeration, and often ships with minimal security controls compared to REST APIs. Attackers view this as low-hanging fruit for data extraction and reconnaissance.

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict it to authenticated users
- Implement query complexity analysis and depth limiting to prevent resource exhaustion attacks
- Enforce rate limiting and request throttling on GraphQL endpoints
- Validate authorization at the resolver/field level, not just at the query level
- Implement proper authentication and session management for all GraphQL operations
- Monitor and log GraphQL queries for anomalous patterns and large data extraction
- Use allowlisting for permitted queries in sensitive environments
- Implement timeout policies for long-running queries
- Sanitize error messages to avoid information leakage
- Regularly audit GraphQL schema and resolver implementations for permission gaps

## Variant hunting
['Search for publicly exposed GraphQL endpoints by probing common paths (/graphql, /api/graphql, /query, /g, /__graphql)', 'Test introspection on discovered endpoints using __schema queries', 'Analyze schema for sensitive field names (password, token, email, ssn, api_key)', 'Fuzz query complexity with deeply nested queries and large batch requests', "Test cross-user data access by querying other users' IDs in pagination arguments", 'Check for mutation abuse (mass operations, privilege escalation via mutations)', 'Examine fragment parsing and alias abuse for query obfuscation and bypasses', 'Test batch query processing for race conditions and state manipulation']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Scan Infrastructure
- T1087 - Account Discovery
- T1592 - Gather Victim Identity Information
- T1213 - Data from Information Repositories
- T1040 - Network Sniffing
- T1566 - Phishing (via enumerated data for social engineering)
- T1498 - Network Denial of Service

## Notes
GraphQL security is often overlooked because developers focus on business logic rather than API-level controls. The standard GraphQL implementations ship with developer-friendly defaults (like introspection) that create significant security debt. This vulnerability class has become increasingly common as GraphQL adoption grows without corresponding security maturity.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
