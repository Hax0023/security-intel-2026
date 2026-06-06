# PayPal Secondary User Account Takeover via Insecure Direct Object Reference (IDOR)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** Critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Inadequate Access Control, Privilege Escalation, Account Takeover
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account management allowed attackers to enumerate and take over secondary user accounts by manipulating an incremental, predictable user ID parameter. By exploiting this flaw, an attacker could gain access to secondary accounts with elevated privileges (such as money transfer permissions) and perform unauthorized financial transactions from victim business accounts.

## Attack scenario (step by step)
1. Attacker creates a secondary user account on their own PayPal business account to understand the API structure
2. Attacker captures the PUT request to /businessmanage/users/api/v1/users and identifies the predictable numeric ID parameter for secondary users
3. Attacker modifies the secondary user ID in the request to enumerate victim secondary account IDs (incrementing from known baseline ID values)
4. Attacker successfully adds enumerated victim secondary accounts to their own business account management interface
5. Attacker changes the password of a victim secondary account with 'Transfer Money' privilege through the Manage Users section
6. Attacker logs into the compromised secondary account and transfers funds from the victim's business account to their own account

## Root cause
PayPal failed to implement proper authorization checks on the secondary user management API endpoint. The API accepted requests modifying secondary user account permissions based on a sequential numeric ID without verifying that the authenticated user had permission to manage that specific secondary account. The predictable nature of the ID also enabled enumeration attacks.

## Attacker mindset
The attacker systematically researched the business account management workflow, identified the API endpoint structure through their own secondary account, recognized the pattern of incremental IDs, and chained the IDOR vulnerability with privilege escalation to achieve financial gain through unauthorized money transfers. This demonstrates methodical reconnaissance and understanding of business process logic.

## Defensive takeaways
- Implement strict authorization checks on every API endpoint that modifies user accounts or permissions; verify the authenticated user has explicit permission to access/modify the requested resource
- Use non-sequential, non-predictable identifiers (UUIDs or cryptographically random tokens) for sensitive resources instead of incremental numeric IDs
- Employ role-based access control (RBAC) and attribute-based access control (ABAC) to enforce principle of least privilege
- Implement request validation to ensure the resource being modified belongs to the authenticated user's organization/account
- Add comprehensive audit logging for all account modifications, permission changes, and sensitive operations to detect anomalies
- Require additional authentication factors (MFA, step-up authentication) for sensitive operations like password changes on secondary accounts
- Implement rate limiting and anomaly detection on account management endpoints to flag mass enumeration attempts
- Conduct security testing specifically for IDOR vulnerabilities across all APIs that manage user accounts or cross-tenant resources

## Variant hunting
['Check other PayPal/financial platforms for similar IDOR in account management APIs using numeric IDs', 'Search for sequential ID patterns in permission modification endpoints across business account management features', 'Test for IDOR in other secondary user operations: deletion, role assignment, access revocation, activity logs', 'Examine third-party payment processors and accounting software integrations for similar account enumeration vulnerabilities', 'Look for IDOR in administrative dashboards where account representatives manage multiple client accounts', 'Test for authorization bypass in bulk user management or CSV import features', 'Check for IDOR in audit log endpoints that might expose transaction history across accounts']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1098 - Account Manipulation
- T1087 - Account Discovery
- T1550 - Use Alternate Authentication Material
- T1021 - Remote Service Session Hijacking

## Notes
This vulnerability is particularly severe because PayPal business accounts manage significant financial resources and secondary users often have delegated authority for fund transfers. The combination of IDOR + privilege abuse created a direct path to unauthorized financial theft. The researcher demonstrated good security practice by not performing actual unauthorized transfers and instead providing a clear proof of concept. PayPal's response to quickly remediate and conduct abuse investigations demonstrates a mature incident response process.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
