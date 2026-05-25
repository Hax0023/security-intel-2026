# GraphQL Abuse - Information Disclosure and Query Introspection Exploitation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Detectify Crowdsource
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Information Disclosure, Introspection Exposure, Excessive Data Exposure, Lack of Rate Limiting, Inadequate Access Controls
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints with enabled introspection queries expose sensitive schema information and business logic, allowing attackers to map the entire API surface and extract unauthorized data. The vulnerability stems from default GraphQL configurations that permit introspection without authentication or authorization checks, combined with weak rate limiting and field-level access control.

## Attack scenario (step by step)
1. Attacker sends introspection query to GraphQL endpoint to enumerate available types, fields, and queries
2. Attacker discovers sensitive data types and fields not intended for public access (e.g., admin operations, user data)
3. Attacker crafts custom GraphQL queries to extract unauthorized information by leveraging discovered fields
4. Attacker performs brute-force or recursive queries to enumerate related objects and relationships
5. Attacker exploits lack of rate limiting to perform large-scale data extraction without detection
6. Attacker combines exposed schema information with business logic flaws to access restricted resources or operations

## Root cause
GraphQL introspection enabled by default without authentication requirements, insufficient query complexity validation, missing field-level authorization checks, and inadequate rate limiting on GraphQL endpoints allowing unrestricted query execution

## Attacker mindset
Reconnaissance-focused approach: leverage introspection to map the complete API surface without triggering alerts, then use discovered endpoints to systematically extract sensitive data. Prioritize discovering unintended public fields and relationships that may bypass authorization logic.

## Defensive takeaways
- Disable GraphQL introspection in production or restrict it to authenticated users with appropriate roles
- Implement strict field-level authorization to ensure sensitive data is inaccessible regardless of query construction
- Deploy query complexity analysis and depth limits to prevent expensive recursive queries
- Apply rate limiting and throttling specific to GraphQL endpoints, tracking by user and query cost
- Validate and sanitize all GraphQL queries; implement allowlist-based query validation when possible
- Separate public and internal GraphQL schemas; expose only necessary fields to unauthenticated clients
- Monitor and log all introspection attempts and unusual query patterns for anomaly detection
- Conduct regular security audits of schema design and access control policies

## Variant hunting
['Test for introspection on internal/staging GraphQL endpoints exposed to internet', 'Check for alias-based query expansion allowing bypassing of rate limits', 'Attempt batched queries to extract multiple data types in single request', 'Search for GraphQL endpoints on alternative paths: /graphql, /api/graphql, /query, /gql', 'Test for mutations that lack proper authorization (state-changing operations)', 'Probe for field suggestions/autocomplete leaking schema information', 'Investigate fragment abuse and persisted query mechanisms for information leakage', 'Look for excessive data returned in error messages exposing schema details']

## MITRE ATT&CK
- T1190
- T1526
- T1592
- T1087
- T1213

## Notes
GraphQL has become a critical attack surface due to its powerful introspection capabilities and complex query language. Organizations often overlook GraphQL security during API design because introspection is enabled by default. This vulnerability is particularly dangerous because it provides attackers with a detailed roadmap of data structures and relationships without requiring authentication, enabling sophisticated follow-up attacks. The writeup emphasizes the importance of treating GraphQL endpoints with the same security rigor as REST APIs.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
