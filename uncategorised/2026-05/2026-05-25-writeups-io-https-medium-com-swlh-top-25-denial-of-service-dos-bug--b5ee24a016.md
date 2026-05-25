# Top 25 Denial-of-Service (DoS) Bug Bounty Reports

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Multiple (General Bug Bounty Programs)
- **Bounty:** Varies by program and severity
- **Severity:** high
- **Vuln types:** Denial of Service, Application-layer DoS, Resource Exhaustion, Input Validation
- **Category:** uncategorised
- **Writeup:** https://medium.com/swlh/top-25-denial-of-service-dos-bug-bounty-reports-4aaeb4e9a052

## Summary
This article is an educational writeup categorizing and discussing 25 disclosed Denial-of-Service vulnerabilities found across various bug bounty programs. It covers different DoS attack vectors including volume-based, protocol-based, and application-layer attacks, with emphasis on discovering DoS flaws in web applications.

## Attack scenario (step by step)
1. Attacker identifies application endpoints that accept user input (forms, files, parameters)
2. Attacker sends oversized payloads or resource-intensive requests to exhaust server resources
3. Application fails to implement proper input validation or rate limiting controls
4. Server becomes overwhelmed and unresponsive to legitimate user requests
5. Application availability is degraded or completely denied to end users
6. Attacker can repeat attack at scale using automated tools or distributed methods

## Root cause
Applications lack sufficient input validation, rate limiting, resource throttling, and timeout mechanisms to prevent abuse of computational resources through crafted requests or oversized inputs.

## Attacker mindset
Attackers seek to find quick wins by identifying resource-intensive operations (file uploads, complex queries, large data processing) that lack proper safeguards, allowing them to impact service availability with minimal effort.

## Defensive takeaways
- Implement strict input validation and size limits on all user-supplied data
- Deploy rate limiting and request throttling mechanisms
- Set appropriate timeouts for resource-intensive operations
- Monitor and alert on abnormal resource consumption patterns
- Use WAF rules to detect and block DoS patterns
- Implement load balancing and auto-scaling for traffic spikes
- Conduct application stress testing to identify bottlenecks
- Enforce quotas on API endpoints and user actions

## Variant hunting
Search for: algorithmic complexity attacks (ReDoS), ZIP bombs/decompression attacks, billion laughs XML attacks, hash collision attacks, cache poisoning, infinite loops in request processing, unbounded recursion, memory leaks in request handlers, slow SQL queries triggered by user input, file processing with no size limits.

## MITRE ATT&CK
- T1499
- T1499.001
- T1499.002
- T1499.003
- T1499.004

## Notes
This is a curated list/educational resource rather than a single vulnerability disclosure. The article serves as a taxonomy and learning resource for bug bounty hunters. Actual severity and bounty amounts vary significantly depending on program scope, business impact, and whether the target accepts DoS reports.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
