# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Privilege Escalation, Account Takeover
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
A critical IDOR vulnerability in PayPal's business account user management API allowed attackers to enumerate and takeover any secondary user account by incrementally guessing sequential user IDs. Compromised secondary accounts with 'Transfer Money' privileges could be exploited to perform unauthorized money transfers from victim business accounts.

## Attack scenario (step by step)
1. Attacker identifies the sequential user ID format in the /businessmanage/users/api/v1/users PUT endpoint while managing their own secondary account
2. Attacker modifies the request to target an enumerated secondary user ID belonging to a victim business account (e.g., incrementing from 44613495 to 44613496)
3. Attacker submits the modified request with elevated privileges, and the vulnerable API accepts the change without proper authorization checks
4. The victim's secondary user account now appears in the attacker's user management dashboard despite belonging to a different business account
5. Attacker uses the management interface to reset the secondary user's password and gain login access
6. Attacker logs into the compromised secondary account and executes unauthorized money transfers from the victim's business account

## Root cause
PayPal's user management API failed to implement proper authorization checks before allowing modifications to secondary user accounts. The API relied solely on sequential numeric IDs without verifying that the requesting user owned or had permission to manage the target account. Additionally, the predictable and enumerable ID scheme facilitated discovery of other accounts.

## Attacker mindset
The attacker recognized that business secondary accounts with financial privileges represent high-value targets. By identifying the enumerable nature of user IDs and the lack of ownership validation, the attacker could systematically discover and compromise accounts with specific permissions (Transfer Money) that directly enable monetary theft. This demonstrates opportunistic exploitation of access control flaws to achieve financial gain.

## Defensive takeaways
- Implement strict authorization checks on all API endpoints that modify user accounts - verify the requesting user owns or has explicit permission to manage the target account
- Replace sequential numeric IDs with non-enumerable identifiers (UUIDs, cryptographic tokens) to prevent ID enumeration attacks
- Apply the principle of least privilege - secondary users should only access accounts within their organization's tenant/workspace
- Enforce business logic validation - API should reject requests attempting to modify accounts outside the requester's authorized scope
- Implement rate limiting and anomaly detection on user management endpoints to identify bulk ID enumeration attempts
- Conduct thorough authorization testing across all multi-tenant features to ensure cross-account access is impossible
- Add comprehensive audit logging for all user account modifications, particularly privilege escalations and password changes

## Variant hunting
['Check other PayPal endpoints managing business resources (invoices, transactions, reports) for similar IDOR vulnerabilities using sequential IDs', 'Test ability to enumerate and modify other secondary user properties (email, name, MFA settings) beyond just permissions', 'Investigate whether the IDOR extends to the parent business account level or other account types (personal, merchant accounts)', 'Search for similar sequential ID enumeration patterns in other PayPal API endpoints (/businessmanage/reports, /businessmanage/transactions)', 'Test if password reset functionality has independent authorization checks or reuses the vulnerable user management logic', 'Examine invitation/onboarding flows for secondary users to identify if IDOR exists at earlier stages of account creation']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1087 - Account Discovery
- T1098 - Account Manipulation
- T1110 - Brute Force (ID enumeration)
- T1589 - Gather Victim Identity Information

## Notes
The $10K bounty reflects the critical business impact - potential for large-scale unauthorized financial transfers from PayPal business accounts. The vulnerability's severity was amplified by the sequential, easily enumerable ID scheme and the direct tie to accounts with active financial privileges. PayPal's timely remediation and confirmation of no abuse incidents prevented wider exploitation. This case exemplifies how IDOR combined with privilege escalation and enumerable resources creates maximum impact in multi-tenant financial systems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
