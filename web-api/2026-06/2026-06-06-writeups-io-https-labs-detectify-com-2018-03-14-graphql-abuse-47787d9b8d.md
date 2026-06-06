# GraphQL Abuse and Information Disclosure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Unknown (Detectify Labs research)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Information Disclosure, Improper Access Control, API Abuse, Introspection Exposure
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints that expose introspection capabilities allow attackers to enumerate the entire API schema, including sensitive fields, mutations, and internal data structures. This information disclosure can be chained with other vulnerabilities to bypass authentication, access unauthorized data, or manipulate server state.

## Attack scenario (step by step)
1. Attacker identifies a GraphQL endpoint exposed on the target application (typically /graphql or /api/graphql)
2. Attacker sends an introspection query to enumerate the complete schema without authentication
3. Schema reveals sensitive fields, mutations, user objects, and internal API structure
4. Attacker crafts targeted queries based on discovered schema to access unauthorized data or sensitive fields
5. Attacker may discover and exploit mutations that lack proper authorization checks
6. Sensitive information is extracted or unauthorized state changes occur

## Root cause
GraphQL introspection is enabled by default in most implementations, allowing unauthenticated queries to reveal the full API schema. Developers often fail to disable introspection in production or implement proper access controls on sensitive fields and mutations.

## Attacker mindset
Modern API reconnaissance is automated and schema-driven. Rather than fuzzing endpoints, attackers leverage introspection to map attack surfaces with surgical precision. Exposed GraphQL schemas are goldmines for understanding backend logic and identifying weaknesses in authorization enforcement.

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict it to authenticated users only
- Implement field-level authorization checks rather than relying on endpoint-level controls
- Sanitize error messages to avoid leaking schema information in rejection responses
- Apply consistent authentication and authorization policies across all queries and mutations
- Monitor and alert on introspection queries as they indicate reconnaissance activity
- Use allowlisting for permitted queries when possible instead of blocklisting
- Implement rate limiting on GraphQL endpoints to prevent enumeration attacks

## Variant hunting
['Check for disabled introspection detection bypasses using aliases or query fragments', 'Test for incomplete field-level authorization on nested objects', 'Examine mutations for missing authorization checks on sensitive operations', 'Look for private fields accidentally exposed through federation or type extensions', 'Test batch query capabilities for authorization bypass opportunities', 'Identify subscription endpoints that may lack authentication requirements']

## MITRE ATT&CK
- T1190
- T1526
- T1087
- T1110
- T1040

## Notes
This foundational research highlighted how GraphQL's powerful introspection feature, designed for developer convenience, became a critical security risk when exposed without proper controls. The attack is particularly effective because it requires no special tools and provides complete architectural visibility.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
