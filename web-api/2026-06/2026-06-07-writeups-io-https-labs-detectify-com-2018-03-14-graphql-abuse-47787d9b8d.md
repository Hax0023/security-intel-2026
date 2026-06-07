# GraphQL Abuse and Security Misconfigurations

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Detectify Crowdsource
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln types:** Information Disclosure, Improper Access Control, API Abuse, Introspection Exposure
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints often expose introspection capabilities and lack proper access controls, allowing attackers to enumerate API schemas and abuse queries to extract sensitive data. Misconfigurations in GraphQL implementations frequently enable unauthorized access to protected resources and information disclosure at scale.

## Attack scenario (step by step)
1. Attacker identifies GraphQL endpoint through standard discovery techniques (e.g., /graphql, /api/graphql)
2. Attacker enables introspection queries to map complete API schema and available fields
3. Attacker identifies sensitive data fields lacking proper authorization checks
4. Attacker crafts queries combining multiple fields to extract protected information
5. Attacker automates data extraction using GraphQL aliases and batched queries
6. Sensitive data is exfiltrated without triggering typical rate-limiting or access controls

## Root cause
GraphQL introspection enabled in production environments, insufficient field-level authorization, lack of rate limiting on API queries, and default configurations exposing schema details without authentication requirements

## Attacker mindset
Reconnaissance-focused; GraphQL provides superior mapping capability compared to REST APIs. Attackers leverage introspection as a reconnaissance tool to identify all available data fields, then systematically bypass access controls through query complexity and batching techniques.

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict to authenticated users
- Implement field-level authorization checks, not just resolver-level validation
- Enforce rate limiting and query complexity analysis on GraphQL endpoints
- Monitor for suspicious query patterns (large batches, introspection attempts, field enumeration)
- Apply principle of least privilege - only expose necessary fields and avoid exposing internal type definitions
- Implement query depth limiting to prevent expensive nested queries
- Log and alert on introspection query attempts
- Separate public and authenticated GraphQL endpoints with different schemas

## Variant hunting
['Check for aliasing abuse enabling request multiplexing to bypass rate limits', 'Test batch query operations for cumulative data extraction', 'Identify fields with missing authorization decorators/middleware', 'Look for circular query references enabling infinite recursion DoS', 'Test for IDOR vulnerabilities within query parameters (e.g., arbitrary user ID queries)', 'Examine federation/gateway setups for schema stitching bypass opportunities', 'Search for debug/admin-only fields inadvertently exposed in production schema']

## MITRE ATT&CK
- T1190
- T1526
- T1087
- T1550
- T1566

## Notes
GraphQL abuse has become a critical attack vector for API reconnaissance. Unlike REST APIs with explicit endpoint enumeration, GraphQL introspection provides a machine-readable schema that perfectly maps the entire attack surface. The combination of introspection + weak authorization is particularly dangerous. Organizations often overlook GraphQL security as they focus on REST API hardening. Consider GraphQL as a distinct security domain requiring specialized testing and monitoring approaches.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
