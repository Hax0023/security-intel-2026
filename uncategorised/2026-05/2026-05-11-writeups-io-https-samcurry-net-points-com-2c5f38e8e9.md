# Leaked Secrets and Unlimited Miles: Hacking Points.com - Multiple Critical Vulnerabilities in Airline/Hotel Rewards Platform

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Points.com (Bug Bounty / Responsible Disclosure)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Path Traversal / Directory Traversal, Authorization Bypass, Credential Exposure / Secrets Leakage, Broken Authentication, API Abuse, Improper Access Control
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities were discovered in Points.com, the backend provider for major airline and hotel rewards programs, between March-May 2023. These flaws allowed unauthenticated access to 22 million customer records, unauthorized transfer of airline miles/points, and full administrative access using leaked API credentials. All vulnerabilities were responsibly disclosed and remediated within hours.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint exposing internal API endpoints
2. Attacker enumerates Points.com customer order database (22M records) to harvest PII, partial credit cards, and rewards numbers
3. Attacker uses harvested rewards number and surname to trigger authorization bypass in rewards transfer API
4. Attacker generates forged authorization tokens to impersonate customer accounts and transfer points to attacker-controlled account
5. Attacker discovers leaked macID/macKey credentials in publicly accessible Virgin rewards endpoint
6. Attacker signs API requests as airline tenant to access administrative functions, modify customer accounts, and add/remove points globally

## Root cause
['Lack of input validation and path canonicalization on HTTP endpoints', 'Insufficient authorization checks relying only on public information (surname + rewards number)', 'Hardcoded API credentials stored in client-accessible endpoints without proper secret management', 'Absence of rate limiting and anomaly detection on sensitive APIs', 'Missing authentication on administrative API endpoints', 'Inadequate separation of concerns between public and internal APIs']

## Attacker mindset
Opportunistic security researcher identifying systemic architectural flaws in a critical infrastructure platform. Focus on chaining vulnerabilities to achieve maximum impact (data exfiltration + operational compromise). Motivation: bug bounty program, security research credibility, and demonstrating severity of platform-wide risks.

## Defensive takeaways
- Implement strict input validation and use allowlists for API path parameters; canonicalize all paths before processing
- Enforce multi-factor authentication and role-based access control; never rely solely on public information for authorization decisions
- Never store API credentials or secrets in client-accessible endpoints; use secure secret management solutions (vaults, HSMs)
- Implement rate limiting, request signing validation, and comprehensive API authentication on all endpoints including administrative ones
- Separate public-facing APIs from internal/administrative APIs on different infrastructure with network segmentation
- Deploy continuous monitoring for unusual API patterns, bulk data access attempts, and privilege escalation activities
- Conduct regular security audits focusing on authentication and authorization logic across all tenant integrations
- Implement request logging and establish incident response procedures for credential compromise scenarios

## Variant hunting
['Similar path traversal patterns on other tenant reward program endpoints (American, Delta, Marriott)', 'Authorization bypass logic in points transfer APIs for other airlines using only public user identifiers', 'Exposed API credentials for other airline/hotel partners in publicly accessible configuration files or endpoints', 'Unauthenticated administrative endpoints on points.com backend serving different business units', 'IDOR vulnerabilities in customer account endpoints accessible with modified user IDs or rewards numbers', 'JWT/token generation flaws allowing signature bypass or algorithm confusion attacks', 'API rate limiting bypass techniques allowing mass enumeration of customer databases', "Cross-tenant API access issues allowing one partner's credentials to access another partner's data"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (data harvesting leading to credential compromise)
- T1110 - Brute Force (enumeration of 22M records)
- T1526 - Reconnaissance (API discovery and endpoint mapping)
- T1078 - Valid Accounts (authorization bypass to impersonate customers)
- T1550 - Use Alternate Authentication Material (forged authorization tokens)
- T1087 - Account Discovery (enumerating customer accounts via API)
- T1014 - Rootkit (potential administrative access with leaked credentials)
- T1556 - Modify Authentication Process (token generation abuse)

## Notes
Outstanding example of responsible disclosure with exceptionally fast vendor response (under 10 minutes for most reports, 1 hour for credential exposure). Vulnerability chain demonstrates how multiple seemingly individual flaws compound into catastrophic system compromise. The 22 million affected customer records and multi-partner impact (Virgin, United, others) represents significant systemic risk. Researchers: Sam Curry, Ian Carroll, Shubham Shah. All vulnerabilities patched by publication date (August 2023).

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
