# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Account Takeover, Privilege Escalation, Unauthorized Financial Transaction
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
A critical IDOR vulnerability in PayPal's secondary user management API allowed attackers to enumerate and takeover any secondary business account by manipulating an incremental user ID parameter. Once compromised, secondary accounts with 'Transfer Money' privileges could be used to authorize unauthorized fund transfers from victim business accounts to attacker-controlled accounts.

## Attack scenario (step by step)
1. Attacker creates their own PayPal business account and a secondary user account to analyze the API endpoint structure
2. Attacker captures the PUT request to /businessmanage/users/api/v1/users containing the secondary user ID (e.g., 4446113495)
3. Attacker identifies that user IDs are incremental numeric values with no authorization checks, allowing enumeration
4. Attacker systematically increments the user ID parameter to discover secondary accounts belonging to victim business accounts
5. Attacker sends API requests to associate discovered secondary user accounts to their own business account interface
6. Attacker changes the password of a compromised secondary account with 'Transfer Money' privileges and executes unauthorized fund transfers

## Root cause
PayPal's API endpoint failed to implement proper authorization checks when managing secondary user accounts. The endpoint accepted user ID modifications without verifying the requester's ownership or authorization over the target secondary account, relying on predictable, sequential numeric IDs that enabled enumeration attacks.

## Attacker mindset
The attacker demonstrated thorough reconnaissance by creating test accounts to understand the system architecture, then recognized the vulnerability pattern (IDOR with enumerable IDs) and escalated it from account enumeration to full account takeover and financial fraud capability. The attacker focused on identifying high-value secondary accounts with specific privileges (money transfer) to maximize financial impact.

## Defensive takeaways
- Implement strict authorization checks on all API endpoints - verify the authenticated user has explicit permission to modify each specific resource
- Replace sequential numeric IDs with non-predictable identifiers (UUIDs v4) or implement proper ID obfuscation
- Use role-based access control (RBAC) to validate that permission modification requests are from account owners only
- Enforce request validation to ensure secondary user modifications can only be performed by authorized primary account holders
- Implement comprehensive audit logging for all account and permission changes, especially for secondary user modifications
- Add rate limiting and anomaly detection for bulk enumeration attempts or rapid ID iteration patterns
- Conduct security testing focused on parameter manipulation in all user management APIs
- Implement API-level access controls that verify the requesting account owns the resource being modified

## Variant hunting
['Check for similar IDOR vulnerabilities in other PayPal API endpoints that manage user roles, permissions, or delegated access', 'Test other PayPal business features for sequential ID enumeration (payment methods, funding sources, invoice IDs)', 'Look for IDOR in account linking/multi-user management across other financial platforms (Stripe, Square, Wise)', 'Examine API endpoints for changing security questions, recovery email, or authentication methods using IDOR', 'Hunt for enumerable IDs in business account transfer/settlement endpoints', 'Test whether compromised secondary accounts can modify primary account settings or create new secondary accounts']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1136 - Create Account
- T1087 - Account Discovery
- T1098 - Account Manipulation
- T1080 - Privilege Escalation
- T1185 - Unsecured Credentials
- T1550 - Use Alternate Authentication Material

## Notes
This vulnerability had severe business impact as it could enable mass account takeover of PayPal business accounts and direct financial fraud. The fix required changes to API authorization logic rather than simple parameter validation. The researcher demonstrated excellent bug bounty methodology by providing clear steps to reproduce and articulating the business impact. PayPal confirmed no evidence of active exploitation before remediation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
