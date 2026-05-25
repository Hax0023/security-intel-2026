# PayPal Secondary User Account Takeover via IDOR Leading to Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** Critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Controls, Account Takeover, Privilege Escalation
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account user management API allowed attackers to enumerate and take over secondary user accounts across any PayPal business account. By exploiting an incremental and predictable secondary user ID in the `/businessmanage/users/api/v1/users` endpoint, an attacker could modify permissions and reset passwords for secondary accounts with money transfer privileges, enabling unauthorized fund transfers from victim business accounts.

## Attack scenario (step by step)
1. Attacker identifies the IDOR vulnerability in the secondary user management API by observing that user IDs are sequential numeric values (e.g., 1660971175791245038)
2. Attacker creates their own PayPal business account and adds a secondary user to understand the API request structure for user management
3. Attacker captures and modifies a PUT request to /businessmanage/users/api/v1/users, changing the secondary user ID from their own account to an enumerated target ID (e.g., incrementing from 4446113495 to 4446113496)
4. System fails to validate that the attacker has authorization to modify the target secondary user account, allowing the attacker to associate victim secondary accounts with their own business account
5. Attacker gains visibility of victim secondary accounts in their Manage Users section and changes the password for a secondary account with 'SEND_MONEY' privilege
6. Attacker logs into the compromised secondary account and transfers funds from the victim PayPal business account to an attacker-controlled account

## Root cause
PayPal failed to implement proper authorization checks on the user management API endpoint. The API did not verify that the requesting user had legitimate ownership or administrative rights over the secondary user account being modified. Additionally, the use of sequential numeric IDs made enumeration trivial, and the API trusted client-provided data without server-side validation of access rights.

## Attacker mindset
An attacker would recognize that business account secondary users are attractive targets due to the financial privileges often granted to them. By discovering the IDOR vulnerability, the attacker realized they could conduct large-scale account takeovers with minimal effort, targeting multiple business accounts simultaneously through simple ID enumeration. The financial motivation is direct—compromised 'Transfer Money' privileged accounts provide immediate access to victim funds.

## Defensive takeaways
- Implement server-side authorization checks on all API endpoints—verify that the authenticated user has explicit rights to access/modify the requested resource, not just that they are authenticated
- Avoid sequential or predictable resource identifiers; use UUIDs or cryptographically random values for sensitive resources like user accounts
- Apply the principle of least privilege—secondary user accounts should have granular, role-based access controls with explicit auditing of privilege assignments
- Implement comprehensive API rate limiting and anomaly detection to identify patterns of ID enumeration or bulk account access attempts
- Add multi-factor authentication requirements for sensitive operations like password resets and money transfers, especially from business accounts
- Maintain detailed audit logs of all user management operations and implement alerts for mass modifications or unusual access patterns
- Conduct regular security testing and code reviews specifically targeting authorization logic in administrative and API endpoints
- Implement request signing or CSRF tokens to prevent unauthorized API modifications from cross-origin or spoofed requests

## Variant hunting
Similar IDOR vulnerabilities likely exist in other PayPal administrative functions such as: (1) business account role management, (2) API signature and permission assignment endpoints, (3) webhook configuration management, (4) settlement account modifications, (5) invoice and invoice template management, (6) payout recipient list management. Any endpoint that references business account sub-resources with numeric or sequential identifiers should be tested for authorization bypass. Check for similar patterns in other financial platforms' user and account management APIs.

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1078 Valid Accounts
- T1556 Modify Authentication Process
- T1098 Account Manipulation
- T1087 Account Discovery
- T1110 Brute Force

## Notes
This vulnerability demonstrates a critical gap in authorization architecture where authentication (proving who you are) was present but authorization (verifying what you can do) was absent. The researcher's writeup clearly documents the enumeration method and privilege escalation path. PayPal's response indicating no evidence of abuse suggests the vulnerability may have existed for an extended period. The $10K bounty reflects the high severity and direct financial impact potential. The vulnerability is particularly dangerous because it operates at the API level, allowing programmatic large-scale exploitation rather than requiring manual per-account attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
