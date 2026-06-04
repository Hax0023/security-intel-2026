# Leaked Secrets and Unlimited Miles: Hacking Points.com Rewards Platform

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** points.com (Bug Bounty Program)
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln types:** Path Traversal, Authorization Bypass, Credential Disclosure, API Authentication Bypass, Broken Access Control, Sensitive Data Exposure
- **Category:** uncategorised
- **Writeup:** https://samcurry.net/points-com/

## Summary
Researchers discovered multiple critical vulnerabilities in points.com, the backend provider for major airline and hotel rewards programs, affecting 22 million customer records. Vulnerabilities included unauthenticated path traversal to order records, authorization bypass allowing points transfers with minimal information, and leaked API credentials for tenant programs like Virgin Rewards. The vulnerabilities would have enabled account takeover, points theft, unauthorized administrative access, and customer data exposure.

## Attack scenario (step by step)
1. Attacker discovers unauthenticated path traversal endpoint and queries the internal API to enumerate 22 million order records containing customer PII and reward numbers
2. Attacker extracts customer surnames and reward point numbers from the leaked data
3. Attacker uses authorization bypass vulnerability with only surname and rewards number to generate full account authentication tokens
4. Attacker uses generated tokens to transfer reward points to their own account, access customer billing/contact information, and view order history
5. Attacker discovers leaked Virgin Rewards API credentials (macID and macKey) exposed on points.com-hosted website
6. Attacker authenticates as Virgin Airlines to core API and modifies customer accounts, adds/removes points, and changes rewards program settings

## Root cause
['Lack of proper path traversal input validation and filtering on API endpoints', 'Insufficient authorization checks relying on easily obtainable public information (surname, rewards number) instead of cryptographic tokens', 'Credentials embedded in client-side code or frontend configuration exposed without proper access controls', 'Missing authentication requirements on sensitive endpoints', 'Inadequate API signature validation and token generation mechanisms']

## Attacker mindset
An attacker would recognize that rewards platforms are high-value targets due to the monetary value of points and access to customer financial data. The low barrier to entry (only needing publicly available or easily obtained information like surname and rewards number) would be immediately exploitable at scale. The attacker would first perform reconnaissance to find unauthenticated endpoints, extract maximum customer data, then escalate to full account compromise and administrative access for broader impact and persistence.

## Defensive takeaways
- Implement strict input validation and use allowlist patterns for API paths to prevent directory traversal
- Require strong authentication factors beyond easily guessable or publicly available information (rewards number, surname)
- Never embed API credentials or secrets in client-side code; use server-side token generation and rotation
- Implement proper authorization checks on every endpoint verifying user identity before granting access to sensitive operations
- Use cryptographically signed tokens with appropriate expiration times for API authentication
- Conduct regular security audits of all API endpoints, especially those handling financial transactions or customer data
- Implement rate limiting and anomaly detection on points transfer operations
- Separate user-facing APIs from administrative APIs with distinct authentication mechanisms
- Implement comprehensive access logging for all sensitive operations
- Use infrastructure-level controls to prevent exposure of sensitive configuration and credentials

## Variant hunting
['Search for similar path traversal patterns on other reward/loyalty platform APIs', 'Audit other airlines/hotel chains using points.com backend for similar authorization bypass patterns', 'Check for embedded credentials in JavaScript files, API responses, or configuration endpoints across loyalty platforms', 'Test for authorization bypass using minimal information on competitor reward programs (Marriott Bonvoy, Hilton Honors, etc.)', 'Fuzz API endpoints for directory traversal with various encoding methods (../, ..%2f, ..%252f, etc.)', 'Look for tenant API credential exposure in publicly hosted reward program frontends', 'Enumerate subdomains and test for unauthenticated API access across points.com infrastructure', 'Check for improper CORS configurations allowing cross-origin API access', 'Test for JWT token weaknesses or predictable token generation in authorization bypass scenarios']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (path traversal, auth bypass)
- T1110 - Brute Force (token enumeration with minimal information)
- T1212 - Exploitation for Credential Access (credential disclosure in frontend)
- T1526 - Enumerate External Accounts (enumeration of 22M customer records)
- T1087 - Account Discovery (customer account enumeration via API)
- T1059 - Command and Scripting Interpreter (API-based account manipulation)
- T1550 - Use Alternate Authentication Material (using leaked API credentials)
- T1078 - Valid Accounts (generating unauthorized authorization tokens)
- T1567 - Exfiltration Over Web Service (data extraction via API queries)

## Notes
This is a high-impact real-world vulnerability chain affecting critical financial infrastructure. The rapid response from points.com (under 10 minutes for initial reports, 1 hour for final credential disclosure) demonstrates strong security incident response capabilities. The vulnerability chain showcases how multiple seemingly low-severity issues compound into critical system compromise. All vulnerabilities were patched and remediable; no active exploitation was confirmed. The writeup provides excellent technical depth for each vulnerability class.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
