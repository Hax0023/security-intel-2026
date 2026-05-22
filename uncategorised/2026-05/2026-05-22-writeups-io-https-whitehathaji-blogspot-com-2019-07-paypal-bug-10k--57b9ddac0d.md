# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Account Takeover, Privilege Escalation, Enumeration
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account management API allowed attackers to enumerate and takeover secondary user accounts by manipulating an incremental user ID parameter in PUT requests. By gaining control of secondary accounts with 'Transfer Money' privileges, attackers could execute unauthorized money transfers from victim PayPal business accounts.

## Attack scenario (step by step)
1. Attacker creates a secondary user account on their own PayPal business account to understand the API structure and identify the user ID parameter
2. Attacker captures the PUT request to /businessmanage/users/api/v1/users endpoint and identifies that the 'id' parameter in the accessPoint object is sequential and enumerable
3. Attacker systematically increments the user ID values to enumerate secondary user accounts belonging to other business accounts
4. For each discovered secondary account ID, attacker modifies the PUT request to add that ID to their own business account's user management section
5. Attacker resets the password of a victim secondary account with 'Transfer Money' privilege through the Manage Users interface
6. Attacker logs in as the compromised secondary user and executes unauthorized money transfers from the victim's PayPal business account

## Root cause
PayPal failed to implement proper authorization checks on the /businessmanage/users/api/v1/users endpoint. The API did not verify that the authenticated user owned or had permission to modify the secondary user accounts referenced by the user IDs in the request. Additionally, the use of sequential, easily enumerable numeric IDs without access control made the vulnerability trivial to exploit.

## Attacker mindset
An attacker would recognize that business accounts with delegated secondary user access present a lucrative target, especially when those secondary users have financial transaction privileges. The sequential ID pattern is immediately apparent and suggests insufficient access control design. The attacker would focus on high-value business accounts where money transfer privileges are assigned, maximizing the financial impact of account compromise.

## Defensive takeaways
- Implement strict server-side authorization checks on all API endpoints to verify the authenticated user has permission to access/modify the requested resources
- Use non-sequential, non-predictable identifiers (UUID/GUID) for sensitive resources instead of enumerable numeric IDs
- Apply principle of least privilege: verify ownership and role-based access for every secondary user management operation
- Implement rate limiting and monitoring on account enumeration patterns, especially within the user management API
- Add multi-factor authentication and additional verification steps before allowing critical operations like password resets on secondary accounts
- Conduct regular security audits of API endpoints, particularly those handling account management and privilege escalation
- Log and alert on suspicious patterns such as bulk user ID enumeration or cross-account access attempts
- Implement CSRF protection and transaction verification for high-risk operations like password changes

## Variant hunting
['Check other PayPal endpoints handling business account management for similar IDOR vulnerabilities with numeric user/business IDs', 'Test payment recipient management APIs for similar sequential ID enumeration and access control bypasses', 'Investigate account permission modification endpoints to see if similar IDOR patterns exist for role/privilege assignments', 'Look for other business account features (invoicing, reporting, integrations) that may use similar enumerable ID schemes without proper access control', 'Test whether organization/workspace APIs in other fintech platforms use similar patterns', 'Check for account linking/delegation features that might have similar IDOR issues with cross-account access']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (API exploitation)
- T1110 - Brute Force (enumeration of sequential IDs)
- T1078 - Valid Accounts (account takeover of secondary users)
- T1556 - Modify Authentication Process (password reset without authorization)
- T1098 - Account Manipulation (privilege escalation and account modification)
- T1087 - Account Discovery (enumeration of business accounts via IDOR)

## Notes
This vulnerability demonstrates a critical gap in authorization logic where an endpoint failed to verify ownership before allowing modifications. The use of sequential numeric IDs compounded the issue by making enumeration trivial. The financial impact is severe as it directly enables unauthorized money transfers. PayPal's fix likely involved implementing proper ownership verification and potentially moving to non-sequential identifiers. The $10K bounty reflects the critical severity and high financial impact of the vulnerability.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
