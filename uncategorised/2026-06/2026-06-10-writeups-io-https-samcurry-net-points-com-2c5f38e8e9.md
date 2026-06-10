# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Points.com (Airline and Hotel Rewards Platform)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Path Traversal / Directory Traversal, Authorization Bypass, Broken Authentication, Credential Exposure, API Authentication Weakness, Improper Access Control
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Researchers discovered multiple critical vulnerabilities in Points.com affecting 22 million customer records, including unauthenticated path traversal exposing PII, authorization bypasses allowing unauthorized point transfers with minimal credentials, and leaked tenant API credentials enabling full administrative access. The vulnerabilities would have enabled attackers to access sensitive customer data, transfer rewards points, and gain full administrative control over loyalty programs for major airlines and hotels.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint on points.com API
2. Attacker queries the traversal endpoint to access internal order records database containing 22 million customer records
3. Attacker extracts customer PII including surnames, rewards numbers, partial credit cards, addresses, emails, and authorization tokens from order records
4. Attacker uses leaked customer surnames and rewards numbers with authorization bypass vulnerability to generate valid authentication tokens for target customer accounts
5. Attacker uses generated tokens to transfer customer rewards points to their own account and access full account management capabilities
6. Attacker discovers leaked macID and macKey credentials for Virgin Rewards program and uses them to sign API requests, gaining full administrative control over the airline's loyalty program

## Root cause
Multiple security failures: (1) Inadequate input validation and authentication controls on API endpoints allowing path traversal; (2) Weak authorization implementation relying solely on easily-obtainable public information (surname + rewards number); (3) Exposure of cryptographic signing credentials (macID/macKey) in endpoint responses; (4) Lack of proper access control separation between customer and administrative APIs; (5) Insufficient API authentication and endpoint protection mechanisms

## Attacker mindset
Opportunistic attacker targeting high-value loyalty program infrastructure for financial gain through point theft and potential resale. Initial reconnaissance focused on finding authentication weaknesses and information disclosure issues. Upon discovering path traversal, attacker would systematically enumerate and extract large datasets. The discovery of tenant credentials would escalate capabilities to full administrative control, enabling large-scale fraud across multiple airline programs.

## Defensive takeaways
- Implement strict input validation and sanitization to prevent path traversal attacks; use allowlists for API paths
- Redesign authorization model to require strong authentication factors beyond public PII (surname + rewards number); implement OAuth/JWT with proper signature verification
- Never expose cryptographic signing credentials in responses; store secrets securely in environment variables or vault systems
- Implement proper API gateway authentication and rate limiting to detect enumeration attempts
- Separate customer-facing and administrative APIs with distinct authentication mechanisms and network segmentation
- Conduct regular security audits of API endpoints with focus on authentication and authorization mechanisms
- Implement comprehensive API logging and monitoring to detect suspicious access patterns
- Use API key rotation policies and credential expiration mechanisms
- Perform penetration testing specifically targeting authorization bypass scenarios
- Establish a responsible disclosure policy and maintain rapid response capabilities for security reports

## Variant hunting
Search for similar patterns in other loyalty program platforms and travel-related APIs: (1) Look for other reward programs using weak authentication based only on surname+number combination; (2) Check airline/hotel partner APIs for exposed signing credentials in responses; (3) Scan for path traversal vulnerabilities in reward program backends; (4) Test for authorization bypass in competitor programs (Marriott Bonvoy, SPG, Delta SkyMiles, etc.); (5) Look for API endpoints exposing customer order/transaction records; (6) Check for improperly configured CORS allowing cross-origin API access; (7) Hunt for credentials in error messages, logs, or development endpoints

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1567 - Exfiltration Over Web Service
- T1526 - Enumerate APIs
- T1589 - Gather Victim Identity Information
- T1110 - Brute Force
- T1555 - Credentials from Password Stores
- T1187 - Forced Authentication
- T1057 - Process Discovery
- T1580 - Cloud Infrastructure Discovery

## Notes
Excellent response time from Points.com team (under 10-60 minutes for each report). The vulnerability chain demonstrates how initial information disclosure (path traversal + customer data leak) can be weaponized with authorization bypass to escalate to full account takeover. The leak of cryptographic signing credentials represents the most severe issue as it enabled impersonation of legitimate airline clients to the core API. The 22 million affected records and potential impact on major airlines (Virgin, United, etc.) indicates this was a critical infrastructure vulnerability with wide-ranging implications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
