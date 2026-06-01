# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** Critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Account Takeover, Privilege Escalation, Unauthorized Money Transfer
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
A critical IDOR vulnerability in PayPal's business account secondary user management API allowed attackers to enumerate and takeover any secondary user account by manipulating an incremental numeric user ID. Compromised secondary accounts with 'Transfer Money' privileges enabled unauthorized fund transfers from victim business accounts to attacker-controlled accounts.

## Attack scenario (step by step)
1. Attacker creates a secondary user account on their own PayPal business account and captures the PUT request to /businessmanage/users/api/v1/users containing their secondary user ID
2. Attacker observes that the second 'id' parameter (e.g., 4446113495) is a sequential numeric identifier tied to specific secondary user accounts
3. Attacker modifies the numeric ID in the PUT request to enumerate adjacent IDs (e.g., 4446113496, 4446113497) and sends crafted requests
4. Each enumerated secondary user account becomes visible in the attacker's 'Manage Users' section, bypassing ownership verification
5. Attacker uses the management interface to change the password of a victim secondary account that possesses 'Transfer Money' privileges
6. Attacker logs into the compromised secondary account and initiates unauthorized money transfers from the victim's PayPal business account

## Root cause
PayPal failed to implement proper authorization checks on the secondary user management API endpoint. The API accepted modifications to secondary user accounts based solely on an incremental numeric ID without verifying that the requesting user actually owned or had legitimate access to the target account. The client-side account ID parameter lacked backend validation against the authenticated user's business account ownership.

## Attacker mindset
The researcher recognized that business secondary accounts are high-value targets due to delegated financial privileges. By identifying the enumerable nature of the secondary user ID and testing object reference manipulation, the attacker realized they could systematically discover and compromise accounts belonging to any PayPal business user. The focus on 'Transfer Money' privilege escalation demonstrates understanding of monetizable attack paths.

## Defensive takeaways
- Implement strict authorization checks on all API endpoints: verify that the authenticated user owns or has legitimate access to any resource they attempt to modify
- Avoid using sequential or easily guessable identifiers for sensitive objects; use cryptographically random UUIDs/GUIDs instead
- Employ role-based access control (RBAC) to ensure secondary users can only manage accounts within their business account scope
- Add audit logging for all secondary user account modifications including password changes and privilege alterations
- Implement rate limiting and anomaly detection on account management operations to flag unusual enumeration patterns
- Require multi-factor authentication or additional verification for sensitive operations like password resets on accounts with financial privileges
- Conduct regular security testing focusing on business account management workflows where privilege delegation occurs

## Variant hunting
['Test other PayPal business management endpoints for similar IDOR patterns in user, role, or permission management APIs', 'Enumerate IDs in payment recipient lists, webhook configurations, and API signature management endpoints', 'Check if other numeric identifiers (account IDs, transaction IDs, merchant IDs) exhibit similar sequential patterns and lack proper authorization checks', 'Test business account bulk operations and exports that might reveal or allow manipulation of secondary user accounts', 'Investigate whether secondary account compromise could lead to API credential theft or OAuth token generation for persistence']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1078: Valid Accounts
- T1550: Use Alternate Authentication Material
- T1098: Account Manipulation
- T1556: Modify Authentication Process
- T1021: Remote Services

## Notes
This vulnerability represents a complete business account compromise vector. The severity justifies the $10K bounty given the potential for mass unauthorized fund transfers affecting millions of PayPal business users. The researcher's clear documentation of incremental ID enumeration and cross-account privilege modification demonstrates excellent vulnerability analysis. PayPal's confirmation of 'no evidence of abuse' suggests either rapid patching or limited attacker knowledge of this weakness. The vulnerability highlights the dangers of relying on numeric identifiers for access control in financial systems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
