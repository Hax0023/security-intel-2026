# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Points.com
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln types:** Path Traversal, Authorization Bypass, Credential Exposure, Broken Authentication, Improper API Configuration, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities were discovered in Points.com, a backend provider serving major airline and hotel rewards programs, affecting 22 million customer records. The vulnerabilities included unauthenticated path traversal exposing customer data, authorization bypasses allowing unauthorized points transfers, and leaked tenant credentials enabling full API impersonation. These flaws would have allowed attackers to access sensitive customer information, transfer rewards points, and gain administrative control over rewards programs.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint on points.com infrastructure
2. Attacker queries internal API to retrieve customer order records including names, addresses, emails, phone numbers, and partial credit card numbers from 22 million records
3. Attacker uses exposed customer data (surname + rewards number) to exploit authorization bypass vulnerability in rewards transfer API
4. Attacker generates valid authentication tokens allowing them to impersonate customers and access full account details, billing information, and transaction history
5. Attacker discovers leaked macID and macKey credentials on Virgin rewards website used for signing API requests as the airline
6. Attacker uses tenant credentials to authenticate to core Points.com API and perform administrative functions including modifying customer accounts, adding/removing points, and altering program settings

## Root cause
Multiple architectural and implementation failures: (1) Lack of authentication controls on internal API endpoints, (2) Insufficient authorization validation allowing generation of tokens with only minimal user identifiers, (3) Credential management failures resulting in API secrets being embedded in client-accessible code or responses, (4) Absence of API request signing verification, (5) Over-permissive API designs granting full account access based on weak identifiers

## Attacker mindset
Systematic reconnaissance and privilege escalation approach targeting high-value targets. Attacker leveraged initial information disclosure to enable subsequent authorization bypasses, demonstrating chained exploitation methodology. Focus on administrative access to unlock complete system control rather than individual account compromise. Opportunistic discovery of leaked credentials as force multiplier for gaining backend API access.

## Defensive takeaways
- Implement mandatory authentication and authorization checks on all API endpoints, including internal-facing APIs
- Require multi-factor identifiers for sensitive operations; never issue authentication tokens based solely on public or semi-public user identifiers
- Implement proper secrets management; never embed API credentials in client-accessible responses, frontend code, or static resources
- Use cryptographic signing and request verification for all API communications; rotate credentials regularly
- Implement least-privilege access controls; limit token scope to minimum necessary permissions
- Conduct comprehensive security audits of path handling and input validation across all endpoints
- Monitor for unusual API access patterns and implement rate limiting on sensitive operations
- Establish incident response procedures for rapid remediation of authentication/authorization issues
- Implement centralized logging and alerting for suspicious authentication attempts and bulk data access

## Variant hunting
Search for similar patterns in other rewards/loyalty platforms: (1) Check for unauthenticated API endpoints on loyalty program backends, (2) Audit authorization logic in rewards transfer/redemption APIs for weak identifier validation, (3) Hunt for exposed credentials in static assets, error messages, or API responses across financial services platforms, (4) Test for path traversal in API gateways and backend routing, (5) Examine multi-tenant environments for cross-tenant API access vulnerabilities, (6) Review airline/hotel partner integration endpoints for credential exposure, (7) Audit admin console access controls and token generation mechanisms

## MITRE ATT&CK
- T1190
- T1526
- T1200
- T1566
- T1589
- T1590
- T1078
- T1087
- T1555
- T1580
- T1199

## Notes
This is a high-profile multi-vector attack against critical infrastructure serving millions of customers. The vulnerability chain demonstrates how information disclosure can enable authorization bypass attacks. Points.com's rapid response (under 10 minutes to acknowledgment, under 1 hour for remediation) is exemplary incident response. The 22 million affected records represents one of the larger datasets at risk. The writeup does not specify final bounty amount, suggesting potential regulatory sensitivity. The involvement of multiple security researchers indicates coordinated disclosure process. Vulnerabilities span from March to May 2023, suggesting either ongoing discovery or delayed reporting of later findings.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
