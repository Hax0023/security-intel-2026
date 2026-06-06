# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Points.com (Bug Bounty)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Directory Traversal, Broken Authentication, Authorization Bypass, Credential Exposure, Insecure Direct Object Reference (IDOR), API Security Misconfiguration
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities in points.com backend enabled unauthorized access to 22 million customer records, ability to transfer airline/hotel rewards points, and access to administrative consoles. Vulnerabilities included unauthenticated path traversal, broken authentication requiring only surname and rewards number, and leaked API credentials for major airline partners like Virgin and United.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint on points.com API
2. Using directory traversal, attacker queries internal API and retrieves 22 million order records containing PII (names, addresses, emails, phone numbers, redacted credit cards, customer tokens)
3. Attacker uses leaked customer data (surname + rewards number) to exploit authorization bypass vulnerability
4. Attacker generates valid authentication tokens for arbitrary customer accounts without credentials
5. Attacker authenticates as legitimate customer and transfers rewards points to attacker-controlled account
6. Attacker escalates privileges using leaked tenant credentials (macID/macKey) to access global admin console with full control over rewards programs

## Root cause
Multiple security design and implementation failures: (1) Inadequate access controls on internal APIs with no authentication requirements, (2) Insufficient authorization checks allowing token generation with minimal identifying information, (3) Credentials hardcoded/exposed in client-accessible endpoints, (4) Lack of API rate limiting and enumeration protections, (5) Improper separation of customer and administrative API scopes

## Attacker mindset
An attacker would recognize points.com as a high-value target due to its role as backend for major airline/hotel programs, multiple revenue streams (point transfers, account takeovers, mass PII harvesting), and opportunity for financial fraud at scale. The progression from data exfiltration to privilege escalation demonstrates methodical exploitation chain development.

## Defensive takeaways
- Implement mandatory authentication on all API endpoints, especially internal/administrative ones
- Enforce strong authorization checks with multiple factors beyond easily guessable attributes (surname + rewards number insufficient)
- Never embed API credentials (macID, macKey) in client-facing endpoints or frontend code
- Implement rate limiting and request throttling to prevent enumeration attacks on customer records
- Segregate customer-facing APIs from administrative/privileged APIs with distinct authentication mechanisms
- Conduct thorough API security reviews focusing on path traversal, IDOR, and authorization bypass patterns
- Implement proper input validation and parameter sanitization to prevent traversal attacks
- Use secrets management solutions for API credentials with appropriate rotation policies
- Monitor for suspicious enumeration patterns and mass data access attempts
- Perform regular security audits of backend infrastructure and API exposure

## Variant hunting
Search for similar patterns in other points.com-hosted reward programs beyond Virgin and United; examine other travel/hospitality backends for path traversal and exposed credentials; test IDOR vulnerabilities on other airline partner APIs; look for additional customer data exposure through different API endpoints; investigate whether credentials exist in client-side JavaScript or configuration files on other partner sites

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing (via credential disclosure)
- T1526: Reconnaissance
- T1589: Gather Victim Identity Information
- T1528: Steal Application Access Token
- T1556: Modify Authentication Process
- T1199: Trusted Relationship
- T1087: Account Discovery
- T1580: Cloud Infrastructure Discovery
- T1078: Valid Accounts

## Notes
Excellent response time from points.com team (under 1 hour for most reports). The vulnerability chain demonstrates critical importance of proper API security architecture. The 22 million records exposure and cross-customer fund transfer capability represent severe financial and privacy impact. The leaked tenant credentials (Virgin macID/macKey) represent particularly dangerous privilege escalation vector. Writeup lacks specific bounty amount and remediation timeline details.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
