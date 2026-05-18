# GraphQL Abuse and Security Risks

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Unknown (Detectify Labs Research)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Information Disclosure, Denial of Service, Introspection Exploitation, Query Complexity Attacks, Batch Query Attacks
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints can be abused through introspection queries to enumerate the entire schema and discover sensitive fields, combined with complexity-based denial of service attacks. Attackers can craft deeply nested or resource-intensive queries to exhaust server resources without proper rate limiting or query complexity analysis.

## Attack scenario (step by step)
1. Attacker identifies a GraphQL endpoint exposed on the target application
2. Attacker executes introspection query to extract full schema definition including all fields and types
3. Attacker maps out sensitive data fields that should not be publicly accessible
4. Attacker crafts deeply nested or circular queries designed to consume excessive computational resources
5. Attacker launches batched query attacks or algorithmic complexity exploits to cause denial of service
6. Server becomes unresponsive or crashes due to resource exhaustion without proper query validation

## Root cause
GraphQL implementations often enable introspection by default without authentication, lack query complexity analysis, absence of depth limits on nested queries, and insufficient rate limiting on query execution. Developers may not implement authorization checks per field and trust client-side query validation.

## Attacker mindset
An attacker seeks to enumerate application capabilities and data structures without authentication, then leverage that knowledge to craft efficient denial of service attacks or extract sensitive information through authorized but excessive queries.

## Defensive takeaways
- Disable GraphQL introspection in production environments or restrict it to authenticated users only
- Implement query complexity analysis and cost estimation before execution
- Enforce maximum query depth limits to prevent nested query exploitation
- Implement rate limiting and throttling per user/IP address
- Apply field-level authorization checks, not just operation-level checks
- Monitor and log suspicious query patterns and complexity anomalies
- Implement timeout mechanisms for long-running queries
- Use allowlisting for critical production GraphQL queries when feasible

## Variant hunting
Search for: other schema introspection endpoints, GraphQL APIs on subdomain enumeration, batched query endpoints, subscription endpoints with unbounded depth, file upload mutations combined with query complexity, mutations that trigger expensive operations, cached queries that bypass complexity limits

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1526: Enumerate External Remote Services
- T1087: Account Discovery
- T1526: Enumerate External Remote Services
- T1498: Network Denial of Service

## Notes
This is a seminal research article on GraphQL security from 2018. The Detectify article discusses fundamental GraphQL attack vectors that remain relevant. Many organizations have since addressed introspection, but query complexity attacks continue to be undermitigated. GraphQL-specific security tools and WAF rules have improved but require proper configuration.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
