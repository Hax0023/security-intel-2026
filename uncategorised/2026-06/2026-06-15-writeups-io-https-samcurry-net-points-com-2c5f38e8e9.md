# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Points.com (bug bounty program)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Path Traversal / Directory Traversal, Authorization Bypass, Broken Authentication, Credential Exposure, API Key Leakage, Insecure Direct Object References (IDOR), Insufficient Access Controls
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Security researchers discovered multiple critical vulnerabilities in Points.com, the backend platform serving airline and hotel rewards programs for millions of customers. The vulnerabilities included unauthenticated path traversal to customer databases, authorization bypasses allowing points transfers with minimal information, and hardcoded tenant API credentials. These flaws could have enabled attackers to access customer PII, transfer points, and gain administrative control over reward programs.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated path traversal endpoint and accesses internal API returning customer order records
2. Attacker extracts 22 million order records containing partial credit card numbers, addresses, emails, and rewards numbers through enumerated API queries
3. Attacker uses extracted rewards numbers and surnames to call authorization bypass endpoints, generating valid authentication tokens
4. Attacker uses tokens to transfer points to their own account, access billing information, and view transaction history
5. Attacker discovers leaked macID and macKey credentials on Virgin rewards website, allowing API calls impersonating the airline
6. Attacker uses credentials to modify customer accounts, add/remove points, and alter rewards program settings with full administrative privileges

## Root cause
Multiple security misconfigurations: (1) Insufficient input validation on path parameters enabling directory traversal, (2) Weak authorization checks relying only on public fields (surname, rewards number) without proper authentication, (3) Hardcoded API credentials stored and exposed in client-accessible endpoints, (4) Absence of proper access controls on administrative APIs, (5) No rate limiting or anomaly detection on sensitive operations

## Attacker mindset
Opportunistic researcher or malicious actor targeting high-value loyalty program systems. Initial reconnaissance focused on API endpoint discovery through path manipulation. Once customer data access was confirmed, natural progression to privilege escalation by exploiting weak authorization logic. Discovery of hardcoded credentials represented goldmine for achieving administrative compromise. The sequential nature of reports suggests methodical exploitation of each discovered weakness before moving to next attack surface.

## Defensive takeaways
- Implement strict input validation and sanitization for all path parameters; use allowlists rather than blacklists
- Enforce proper authentication before any data access, not just authorization checks
- Never rely on single public identifier or weak combinations for authorization decisions; use cryptographic tokens and session management
- Implement secure credential management: never hardcode secrets in code, use environment variables or secure vaults, rotate credentials regularly
- Apply principle of least privilege to all API endpoints and administrative functions
- Implement comprehensive logging and alerting for sensitive operations like points transfers and administrative actions
- Conduct regular security audits and penetration testing of customer-facing APIs and authentication mechanisms
- Implement rate limiting and behavioral analysis on high-risk operations
- Use API gateway solutions to enforce consistent authentication and authorization policies
- Implement defense-in-depth: require multiple factors for sensitive operations even with valid authentication

## Variant hunting
Similar vulnerabilities likely exist in other loyalty program backends and payment processors. Search for: (1) Path traversal in other reward/loyalty platforms via predictable parameter patterns, (2) Authorization bypasses in travel/hospitality APIs using surname+membership_id combinations, (3) Exposed credentials in frontend code or client-accessible endpoints across other airline/hotel reward systems, (4) IDOR vulnerabilities in points transfer endpoints, (5) Unprotected administrative APIs lacking proper authentication, (6) Hardcoded API keys in mobile apps or web applications, (7) Similar patterns in cryptocurrency exchanges or digital asset platforms handling user transfers

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (not directly used but data exposure enables targeting)
- T1078 - Valid Accounts (generating unauthorized tokens)
- T1087 - Account Discovery
- T1526 - Adversary-in-the-Middle (credential usage)
- T1555 - Credentials from Password Stores (extracted credentials)
- T1586 - Compromise Accounts (account takeover capability)
- T1213 - Data from Information Repositories (API access to customer database)
- T1041 - Exfiltration Over C2 Channel (data extraction via API)

## Notes
Exceptional incident response: Points.com team responded within 10 minutes to most reports and remediated issues rapidly. Vulnerability discovery timeline (March-May 2023) shows methodical progression from reconnaissance to high-impact findings. The 22 million customer records affected represents massive potential impact. Collaboration between three security researchers increased finding severity and credibility. Writeup is notably missing specific bounty amount and full details on the 'global administration console' vulnerability mentioned in final heading. Points.com's rapid response prevented real-world exploitation but demonstrates critical importance of responsible disclosure practices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
