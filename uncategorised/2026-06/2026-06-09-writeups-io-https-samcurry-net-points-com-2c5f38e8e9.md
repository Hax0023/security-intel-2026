# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Points.com (Bug Bounty/Responsible Disclosure)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Path Traversal, Authorization Bypass, Credential Exposure, Broken Authentication, Insecure Direct Object References (IDOR), API Security Misconfiguration
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities discovered in Points.com (backend for airline/hotel rewards programs) between March-May 2023 allowing unauthorized access to 22M+ customer records, ability to transfer reward points, and access to administrative consoles. Vulnerabilities included unauthenticated path traversal, authorization bypass with minimal credentials, and leaked tenant API credentials. All issues were patched within hours of responsible disclosure.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated path traversal vulnerability on publicly accessible points.com API endpoint
2. Attacker enumerates 22 million customer order records containing PII, partial credit card numbers, rewards account numbers, and authorization tokens
3. Attacker extracts victim surname and rewards number from exposed database records
4. Attacker uses second vulnerability (authorization bypass) to generate valid authentication tokens with only surname and rewards number
5. Attacker uses stolen tokens to transfer reward points to their own account, access customer billing/contact information, and view transaction histories
6. Attacker discovers leaked macID/macKey credentials for Virgin rewards program on points.com endpoint, uses them to sign API requests and gain full airline administrator privileges

## Root cause
Multiple systemic security failures: (1) Inadequate path traversal input validation and access controls on internal API endpoints, (2) Authorization logic relying solely on non-secret PII (surname, rewards number) without rate limiting or additional verification, (3) Credential management exposing sensitive API signing keys in client-accessible endpoints, (4) Lack of authentication requirements on sensitive data retrieval endpoints, (5) Insufficient API security architecture separating customer and administrative access

## Attacker mindset
Opportunistic researcher systematically mapping public-facing points.com infrastructure to identify authentication/authorization weaknesses. Focused on finding chaining vulnerabilities - leveraging initial path traversal for credential harvesting, then using harvested data to exploit authorization bypass. Sophisticated understanding of API security and rewards program architecture. Responsible disclosure approach suggests ethical security researcher rather than malicious actor.

## Defensive takeaways
- Implement strict input validation and output encoding to prevent path traversal; use allowlists for API paths
- Require multi-factor authentication and additional verification beyond PII for sensitive account operations
- Never expose API signing credentials (macID/macKey) in client-accessible responses; use secure credential management systems
- Implement proper authentication/authorization on all API endpoints; verify user identity independently of client-provided data
- Apply rate limiting and anomaly detection on authorization flows to detect bulk account access attempts
- Separate authentication tokens by privilege level; ensure customer tokens cannot access customer data of others
- Conduct comprehensive API security assessment covering IDOR, privilege escalation, and credential exposure vectors
- Implement logging and monitoring for unusual data access patterns and bulk queries
- Regular security audits of third-party APIs and tenant credential management practices
- Establish incident response procedures with rapid remediation capabilities (points.com achieved <1 hour responses)

## Variant hunting
['Search for other API endpoints on points.com and partner domains leaking tenant credentials or API keys', 'Test other loyalty programs built on points.com infrastructure for similar path traversal patterns', 'Enumerate alternative authentication bypass methods using partial customer data (email, phone, account number combinations)', 'Investigate if customer authorization tokens can be leveraged to access unrelated customer accounts or loyalty programs', 'Check for similar credential exposure in other points.com tenant configuration endpoints', 'Test for IDOR vulnerabilities in administrative functions using enumerated customer/program IDs from path traversal', 'Examine API request signing mechanisms across different tenant integrations for credential leakage', 'Hunt for other endpoints accepting optional sorting/filtering parameters that could enable data enumeration']

## MITRE ATT&CK
- T1190
- T1200
- T1040
- T1566
- T1598
- T1589
- T1021
- T1078
- T1087
- T1580
- T1526

## Notes
Exceptionally well-coordinated disclosure with rapid response (<1 hour for most vulnerabilities). Points.com demonstrated mature incident response practices by immediately taking affected services offline and patching. Writeup exemplifies responsible disclosure and ethical security research. The vulnerability chaining (path traversal → credential harvesting → authorization bypass → privilege escalation) demonstrates sophisticated attack methodology. Impact potential was catastrophic given exposure of 22M customer records and ability to generate administrative access. No evidence of exploitation in the wild before disclosure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
