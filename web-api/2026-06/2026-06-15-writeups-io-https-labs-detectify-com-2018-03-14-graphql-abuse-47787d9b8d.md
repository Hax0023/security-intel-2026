# GraphQL Abuse and Exploitation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Unknown (Detectify Labs Research)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Improper Input Validation, Information Disclosure, Denial of Service, Abuse of Functionality
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
This research demonstrates common abuse patterns and security misconfigurations in GraphQL APIs that expose sensitive information and enable denial of service attacks. The vulnerability stems from insufficient input validation, overly permissive query complexity, and lack of proper access controls on GraphQL endpoints.

## Attack scenario (step by step)
1. Attacker discovers a GraphQL endpoint through reconnaissance (e.g., /graphql, /api/graphql)
2. Attacker sends introspection queries to enumerate all available schema, types, and fields without authentication
3. Attacker identifies sensitive data fields and constructs queries to extract information (user data, internal system details)
4. Attacker crafts deeply nested or circular queries to cause excessive computational overhead
5. Server processes resource-intensive queries leading to CPU exhaustion and service degradation
6. Attacker bypasses access controls by querying protected resources through parent-child relationships

## Root cause
GraphQL implementations frequently lack proper security controls including: disabled introspection in production, absence of query complexity analysis, missing rate limiting, inadequate authentication/authorization per field, and failure to validate query depth and breadth.

## Attacker mindset
An attacker views GraphQL as a powerful attack surface due to its flexibility and discoverability. The ability to request exactly what data is needed, combined with weak access controls, makes it an attractive target for reconnaissance, data exfiltration, and DoS attacks. The graphical nature of relationships allows attackers to traverse the schema discovering sensitive information.

## Defensive takeaways
- Disable GraphQL introspection in production environments
- Implement query complexity analysis and set limits on query depth, breadth, and execution time
- Apply rate limiting and throttling per IP/user/query type
- Enforce strong authentication and field-level authorization checks
- Validate and sanitize all user inputs; implement query cost analysis
- Use alias and directive restrictions to prevent exploitation
- Monitor and log GraphQL queries for anomalous patterns
- Implement timeouts on query execution
- Test GraphQL endpoint security as part of regular security assessments

## Variant hunting
Search for other GraphQL abuse techniques: batching attacks, alias attacks, fragment attacks, directive abuse, mutation-based DoS, N+1 query problems, and unauthorized batch field resolution.

## MITRE ATT&CK
- T1190
- T1526
- T1592
- T1589
- T1590
- T1498
- T1499

## Notes
GraphQL's powerful query language and introspection capabilities, while beneficial for legitimate use, create a unique attack surface that many developers fail to secure properly. This research highlights the importance of treating GraphQL endpoints with the same rigor as traditional APIs and understanding the specific threats posed by graph-based data querying.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
