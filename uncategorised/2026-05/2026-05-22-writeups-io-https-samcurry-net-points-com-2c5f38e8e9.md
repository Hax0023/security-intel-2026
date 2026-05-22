# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** points.com
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Directory Traversal, Broken Authentication, Authorization Bypass, API Credential Exposure, Insufficient Access Controls
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities discovered in points.com, the backend provider for major airline and hotel rewards programs, allowing unauthorized access to 22 million customer records and administrative systems. Attackers could access PII, transfer reward points, and gain full administrative control over rewards programs affecting millions of customers globally.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated directory traversal endpoint on points.com infrastructure
2. Attacker queries internal API without authentication to enumerate 22 million order records containing PII and partial credit card data
3. Attacker extracts customer rewards numbers and surnames from exposed records
4. Attacker uses authorization bypass vulnerability to generate forged authentication tokens for target customers using only surname and rewards number
5. Attacker transfers reward points from customer accounts or authenticates to administrative panels with forged tokens
6. Attacker gains access to global administration console to issue points, manage programs, and modify customer accounts at scale

## Root cause
Multiple configuration and design failures: (1) Insufficient path traversal validation allowing access to internal APIs; (2) Weak authentication mechanisms requiring only publicly-disclosed customer fields; (3) Improper credential storage and exposure of API signing keys (macID/macKey) in client-facing endpoints; (4) Lack of proper authorization checks on administrative functions; (5) No rate limiting or anomaly detection on sensitive operations

## Attacker mindset
Opportunistic reconnaissance-focused approach demonstrating systematic vulnerability chaining: starting with passive enumeration (directory traversal), escalating to data exfiltration, then leveraging exposed credentials for lateral movement and privilege escalation to global administrative access. The attacker was methodical, collaborative, and responsible in disclosure rather than exploitative.

## Defensive takeaways
- Implement strict input validation and path canonicalization to prevent directory traversal attacks
- Enforce strong authentication mechanisms beyond single customer attributes; require multi-factor verification for sensitive operations
- Never expose signing credentials (API keys, MACs, secrets) in client-facing endpoints or frontend code
- Implement proper authorization checks on all administrative functions with principle of least privilege
- Use cryptographic operations instead of simple field combinations for authentication tokens
- Implement comprehensive API rate limiting and behavioral anomaly detection for account manipulation
- Conduct regular security audits of all public endpoints and external-facing infrastructure
- Segregate customer data access APIs from administrative APIs with separate authentication mechanisms
- Implement proper logging and monitoring for sensitive operations like points transfers
- Establish bug bounty program and rapid response procedures for vulnerability reports

## Variant hunting
Search for similar patterns in other loyalty/rewards platforms: (1) Check for exposed API credentials in frontend configurations or source maps; (2) Test for directory traversal on internal API endpoints; (3) Probe authentication mechanisms that rely on personally-identifiable information alone; (4) Attempt to forge authorization tokens with minimal information; (5) Enumerate hidden administrative endpoints on loyalty platform subdomains; (6) Review API documentation for improperly exposed sensitive endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1552.001 - Credentials In Files
- T1555 - Credentials from Password Stores
- T1110 - Brute Force
- T1548 - Abuse Elevation Control Mechanism
- T1021 - Remote Services
- T1078 - Valid Accounts
- T1087 - Account Discovery
- T1530 - Data from Cloud Storage
- T1526 - Enumerate Cloud Resources

## Notes
Exemplary responsible disclosure: researchers coordinated with points.com who responded within 1 hour to each report and remediated all issues rapidly. The vulnerability chain is significant because it affects the backend infrastructure for numerous major airlines (United, Virgin, etc.) and hotel chains, with exposure affecting millions of loyalty program members. The escalation from information disclosure to full administrative compromise demonstrates the critical importance of securing administrative interfaces. No explicit bounty amount mentioned in writeup; points.com's rapid response suggests either active bug bounty program or strong security culture.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
