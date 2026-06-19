# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Privilege Escalation, Account Takeover
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's secondary user management API allowed attackers to enumerate and take over any secondary user account of PayPal business accounts by modifying user IDs in PUT requests. By taking over secondary accounts with money transfer privileges, attackers could perform unauthorized money transfers from victim business accounts to attacker-controlled accounts.

## Attack scenario (step by step)
1. Attacker identifies the API endpoint /businessmanage/users/api/v1/users and the pattern of incremental, enumerable user IDs
2. Attacker captures and analyzes a legitimate PUT request containing a secondary user ID (e.g., 4446113495)
3. Attacker modifies the user ID in the request to target a victim's secondary user account by incrementing the ID value
4. The API accepts the request without proper authorization checks, adding the victim's secondary account to the attacker's secondary user list
5. Attacker uses the Manage Users section to change the password of the compromised secondary account
6. Attacker logs into the victim's secondary account and exploits the 'Transfer Money' privilege to move funds to their own account

## Root cause
PayPal failed to implement proper authorization checks on the secondary user management API endpoint. The API lacked validation to ensure that only account owners could modify their own secondary users, relying solely on predictable, sequential user IDs without access control verification.

## Attacker mindset
The attacker methodically identified an enumerable ID pattern and recognized that lack of authorization checks would allow lateral privilege escalation across any business account. They understood that secondary accounts often have financial privileges, making this vulnerability particularly lucrative for financial fraud.

## Defensive takeaways
- Implement proper authorization checks on all API endpoints to verify user ownership before allowing modifications
- Use non-sequential, non-enumerable identifiers (UUID/GUID) instead of incremental IDs for sensitive objects
- Apply principle of least privilege - validate that requesters can only access/modify their own resources
- Implement server-side session validation to ensure operations are performed within the authorized account context
- Conduct security code reviews focusing on IDOR vulnerabilities in multi-user account management features
- Monitor and alert on suspicious secondary user modifications or enumeration attempts

## Variant hunting
['Check other PayPal administrative endpoints for similar IDOR patterns in user/account management', 'Test permission modification endpoints with modified user IDs across different ID ranges', 'Examine API requests for other sequential ID parameters in business account management features', 'Test whether other sensitive operations (delete, suspend, role changes) suffer from same IDOR weakness', 'Verify if individual account access controls are properly enforced on financial transaction APIs']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1098 - Account Manipulation
- T1550 - Use Alternate Authentication Material
- T1021 - Remote Services

## Notes
This was a high-impact vulnerability affecting millions of PayPal business accounts worldwide. The incremental ID enumeration made it trivially exploitable at scale. PayPal confirmed no evidence of active exploitation. The researcher demonstrated strong understanding of authorization bypass techniques and financial fraud impact assessment.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
