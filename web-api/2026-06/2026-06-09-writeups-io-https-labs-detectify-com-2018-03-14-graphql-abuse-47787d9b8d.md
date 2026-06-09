# GraphQL Abuse: Information Disclosure and DoS Vulnerabilities

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Detectify Crowdsource
- **Bounty:** Undisclosed
- **Severity:** high
- **Vuln types:** Information Disclosure, Denial of Service, Introspection Abuse, Query Complexity Attack
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints can be abused through introspection queries and deeply nested queries to extract sensitive information and cause denial of service. Attackers can enumerate the entire API schema and craft complex queries that consume excessive server resources.

## Attack scenario (step by step)
1. Attacker identifies a GraphQL endpoint exposed on the target application
2. Attacker enables introspection queries to retrieve the complete API schema including all types, fields, and relationships
3. Attacker uses the schema information to map out sensitive data structures and relationships not intended for public access
4. Attacker crafts deeply nested or circular queries that cause exponential resource consumption
5. Attacker executes queries repeatedly, causing server resource exhaustion and application degradation
6. Legitimate users experience denial of service while attacker extracts sensitive information

## Root cause
GraphQL introspection was enabled in production without proper access controls, and insufficient query complexity validation allowed unbounded nested queries to execute unchecked

## Attacker mindset
Reconnaissance-focused attacker seeking to map API attack surface and discover exploitable data structures, combined with disruption-motivated attacker attempting to exhaust server resources through algorithmic complexity attacks

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict to authenticated users
- Implement query complexity analysis and depth limiting to prevent resource exhaustion
- Set strict timeouts and rate limiting on GraphQL queries
- Use allowlisting for approved queries when possible
- Implement persistent query mechanisms to prevent ad-hoc query execution
- Monitor for suspicious query patterns indicative of reconnaissance or DoS attempts
- Apply principle of least privilege to GraphQL schema exposure

## Variant hunting
Test for: (1) introspection query execution without authentication, (2) deeply nested query handling with arbitrary depth, (3) circular query references, (4) batch query processing without limits, (5) alias attacks, (6) fragment-based query expansion, (7) error message information disclosure, (8) mutation-based resource exhaustion

## MITRE ATT&CK
- T1526
- T1190
- T1213
- T1565

## Notes
GraphQL security requires paradigm shift from traditional REST API security; introspection abuse is a common reconnaissance vector in modern API assessments; query complexity attacks are GraphQL-specific DoS vectors that traditional WAF rules may not detect

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
