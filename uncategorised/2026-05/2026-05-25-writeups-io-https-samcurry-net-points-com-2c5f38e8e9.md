# Leaked Secrets and Unlimited Miles: Hacking the Largest Airline and Hotel Rewards Platform (Points.com)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Points.com
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Directory Traversal, Authorization Bypass, Credential Exposure, API Authentication Bypass, Broken Access Control, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Security researchers discovered multiple critical vulnerabilities in Points.com, the backend provider for airline and hotel rewards programs, affecting approximately 22 million customer records. The vulnerabilities enabled unauthorized access to sensitive customer data (names, addresses, credit cards, emails, phone numbers), point transfers, and administrative functions. All issues were promptly patched after responsible disclosure between March-May 2023.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated HTTP path traversal endpoint exposed on points.com infrastructure
2. Attacker queries the internal API to access 22 million order records containing PII, partial credit cards, and reward point numbers
3. Attacker uses exposed customer surname and reward number from traversal vulnerability to bypass authorization checks
4. Attacker generates forged authorization tokens allowing full account management and point transfers to attacker-controlled accounts
5. Attacker discovers leaked tenant credentials (macID/macKey) for Virgin Rewards API endpoint on points.com-hosted website
6. Attacker authenticates to core points.com API as Virgin Airlines, accessing administrative functions to modify accounts and issue fraudulent points

## Root cause
['Insufficient input validation on API endpoints allowing path traversal without authentication', 'Broken authorization logic relying solely on easily-guessable parameters (surname + reward number) for token generation', 'Exposure of cryptographic credentials in client-side code or unsecured endpoints', 'Lack of proper API authentication mechanisms and tenant isolation', 'Missing authentication checks on internal API endpoints', 'Inadequate secrets management allowing credential leakage in web-accessible resources']

## Attacker mindset
An attacker would recognize that loyalty/rewards platforms are high-value targets due to direct financial impact (point transfers = money), large customer databases, and potential administrative access. By chaining multiple vulnerabilities (traversal → data enumeration → weak authorization → credential abuse), an attacker could systematically escalate from information disclosure to full platform compromise with minimal effort required.

## Defensive takeaways
- Implement strict input validation and canonicalization to prevent path traversal attacks on all endpoints
- Enforce strong authentication on all APIs; never rely on single user attributes (name/ID) for authorization decisions
- Implement proper access control checks before exposing sensitive endpoints; require authentication tokens with proper validation
- Never expose secrets, API keys, or cryptographic material in frontend code, logs, or configuration files
- Conduct regular security audits of API endpoints, especially those handling sensitive financial data
- Implement rate limiting and anomaly detection on reward point transfer operations
- Use secrets management systems for credential storage; rotate tenant credentials regularly
- Segment tenant data and enforce isolation at the database/API layer
- Implement comprehensive logging and monitoring for sensitive operations
- Establish clear vulnerability disclosure policies and SLAs for response

## Variant hunting
['Search for similar path traversal patterns in other points.com subdomains and API endpoints', 'Test other loyalty program integrations for exposed tenant credentials in web-accessible endpoints', 'Enumerate other reward platforms for weak authorization based on enumerable customer identifiers', 'Fuzz API endpoints with path traversal payloads (../, ..\\, encoded variants, unicode normalization)', 'Review JavaScript bundles and static assets for accidentally-committed API credentials or configuration', 'Test authorization bypass using parameter tampering (modifying user IDs, reward numbers in requests)', 'Scan for information disclosure in error messages and response headers revealing API structure', 'Investigate other tenant integrations for similar credential exposure vulnerabilities', 'Check deprecated or historical API versions for unpatched vulnerabilities']

## MITRE ATT&CK
- T1190
- T1040
- T1526
- T1087
- T1557
- T1021
- T1078
- T1592
- T1652
- T1526

## Notes
This is a high-quality security research example demonstrating responsible disclosure with excellent response times from vendor (under 1 hour). The vulnerability chain is sophisticated, combining multiple attack vectors (traversal → enumeration → authorization bypass → credential reuse) that compound severity. The researcher responsibly demonstrated the impact without causing harm. Points.com's rapid response (taking sites offline within minutes, patching within hours) represents best-in-class incident response. The scale (22M records, multiple airline programs) and severity (direct financial impact via point transfers + admin access) make this Critical. No bounty amount disclosed suggests this may have been reported through private channels or formal program.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
