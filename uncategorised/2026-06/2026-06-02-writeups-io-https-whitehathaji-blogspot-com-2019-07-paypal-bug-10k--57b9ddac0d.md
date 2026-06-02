# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Account Takeover, Privilege Escalation, Unauthorized Financial Transaction
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account management API allowed attackers to enumerate and takeover any secondary user account by manipulating an incremental user ID parameter. By gaining control of secondary accounts with money transfer privileges, attackers could perform unauthorized fund transfers from victim PayPal business accounts.

## Attack scenario (step by step)
1. Attacker identifies the secondary user management endpoint at /businessmanage/users/api/v1/users with an enumerable numeric ID parameter
2. Attacker captures and modifies a PUT request used to update secondary user permissions, changing the target user ID from their own to an incremental value
3. Attacker systematically enumerates sequential user IDs to discover secondary accounts belonging to other business account holders
4. Attacker gains visibility of victim secondary accounts in their own Manage Users section by sending crafted requests with enumerated IDs
5. Attacker uses the management interface to reset passwords on victim secondary accounts with 'Transfer Money' privilege level
6. Attacker logs into compromised secondary account and executes unauthorized money transfers from victim's PayPal business account

## Root cause
Insufficient access control validation on the secondary user management API endpoint. The API failed to verify that the requesting user had authorization to modify secondary accounts belonging to other business account owners. Additionally, the use of an easily enumerable, sequential numeric ID without proper authorization checks enabled account enumeration.

## Attacker mindset
Target high-value business accounts that utilize secondary users with financial transaction privileges. Systematically enumerate account IDs to identify secondary accounts, then leverage weak access controls to gain administrative control and execute profitable unauthorized transactions with minimal detection risk.

## Defensive takeaways
- Implement proper authorization checks on all API endpoints - verify the authenticated user owns/controls the resource being modified before allowing changes
- Replace enumerable numeric IDs with non-sequential, unpredictable identifiers (UUIDs) for sensitive resources
- Add server-side validation that the account being modified belongs to the authenticated user's organization
- Implement comprehensive audit logging for all secondary user permission changes and password modifications
- Require multi-factor authentication or email verification for critical actions like secondary user password resets
- Apply principle of least privilege - restrict secondary user creation and management capabilities
- Conduct regular access control audits across all admin/management API endpoints
- Implement rate limiting on API endpoints that could be used for enumeration attacks

## Variant hunting
['Check other PayPal management endpoints (/businessmanage/*, /account/*, /settings/*) for similar IDOR patterns with numeric IDs', 'Examine other financial transaction platforms (Stripe, Square, etc.) for similar secondary user management IDOR vulnerabilities', 'Test payment processor APIs for enumerable resource IDs in employee/team management sections', 'Look for IDOR in API endpoints that modify user permissions, roles, or delegated access', 'Investigate business account admin panels across fintech platforms for sequential ID patterns in user management', 'Test for authorization bypasses in endpoints that interact with account privileges or financial controls']

## MITRE ATT&CK
- T1190
- T1589
- T1592
- T1110
- T1078
- T1098
- T1021
- T1185

## Notes
The vulnerability's severity was amplified by PayPal's business model where secondary accounts can hold significant financial transaction privileges. The incremental nature of the user ID made systematic enumeration trivial. Paypal confirmed no evidence of exploitation. This is a textbook IDOR case demonstrating why sequential IDs should never be used for authorization decisions without proper access control validation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
