# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** PayPal (via HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Privilege Escalation, Account Takeover, Horizontal Authorization Bypass
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
A critical IDOR vulnerability in PayPal's business account management API allowed attackers to enumerate and takeover any secondary user account through predictable, sequential user IDs. By exploiting this flaw, an attacker could assume control of secondary accounts with elevated privileges (such as money transfer permissions) and perform unauthorized financial transactions from victim business accounts.

## Attack scenario (step by step)
1. Attacker identifies that the secondary user management endpoint uses sequential, enumerable IDs in the format /businessmanage/users/api/v1/users with a numeric ID parameter (e.g., 4446113495)
2. Attacker discovers the IDOR vulnerability by modifying the ID parameter in PUT requests used to edit user permissions, finding that authorization checks are insufficient
3. Attacker enumerates sequential ID values (e.g., 4446113496, 4446113497, etc.) to discover secondary user accounts belonging to other business owners
4. Attacker uses the endpoint to modify permissions or reset passwords for enumerated secondary user accounts, achieving complete account takeover
5. Attacker gains access to a secondary account with 'Transfer Money' privilege and logs in to the compromised account
6. Attacker performs unauthorized money transfers from the victim's PayPal business account to attacker-controlled accounts

## Root cause
PayPal failed to implement proper authorization checks on the user management API endpoint. The system did not validate that the requester had permission to modify other business owners' secondary user accounts. Additionally, the use of sequential, enumerable numeric IDs without access control enabled attackers to discover and enumerate all secondary user IDs across the platform.

## Attacker mindset
An attacker would recognize that business accounts hold significant financial value and that secondary users often have delegated permissions for operational tasks like money transfers. By discovering the IDOR vulnerability, the attacker realizes they can systematically enumerate all secondary users and exploit this at scale to commit financial fraud across multiple PayPal business accounts. The sequential ID scheme would be immediately recognized as exploitable.

## Defensive takeaways
- Implement strict server-side authorization checks on all API endpoints; verify the requester owns/manages the resource before allowing modifications
- Replace sequential, predictable IDs with cryptographically random tokens (UUIDs) that cannot be enumerated
- Add rate limiting and anomaly detection on bulk enumeration attempts targeting sequential resources
- Implement comprehensive audit logging for all permission changes and account modifications
- Enforce multi-factor authentication for sensitive operations like password resets and privilege modifications
- Conduct security testing specifically targeting IDOR vulnerabilities across all user/account management endpoints
- Use parameterized access control lists (ACLs) to explicitly verify relationship ownership before granting access

## Variant hunting
['Search for other PayPal endpoints using sequential numeric IDs in business/enterprise management interfaces (invoicing, reporting, API keys, linked accounts)', 'Test similar sequential ID patterns in other payment processor platforms (Stripe, Square, 2Checkout) in their business management areas', 'Look for batch operation endpoints that might accept multiple user IDs without proper authorization validation', 'Examine any API endpoints that modify user permissions, roles, or delegated access across different account types', 'Test for IDOR in password reset flows for secondary/delegated accounts across financial services platforms', 'Investigate whether primary account permissions can be modified through secondary account endpoints']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (Compromised Secondary Accounts)
- T1548 - Abuse Elevation Control Mechanism
- T1556 - Modify Authentication Process
- T1087 - Account Discovery (Enumeration of sequential IDs)
- T1583 - Acquire Infrastructure
- T1589 - Gather Victim Identity Information

## Notes
The vulnerability demonstrates the critical importance of proper authorization checks separate from authentication. Even though the attacker was authenticated, they could access and modify resources belonging to other users. The sequential ID scheme was a significant contributing factor, as it eliminated the need for attackers to discover valid user IDs through trial and error. PayPal reported no evidence of actual exploitation in the wild, suggesting responsible disclosure practices. This finding likely prompted PayPal to conduct a comprehensive security review of all ID-based resource access patterns across their platform.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
