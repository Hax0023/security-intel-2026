# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Account Takeover, Privilege Escalation, Insufficient Authorization Checks
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account secondary user management API allowed attackers to enumerate and take over any secondary user account by predicting sequential user IDs. By modifying the user ID in PUT requests to /businessmanage/users/api/v1/users, attackers could add victim secondary accounts to their own business account and change credentials, potentially enabling unauthorized money transfers from victim business accounts.

## Attack scenario (step by step)
1. Attacker identifies the sequential ID pattern used for secondary users (e.g., 4446113495) from their own account
2. Attacker captures the PUT request used to manage secondary user permissions in their business account
3. Attacker modifies the incremental user ID in the request to enumerate other secondary user accounts (4446113496, 4446113497, etc.)
4. Attacker discovers victim secondary user accounts and adds them to their own business account through the vulnerable API
5. Attacker changes the password of the compromised secondary user via the Manage Users section
6. Attacker logs into the victim's secondary account and executes unauthorized money transfers if the account has 'Transfer Money' privileges

## Root cause
PayPal's secondary user management API failed to properly validate authorization before allowing modifications to user accounts. The API accepted user IDs in requests without verifying that the requesting account had legitimate ownership or control over the targeted user. Additionally, sequential/enumerable user IDs were used without rate limiting or detection mechanisms.

## Attacker mindset
An attacker would recognize the opportunity to enumerate sequential IDs and test them against the API to discover secondary accounts. They would understand that secondary user accounts often have elevated privileges (like money transfer) and that compromise of these accounts could lead to direct financial theft. The attacker would methodically test the API's authorization logic to bypass access controls.

## Defensive takeaways
- Implement strict authorization checks on all API endpoints - verify the requesting user owns/manages the target object before allowing modifications
- Use non-sequential, non-enumerable identifiers (UUIDs, cryptographically random tokens) instead of incremental IDs
- Add rate limiting and monitoring for enumeration attempts on ID sequences
- Implement proper access control lists (ACLs) that verify user-account relationships server-side
- Add audit logging and alerting for suspicious account modifications or privilege changes
- Validate that secondary user modifications originate from the correct business account context
- Implement CSRF protections on state-changing operations
- Regularly test APIs for IDOR vulnerabilities in sensitive operations like account management

## Variant hunting
['Search for other PayPal API endpoints that accept user/account IDs and test them for IDOR patterns', 'Test permission modification endpoints with IDs from different business accounts', 'Examine other financial account management systems for similar sequential ID patterns in secondary user management', 'Test bulk operations or batch user management APIs for authorization bypass', 'Look for similar patterns in payment processor competitors (Stripe, Square, etc.)', 'Test role creation and assignment endpoints for IDOR vulnerabilities', 'Enumerate webhook configuration and API key management endpoints']

## MITRE ATT&CK
- T1190
- T1110
- T1078
- T1547
- T1556
- T1078.002

## Notes
This vulnerability represents a high-impact account takeover with direct financial implications. The sequential nature of the user IDs made exploitation straightforward and reliable. The fact that secondary accounts often have elevated privileges (transfer money) amplified the risk significantly. PayPal's remediation appears to have involved implementing proper authorization checks and potentially transitioning to non-enumerable identifiers. The $10K bounty reflects the critical severity and financial impact potential.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
