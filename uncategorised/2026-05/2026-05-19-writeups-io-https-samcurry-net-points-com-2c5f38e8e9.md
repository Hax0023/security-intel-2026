# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Points.com (Bug Bounty via Responsible Disclosure)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Directory Traversal, Broken Authentication, Authorization Bypass, Credential Exposure, Insecure Direct Object References (IDOR), API Security Misconfiguration
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities discovered in Points.com backend system affecting 22+ million customer records across major airline and hotel rewards programs. Attackers could access sensitive PII, transfer reward points, forge authentication tokens, and gain full administrative access through directory traversal, auth bypass, and leaked tenant credentials.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint on points.com infrastructure
2. Exploits directory traversal to access internal API querying 22 million order records containing PII and partial credit card numbers
3. Extracts customer surnames and rewards numbers from leaked data
4. Uses only surname and rewards number to trigger authorization bypass, generating forged account authorization tokens
5. Authenticates as legitimate customer to transfer reward points to attacker-controlled account or access admin functions
6. Leverages leaked Virgin tenant credentials (macID/macKey) to sign API requests impersonating the airline and modify rewards programs globally

## Root cause
Multiple systemic security failures: (1) Insufficient access controls on internal API endpoints exposing directory traversal, (2) Weak authentication mechanism relying solely on publicly-disclosed surname and rewards number, (3) Failure to implement token validation and request signing verification, (4) Exposure of tenant API credentials in client-side or publicly-accessible endpoint, (5) Lack of input validation and path normalization on traversal-prone endpoints

## Attacker mindset
Advanced persistent threat targeting high-value loyalty platform infrastructure. Motivation likely financial (transferring miles/points for resale), competitive intelligence (accessing competitor program data), or establishing persistent administrative access for long-term exploitation. Methodical reconnaissance identifying multiple attack vectors and escalation paths.

## Defensive takeaways
- Implement strict access controls and authentication on all API endpoints; eliminate direct path traversal possibilities through proper input validation and canonicalization
- Require multi-factor authentication beyond PII for sensitive operations; never use publicly-disclosed information (surname, rewards number) as sole auth factors
- Enforce principle of least privilege with granular role-based access control (RBAC) for administrative functions
- Rotate and secure all tenant/partner API credentials; never expose credentials in client-facing endpoints, frontend code, or response bodies
- Implement request signing and HMAC validation for inter-service communication; validate signatures server-side before processing
- Audit and segment internal APIs; restrict access to production data APIs from public-facing infrastructure
- Deploy Web Application Firewall (WAF) with traversal detection rules; implement rate limiting on sensitive endpoints
- Conduct comprehensive security testing including path traversal fuzzing, authentication/authorization testing, and API security assessments
- Maintain incident response procedures; monitor for unusual data access patterns on customer records
- Establish bug bounty program with clear SLAs (this vendor responded within 1 hour—positive practice)

## Variant hunting
['Search for similar directory traversal patterns on other loyalty platform backends (Marriott Bonvoy, Hilton Honors, Amex Rewards)', 'Test authorization bypass on other APIs using only partial customer identifiers (phone number, email, account number combinations)', 'Enumerate for leaked API credentials in similar cloud-hosted admin panels, particularly those using HMAC/MAC authentication schemes', 'Fuzz API endpoints with path traversal payloads (../, ..\\, URL encoding variants) to discover additional information disclosure paths', 'Investigate whether other tenant programs (airlines, hotels) hosted on same infrastructure have exposed credentials or auth bypasses', 'Test for IDOR vulnerabilities in customer account endpoints using sequential or enumerable account IDs', 'Search public repositories (GitHub, Pastebin) for leaked Points.com API documentation or credential patterns']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate Remote Systems
- T1589 - Gather Victim Identity Information
- T1583 - Acquire Infrastructure
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process
- T1134 - Access Token Manipulation
- T1087 - Account Discovery
- T1057 - Process Discovery
- T1083 - File and Directory Discovery
- T1552 - Unsecured Credentials

## Notes
This is an exemplary responsible disclosure case with rapid vendor response (under 10 minutes for multiple reports). The cascading nature of vulnerabilities demonstrates how initial information disclosure (directory traversal) enables subsequent exploitation (auth bypass using leaked PII). The involvement of three coordinated security researchers (Curry, Carroll, Shah) suggests this was submitted through formal vulnerability disclosure rather than traditional bug bounty platform. Vendor's swift remediation and transparent acknowledgment is noteworthy. The Points.com platform's critical role as backend for major loyalty programs amplifies the severity—compromise would affect millions of end consumers across multiple airlines and hotels.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
