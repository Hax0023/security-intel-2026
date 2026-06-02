# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Points.com (Bug Bounty - responsible disclosure)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Directory Traversal, Authorization Bypass, Credential Exposure, Broken Authentication, Insecure Direct Object References (IDOR), API Security Misconfiguration
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities were discovered in points.com, the backend provider for airline and hotel rewards programs, affecting 22 million customer records. Attackers could access sensitive PII, transfer loyalty points, and gain administrative access to the global rewards platform. All issues were patched within hours of responsible disclosure.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint on points.com infrastructure
2. Attacker enumerates and queries 22 million customer order records via the exposed internal API using pagination and sorting parameters
3. Attacker extracts customer surnames, rewards numbers, and partial credit card information from query results
4. Attacker uses extracted rewards number and surname to bypass authorization controls and generate full account tokens
5. Attacker uses forged tokens to transfer loyalty points to attacker-controlled accounts and access customer PII
6. Attacker discovers leaked tenant API credentials (macID/macKey) in client-side code or misconfigured endpoints and signs requests to impersonate Virgin Airlines

## Root cause
Multiple architectural and configuration failures: (1) Insufficient path traversal validation allowing access to internal APIs; (2) Authorization logic relying solely on non-secret customer attributes (surname + rewards number); (3) Credential management exposing API signing keys in client-accessible locations; (4) Lack of API authentication rate limiting and anomaly detection; (5) Absence of proper access controls between tenant applications and core platform APIs

## Attacker mindset
Opportunistic researcher with focus on high-impact targets in financial services sector. Demonstrates systematic vulnerability chaining (traversal → data extraction → auth bypass → privilege escalation). Responsible disclosure approach suggests ethical researcher rather than malicious actor, but attack chain shows intent to fully compromise platform if pursued maliciously.

## Defensive takeaways
- Implement strict input validation and path canonicalization to prevent directory traversal attacks
- Enforce multi-factor authentication for API access; never rely on customer-guessable attributes as authentication factors
- Implement role-based access control (RBAC) with principle of least privilege for all API endpoints
- Rotate and secure all API credentials; never embed secrets in client-side code or configuration files
- Implement request signing and validation for inter-service authentication with cryptographic verification
- Deploy API rate limiting, anomaly detection, and behavioral analysis to identify suspicious access patterns
- Conduct regular security audits of all tenant integrations and API surface areas
- Implement comprehensive logging and monitoring for account access, point transfers, and administrative actions
- Segment networks to limit lateral movement between customer data APIs and administrative consoles
- Establish incident response procedures for rapid remediation (points.com achieved <1 hour response time)

## Variant hunting
['Search for similar path traversal patterns in other API gateways or microservices using parameter fuzzing', 'Audit all APIs relying on customer PII combinations (email + DOB, phone + surname, etc.) as authentication factors', 'Enumerate all tenant credentials stored in web-accessible configuration files, error messages, or client-side JavaScript', 'Test for IDOR vulnerabilities in order IDs, transaction IDs, and account identifiers across all reward programs', 'Fuzz API endpoints with parameter tampering to bypass authorization checks (e.g., userId, accountId, programId)', 'Analyze JWT/token generation algorithms for predictability or weak signing mechanisms', 'Investigate other airline/hotel reward programs using shared backend infrastructure for similar misconfigurations', 'Test for broken access control in admin panels by enumerating program IDs and verifying multi-tenant isolation']

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1592
- T1526
- T1552
- T1087
- T1136
- T1531
- T1078
- T1199

## Notes
Exemplary responsible disclosure case study with <10 minute response times from vendor. Attack demonstrates critical importance of securing customer data APIs in fintech/rewards platforms. Findings affected multiple airlines (Virgin, United) using same backend, indicating systemic risk across industry. Writeup credits collaborative effort (Sam Curry, Ian Carroll, Shubham Shah), suggesting formal bug bounty program engagement rather than opportunistic hacking.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
