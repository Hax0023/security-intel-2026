# PayPal Secondary User Account Takeover via IDOR Leading to Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** Critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Privilege Escalation, Account Takeover
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account secondary user management API allowed attackers to enumerate and takeover any secondary user account by manipulating an incremental, predictable user ID parameter. An attacker could leverage this to gain control of secondary accounts with elevated privileges (such as money transfer permissions) and subsequently authorize unauthorized financial transfers from victim business accounts.

## Attack scenario (step by step)
1. Attacker identifies the secondary user management endpoint at https://www.paypal.com/businessmanage/users/ and captures a PUT request to the /businessmanage/users/api/v1/users endpoint containing their own secondary user ID (e.g., 4446113495)
2. Attacker recognizes the user ID parameter is numeric, incremental, and directly controllable in the API request, indicating an IDOR vulnerability
3. Attacker enumerates sequential user IDs (incrementing from a known base value like 4446113495 to 4446113999) by submitting modified PUT requests with different ID values
4. For each enumerated ID, the attacker modifies the request to add the victim's secondary user account to their own business account's user management interface
5. Once the victim's secondary user account appears in the attacker's 'Manage Users' section, the attacker changes the account password through the business management console
6. Attacker logs into the compromised secondary account and, if the account has 'Transfer Money' privileges, executes unauthorized fund transfers from the victim's business account to attacker-controlled accounts

## Root cause
PayPal failed to implement proper access control checks on the /businessmanage/users/api/v1/users API endpoint. The API did not verify that the authenticated user had authorization to modify or view the secondary user account identified by the user ID parameter before processing the request. Additionally, the use of sequential, enumerable numeric IDs without rate limiting or enumeration detection enabled attackers to discover valid user IDs.

## Attacker mindset
The attacker demonstrated systematic reconnaissance by identifying an API endpoint, recognizing patterns in the ID structure, and understanding the business logic flow (enumeration → listing → password change → privilege escalation → financial theft). The approach reflects a methodical understanding of how PayPal's secondary user permission system works and how to chain multiple steps to achieve financial fraud.

## Defensive takeaways
- Implement robust access control checks on all API endpoints to verify users can only access/modify resources they own or are explicitly authorized to manage
- Avoid using sequential numeric IDs for sensitive resources; implement UUIDs or other non-enumerable identifiers instead
- Add rate limiting and anomaly detection for ID enumeration attempts across user management endpoints
- Enforce principle of least privilege for secondary user account modifications; require additional authentication for permission changes
- Implement comprehensive audit logging for all account modifications, especially password changes and permission updates
- Conduct regular security reviews of business account management APIs where financial transactions are involved
- Require multi-factor authentication for sensitive operations like password resets on secondary accounts with elevated privileges

## Variant hunting
['Search for other PayPal endpoints using numeric IDs in user management, payment processing, or account administration APIs', 'Test other endpoints in /businessmanage/ hierarchy for similar IDOR vulnerabilities with incremental parameters', "Investigate PayPal's API for predictable patterns in account IDs, transaction IDs, or other business object identifiers", 'Examine whether similar enumeration issues exist in other PayPal products (Venmo, Braintree, etc.) that manage user hierarchies', 'Check for IDOR vulnerabilities in privilege/permission modification endpoints across other payment processors', 'Look for opportunities to chain IDOR vulnerabilities with privilege escalation in financial systems']

## MITRE ATT&CK
- T1190
- T1078
- T1098
- T1548
- T1555
- T1021

## Notes
This vulnerability is particularly severe because it affected PayPal Business accounts used by millions of organizations worldwide. The attacker could have gained access to accounts with financial transaction privileges, enabling large-scale fraud. The incremental ID design combined with no access control created a perfect storm for exploitation. PayPal confirmed no evidence of exploitation in the wild, indicating responsible disclosure. The $10K bounty was appropriate given the critical nature and financial impact potential.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
