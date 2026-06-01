# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Points.com (Bug Bounty)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Path Traversal / Directory Traversal, Authorization Bypass, Broken Authentication, Credential Exposure, Insufficient Access Controls, API Security Misconfiguration
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Multiple critical vulnerabilities were discovered in Points.com, the backend for major airline and hotel rewards programs, affecting 22 million customer records. Vulnerabilities included unauthenticated path traversal to access customer data, authorization bypass to transfer rewards points, exposed tenant API credentials, and insufficient access controls on admin consoles. All issues were patched within hours of responsible disclosure.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint exposing internal API with access to 22 million order records
2. Attacker queries customer data including partial credit cards, addresses, emails, phone numbers, and reward point numbers through enumeration or targeted search
3. Attacker obtains customer surname and rewards number from leaked data to exploit authorization bypass in rewards transfer API
4. Attacker generates valid authorization tokens allowing full account management, point transfers, and access to billing/contact information
5. Attacker discovers exposed tenant credentials (macID/macKey) on Virgin rewards website enabling API signature generation
6. Attacker signs requests as Virgin airline to modify customer accounts, add/remove points, and alter rewards program settings globally

## Root cause
Multiple failures in security controls: (1) Path traversal due to improper input validation on API endpoints, (2) Authorization bypass through insufficient validation of user identity (only surname + rewards number), (3) Hardcoded/exposed credentials in client-accessible endpoints, (4) Lack of proper authentication/authorization checks on admin consoles, (5) Overly permissive API access controls for tenant applications

## Attacker mindset
An attacker would recognize Points.com as a high-value target due to its role as central infrastructure for dozens of airline and hotel reward programs. The discovery of path traversal would immediately suggest further enumeration. The combination of exposed customer identifiers with authorization bypass would enable account takeover and fraud at scale. Finding leaked tenant credentials would represent complete compromise of the airline/hotel on whose behalf Points.com operates, enabling admin-level actions.

## Defensive takeaways
- Implement strict input validation and canonicalization to prevent path traversal attacks; use allowlist-based access controls
- Enforce multi-factor authentication requirements beyond just surname + rewards number; validate requests through additional context or challenge-response
- Never expose API credentials or secrets in client-accessible endpoints; use secure credential management systems and rotate regularly
- Implement proper authorization checks at API layer; verify user identity through secure session tokens rather than easily-guessable identifiers
- Apply principle of least privilege to all API endpoints; restrict tenant credentials to minimal necessary permissions
- Conduct regular security audits of sensitive endpoints handling customer data or financial transactions
- Implement rate limiting and anomaly detection on data access patterns to detect enumeration attacks
- Encrypt sensitive data at rest (credit cards, addresses); implement PII masking in logs and responses

## Variant hunting
Search for similar issues in other loyalty/rewards platforms, payment processors, and multi-tenant SaaS backends. Look for: (1) Other instances of path traversal on internal APIs, (2) Authorization bypass patterns where user identity relies on public/guessable identifiers, (3) Exposed API credentials in client-accessible endpoints (check JavaScript, error messages, responses), (4) Admin panels or privileged endpoints lacking proper authentication, (5) Similar multi-tenant architectures where tenant credentials could be exposed

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Reconnaissance via API Discovery
- T1552 - Unsecured Credentials
- T1110 - Brute Force / Credential Enumeration
- T1078 - Valid Accounts / Unauthorized Access
- T1556 - Modify Authentication Process
- T1530 - Data from Cloud Storage
- T1087 - Account Discovery

## Notes
This writeup demonstrates the critical importance of securing multi-tenant platforms handling financial/rewards data. The vulnerability chain shows how initial reconnaissance (path traversal) enables exploitation of downstream authorization flaws. Points.com's rapid response (sub-60 minute patches) is exemplary incident response. The involvement of multiple security researchers (Sam Curry, Ian Carroll, Shubham Shah) suggests coordinated responsible disclosure. No specific bounty amount disclosed, which is common in high-profile reports where companies may offer discretionary rewards. The May 2nd 2023 credential exposure on Virgin's domain is particularly severe as it could enable impersonation of the airline entity itself.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
