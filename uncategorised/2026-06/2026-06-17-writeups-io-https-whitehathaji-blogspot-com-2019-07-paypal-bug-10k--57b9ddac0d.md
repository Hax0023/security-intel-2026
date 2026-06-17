# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** Critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Account Takeover, Privilege Escalation, Unauthorized Financial Transaction
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account management API allowed attackers to enumerate and takeover secondary user accounts by manipulating an incrementally-indexed user ID parameter. Compromised secondary accounts with money transfer privileges could be used to conduct unauthorized financial transfers from victim business accounts.

## Attack scenario (step by step)
1. Attacker identifies the secondary user management endpoint at /businessmanage/users/api/v1/users with enumerable numeric IDs
2. Attacker captures and modifies a PUT request intended to update permissions, changing the vulnerable 'id' parameter to target victim secondary user accounts
3. Attacker incrementally enumerates secondary user IDs (e.g., 4461134950 to 4461134999) by submitting modified requests
4. Vulnerable endpoint associates enumerated secondary accounts with attacker's business account, making them visible in the attacker's user management dashboard
5. Attacker resets password for compromised secondary user account through the management interface
6. Attacker authenticates as the secondary user and executes unauthorized money transfers from victim's business account to attacker-controlled accounts

## Root cause
The API endpoint failed to validate that the user making the request had authorization to modify the targeted secondary user account ID. The numeric ID was directly used without checking ownership context, and lack of server-side authorization checks allowed cross-account object manipulation.

## Attacker mindset
An attacker seeking to compromise financial accounts would enumerate sequential numeric IDs to discover secondary user accounts, recognizing that secondary accounts with transfer privileges represent high-value targets for monetization. The attacker understood privilege escalation opportunities within business account structures.

## Defensive takeaways
- Implement strict server-side authorization checks verifying the requester owns/manages the target user account before any modification
- Avoid exposing sequential or enumerable identifiers; use non-sequential tokens or UUIDs for sensitive resources
- Enforce principle of least privilege for secondary accounts - restrict transfer capabilities where unnecessary
- Implement rate limiting and anomaly detection on privilege modification requests
- Conduct comprehensive IDOR testing across all API endpoints that manipulate user-associated resources
- Add logging and alerting for account takeover indicators (password changes, privilege modifications from unusual locations)
- Require multi-factor authentication for sensitive operations like secondary user management and privilege changes

## Variant hunting
Search for similar IDOR vulnerabilities in: (1) other PayPal endpoints managing user roles/permissions using sequential IDs; (2) account delegation features in competing fintech platforms (Stripe, Square, Wise business accounts); (3) secondary user/team member management in SaaS platforms (Salesforce, HubSpot, Zendesk); (4) API endpoints accepting user ID parameters without explicit authorization context validation

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1078: Valid Accounts
- T1550: Use Alternate Authentication Material
- T1098: Account Manipulation
- T1020: Automated Exfiltration

## Notes
The vulnerability's severity was amplified by the financial impact potential and the targeting of business accounts serving millions of organizations. The researcher demonstrated strong understanding of authorization bypass mechanics and privilege abuse. PayPal's rapid remediation with no evidence of exploitation is noteworthy. This finding exemplifies why security teams must validate authorization on every object modification, not just authentication.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
