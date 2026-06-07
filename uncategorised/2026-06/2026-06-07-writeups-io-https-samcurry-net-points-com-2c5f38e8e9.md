# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Points.com (Bug Bounty Program)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Directory Traversal, Broken Authentication, Authorization Bypass, Credential Exposure, Insecure Direct Object References (IDOR), API Security Misconfiguration
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities were discovered in Points.com's backend infrastructure affecting 22+ million customer records across airline and hotel rewards programs. The vulnerabilities enabled unauthenticated access to sensitive customer data (credit cards, addresses, emails, phone numbers), unauthorized points transfers, and tenant credential leakage that granted full API access as airlines. All issues were patched within hours to one day of responsible disclosure.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated directory traversal endpoint that exposes internal API endpoints
2. Attacker queries the exposed API to enumerate 22 million customer order records with optional sorting parameters
3. Attacker extracts customer rewards numbers and surnames from leaked records
4. Attacker uses only rewards number and surname to generate valid authorization tokens via authorization bypass vulnerability
5. Attacker uses valid tokens to transfer points between accounts, access billing information, and view transaction history
6. Attacker discovers leaked tenant credentials (macID/macKey) and uses them to sign API requests on behalf of airlines, gaining administrative access to modify rewards programs and customer accounts

## Root cause
Multiple systemic security failures: (1) Insufficient path traversal input validation on internal API endpoints, (2) Weak authentication mechanisms relying on easily obtainable public information (surname + rewards number), (3) Missing authorization checks on sensitive endpoints, (4) Credential exposure through unprotected configuration endpoints, (5) Lack of API rate limiting and query restrictions

## Attacker mindset
An attacker would recognize Points.com as a high-value target due to its central role in managing rewards for major airlines and hotels affecting millions of customers. The attacker would systematically map the API surface, discover the directory traversal to access the customer database, then chain multiple vulnerabilities to escalate from data access to account manipulation to full administrative compromise. The discovery of leaked credentials would represent a critical escalation opportunity enabling impersonation of airline partners.

## Defensive takeaways
- Implement strict input validation and canonicalization for all path-based parameters to prevent directory traversal
- Enforce strong authentication requiring multiple factors beyond public information (surname/rewards number)
- Implement proper authorization checks at API endpoint level, not relying on client-side validation
- Never expose API credentials, keys, or secrets in frontend responses or configuration files; use secure credential management
- Apply principle of least privilege to API endpoints and customer data access
- Implement API rate limiting, query restrictions, and pagination limits to prevent mass data enumeration
- Conduct regular security testing of internal and partner-facing APIs
- Implement comprehensive audit logging for sensitive operations
- Use API gateways with authentication/authorization enforcement before reaching backend services
- Segment customer data access by account and require proper authentication at API level

## Variant hunting
Search for similar vulnerabilities in other multi-tenant reward platform providers; test for directory traversal in partner-facing API endpoints; enumerate API endpoints for missing authentication on account modification functions; review public S3 buckets and GitHub repositories for exposed API credentials from points.com partners; test authorization bypass in other customer identification scenarios (email + verification code, phone + PIN); check for unprotected admin consoles at subdomains related to other airlines/hotels using points.com backend

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1552.001 - Credentials In Files
- T1087 - Account Discovery
- T1110 - Brute Force
- T1555 - Credentials from Password Stores
- T1078 - Valid Accounts
- T1021 - Remote Services

## Notes
This writeup represents a masterclass in API security research with multiple chained vulnerabilities. The rapid response from Points.com (under 10 minutes to 1 hour) demonstrates effective incident response. The vulnerability chain escalated from information disclosure to account compromise to full administrative access. The discovery of tenant credentials (Virgin macID/macKey) is particularly noteworthy as it enabled complete impersonation of airline partners. The researchers responsibly disclosed all issues between March-May 2023 and provided clear technical documentation of each vulnerability class.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
