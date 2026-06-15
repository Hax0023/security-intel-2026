# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** PayPal (via HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Account Takeover, Privilege Escalation
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account secondary user management API allowed attackers to enumerate and takeover any secondary user account by manipulating incremental user IDs. Since secondary users could be assigned money transfer privileges, successful exploitation enabled unauthorized fund transfers from victim business accounts.

## Attack scenario (step by step)
1. Attacker creates a secondary user account on their own PayPal business account and captures the PUT request to the /businessmanage/users/api/v1/users endpoint
2. Attacker identifies that the 'id' parameter in the API request (e.g., 4446113495) is sequential and enumerable across all secondary users
3. Attacker increments the ID value to enumerate secondary user accounts from victim business accounts (e.g., 4446113496, 4446113497, etc.)
4. Attacker sends requests with modified sequential IDs, causing victim secondary accounts to appear in their own Manage Users section
5. Attacker uses the management interface to reset passwords for enumerated secondary accounts with money transfer privileges
6. Attacker logs into compromised secondary accounts and executes unauthorized money transfers from victim business accounts to attacker-controlled accounts

## Root cause
PayPal failed to properly validate that the user making API requests had authorization to modify the specified secondary user accounts. The use of sequential, enumerable IDs without access control checks allowed attackers to reference and modify arbitrary secondary users across different business accounts.

## Attacker mindset
The attacker recognized that API endpoints often contain object identifiers and systematically tested whether these identifiers were predictable and unprotected. By understanding that secondary user IDs were sequential numbers, the attacker realized they could brute-force enumerate all users and modify their permissions, gaining access to privileged accounts with financial transaction capabilities.

## Defensive takeaways
- Implement strict access control checks on all API endpoints - verify the requesting user has explicit authorization to modify the requested resource
- Use non-sequential, non-enumerable identifiers (UUIDs/GUIDs) for sensitive objects instead of incremental integers
- Validate that the requested resource belongs to the authenticated user's organization/business account
- Implement rate limiting on API endpoints that enumerate or modify user accounts
- Log and monitor API requests that attempt to access resources outside the authenticated user's scope
- Apply principle of least privilege - secondary users should only be able to modify their own account details, not other accounts
- Conduct regular security audits of API endpoints, especially those handling sensitive operations like user management and financial transactions
- Implement multi-factor authentication for secondary account access and password changes

## Variant hunting
['Check if other PayPal management endpoints use sequential IDs without proper authorization checks (e.g., invoice management, payment processing rules)', 'Test whether the IDOR vulnerability extends to reading sensitive account data beyond just modification', 'Investigate if the vulnerability affects merchant API accounts or other business account types', 'Look for similar patterns in API endpoints for managing business account permissions and roles', 'Test whether the incremental ID pattern exists in other areas such as business profile management or payment method administration']

## MITRE ATT&CK
- T1190
- T1550
- T1556
- T1199
- T1078
- T1552

## Notes
This vulnerability is particularly severe because PayPal business accounts are high-value targets used by millions of organizations worldwide. The combination of IDOR with privilege escalation and financial transaction capabilities created a critical exploitation path. The sequential ID enumeration was the key insight that made this vulnerability practical to exploit at scale. PayPal's remediation was successful with no evidence of real-world abuse detected.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
