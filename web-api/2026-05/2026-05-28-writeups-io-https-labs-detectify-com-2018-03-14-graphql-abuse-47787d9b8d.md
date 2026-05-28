# GraphQL Abuse - Query Complexity and DoS Vulnerabilities

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Detectify Crowdsource
- **Bounty:** Unknown
- **Severity:** High
- **Vuln types:** Denial of Service, Resource Exhaustion, Query Complexity Attack, Insufficient Rate Limiting, Information Disclosure
- **Category:** web-api
- **Writeup:** https://labs.detectify.com/2018/03/14/graphql-abuse/

## Summary
GraphQL endpoints are vulnerable to abuse through maliciously crafted queries that exploit insufficient complexity validation and rate limiting. Attackers can construct deeply nested or resource-intensive queries to exhaust server resources, causing denial of service conditions. The lack of proper query cost analysis allows attackers to bypass traditional security controls.

## Attack scenario (step by step)
1. Attacker identifies a GraphQL endpoint exposed by the target application
2. Attacker crafts a deeply nested query leveraging recursive field relationships to amplify computational cost
3. Attacker submits the malicious query without triggering standard request-based rate limits due to single large payload
4. GraphQL resolver attempts to execute the complex query, consuming excessive CPU, memory, and database resources
5. Server resources become exhausted, causing performance degradation or complete service unavailability
6. Legitimate users experience denial of service while attacker remains undetected due to low request volume

## Root cause
GraphQL implementations lack adequate query complexity analysis, cost calculation, and execution depth limiting. Default configurations do not enforce per-query resource budgets or timeout mechanisms, allowing unrestricted execution of expensive operations.

## Attacker mindset
Attackers recognize GraphQL's powerful query language as an unexploited attack surface compared to traditional REST APIs. They understand that bypassing request-based rate limits through single complex payloads provides a stealthier DoS vector with higher impact-to-request ratio.

## Defensive takeaways
- Implement query complexity scoring and cost analysis before execution
- Enforce maximum query depth and field selection limits
- Set per-query execution timeouts and resource quotas
- Implement rate limiting based on query complexity, not just request count
- Monitor for unusual query patterns and nested field access
- Use query whitelisting for critical GraphQL operations
- Implement proper error handling to avoid information leakage about schema
- Conduct regular security audits of GraphQL schema and resolver implementations

## Variant hunting
['Alias-based query expansion (using multiple aliases for same field to bypass limits)', 'Fragment spread exploitation (recursive fragments to amplify query size)', 'Batched query attacks (multiple queries in single request)', 'Introspection query abuse for information gathering before targeted attack', 'Mutation-based resource exhaustion attacks', 'Connection-based pagination attacks (requesting maximum page sizes repeatedly)']

## MITRE ATT&CK
- T1190
- T1499
- T1526

## Notes
GraphQL abuse represents a paradigm shift in API-based DoS attacks, requiring security teams to move beyond traditional rate limiting to implement query-aware defenses. Organizations should treat GraphQL security as critical infrastructure hardening rather than optional enhancement.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
