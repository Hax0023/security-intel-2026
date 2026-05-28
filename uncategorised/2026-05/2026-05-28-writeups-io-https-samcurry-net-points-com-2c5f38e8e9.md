# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Points.com (Bug Bounty/Responsible Disclosure)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Path Traversal, Authorization Bypass, Credential Exposure, Broken Authentication, Improper Access Control, API Security Misconfiguration
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Security researchers discovered multiple critical vulnerabilities in Points.com, the backend provider for major airline and hotel rewards programs, affecting 22 million customer records. Vulnerabilities included unauthenticated path traversal to customer data, authorization bypass allowing points transfers, and leaked API credentials for tenant programs. All issues were patched within hours of responsible disclosure.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint exposing internal API with access to 22 million order records
2. Attacker enumerates customer data including partial credit card numbers, addresses, emails, phone numbers, and rewards numbers through API pagination
3. Attacker uses disclosed rewards number and surname from step 2 to exploit authorization bypass and generate valid authentication tokens
4. Attacker uses stolen tokens to transfer reward points to their own account and access sensitive customer information across multiple programs
5. Attacker discovers leaked macID and macKey credentials on Virgin rewards website and uses them to sign API requests as the airline
6. Attacker gains full administrative access to points.com console with ability to modify accounts, manage rewards programs, and issue arbitrary points

## Root cause
Multiple API security misconfigurations: (1) Insufficient input validation allowing path traversal, (2) Missing or weak authorization checks on sensitive endpoints, (3) Credentials embedded or exposed in client-facing responses, (4) Over-reliance on easily guessable identifiers (surname + rewards number) for authentication, (5) Lack of API gateway protection and request signing validation

## Attacker mindset
An attacker could systematically exploit these vulnerabilities to commit large-scale fraud by transferring miles from millions of customers, stealing personally identifiable information for identity theft, or gaining administrator access to manipulate the entire rewards ecosystem affecting numerous airlines and hotels. The attack requires minimal knowledge once vulnerabilities are discovered—just names and rewards numbers from the traversal flaw enable full compromise.

## Defensive takeaways
- Implement strict input validation and canonicalization to prevent path traversal attacks; use allowlists for API endpoints
- Enforce proper authorization checks on all API endpoints; validate user permissions for every sensitive operation
- Never expose sensitive credentials, keys, or tokens in client-accessible responses or static files
- Implement strong authentication mechanisms beyond easily guessable identifiers; require multi-factor verification for sensitive operations
- Use API gateways with rate limiting, request signing validation, and comprehensive logging
- Conduct regular security audits of API responses to identify data leakage
- Implement zero-trust architecture with mutual TLS and cryptographic request signing
- Segment administrative consoles from customer-facing APIs with separate authentication mechanisms
- Monitor for unusual access patterns and bulk data queries

## Variant hunting
Look for similar path traversal patterns in other points.com-hosted reward programs; search for other endpoints exposing macID/macKey or similar service-to-service credentials; test authorization bypass on other loyalty platforms using minimal user identifiers; investigate whether other airlines/hotels experienced similar tenant credential exposure; examine backup/archive endpoints that may bypass traversal protections

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (potential downstream use of stolen PII)
- T1040 - Traffic Sniffing (API credential interception)
- T1110 - Brute Force (enumeration via API pagination)
- T1526 - Reconnaissance/Web Service Discovery
- T1199 - Trusted Relationship (exploitation via legitimate API endpoints)
- T1134 - Access Token Manipulation
- T1087 - Account Discovery (via data enumeration)

## Notes
This vulnerability chain demonstrates the critical importance of defense-in-depth in financial platforms. The researchers' responsible disclosure approach (immediate reporting, coordinated patching) prevented real-world exploitation of vulnerabilities affecting millions of customers. The 10-minute response time by Points.com indicates mature incident response capability. The progression from initial path traversal to full administrative access illustrates how multiple low-to-medium severity issues can chain into critical compromise.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
