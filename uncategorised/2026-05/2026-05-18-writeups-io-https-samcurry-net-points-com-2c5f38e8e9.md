# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Points.com (Responsible Disclosure)
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln types:** Path Traversal, Authorization Bypass, Credential Exposure, Insecure Direct Object References (IDOR), API Authentication Bypass, Insufficient Access Controls
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Researchers discovered multiple critical vulnerabilities in Points.com, the backend provider for major airline and hotel rewards programs, affecting 22 million customer order records. Vulnerabilities included unauthenticated path traversal to internal APIs, authorization bypass allowing rewards transfer with minimal information, and leaked API credentials for airline partners. These issues would have allowed attackers to access sensitive customer data, transfer loyalty points, and gain administrative access to global systems.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint exposing internal API endpoints
2. Attacker queries the internal API iteratively to enumerate and extract 22 million customer records containing PII, partial credit cards, and rewards numbers
3. Attacker uses extracted customer surnames and rewards numbers to exploit authorization bypass and generate valid authentication tokens
4. Attacker uses authenticated tokens to transfer rewards points to their own accounts and access victim account details
5. Attacker finds leaked tenant credentials (macID/macKey) exposed on publicly accessible Virgin rewards endpoint
6. Attacker signs API requests with leaked credentials to impersonate Virgin airline and modify rewards programs, customer accounts, and issue/remove points globally

## Root cause
['Failure to implement proper authentication on internal API endpoints', 'Missing or inadequate authorization checks allowing users to perform actions on other accounts with minimal identifying information', 'Exposure of sensitive cryptographic credentials in client-side or publicly accessible endpoints', 'Lack of input validation on API parameters allowing traversal and enumeration', 'Insufficient access controls on tenant/partner credential storage and exposure']

## Attacker mindset
Systematic reconnaissance and privilege escalation targeting high-value targets (airlines/hotels). Attacker demonstrates understanding of API architecture, credential usage patterns, and reward system mechanics. Focus on maximizing impact through mass data exfiltration and unauthorized financial transactions while maintaining operational security.

## Defensive takeaways
- Implement mandatory authentication on all API endpoints, including those believed to be internal-only
- Enforce principle of least privilege with strong authorization checks based on user identity, not just credentials
- Never embed sensitive credentials (API keys, signing keys) in client-facing code or responses
- Implement rate limiting and anomaly detection on high-risk operations like fund transfers
- Conduct regular security audits of API endpoint exposure, especially around customer data access
- Use defense-in-depth approach: combine authentication, authorization, encryption, and monitoring
- Implement proper secret management and rotation for multi-tenant/partner credentials
- Add detailed audit logging for all privileged operations and data access
- Validate and sanitize all path parameters to prevent traversal attacks
- Segment networks and APIs to isolate tenant access from global administration systems

## Variant hunting
['Check other endpoints on points.com subdomains for similar path traversal patterns', 'Review all partner/airline portal endpoints for exposed credentials or API keys', 'Search for similar authorization bypasses using minimal user identifiers across different reward programs', 'Audit all multi-tenant environments for proper isolation and access controls', 'Test for IDOR vulnerabilities on endpoints accepting user IDs, order IDs, or account numbers', 'Search for leaked credentials in responses, error messages, and debugging endpoints across hospitality/travel industry APIs']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1611 - Escape to Host
- T1552.001 - Unsecured Credentials: Credentials in Files
- T1110.001 - Brute Force: Password Guessing
- T1087.001 - Account Discovery: Local Account
- T1136.001 - Create Account: Local Account
- T1078.001 - Valid Accounts: Default Accounts
- T1098 - Account Manipulation
- T1530 - Data from Cloud Storage
- T1213 - Data from Information Repositories

## Notes
Researchers demonstrated exceptional coordination and responsible disclosure practices. Points.com team responded rapidly (under 10 minutes to under 1 hour) and took affected systems offline during remediation. This case exemplifies the critical importance of security in financial systems handling sensitive PII and monetary assets. The vulnerability chain demonstrates how initial information disclosure (22M records) becomes weaponized through authorization bypass and credential exposure to achieve complete system compromise.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
