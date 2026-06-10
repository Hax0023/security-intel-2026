# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Privilege Escalation, Account Takeover
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
A critical IDOR vulnerability in PayPal's business account secondary user management API allowed attackers to enumerate and takeover any secondary user account through predictable numeric IDs. By modifying the secondary user ID parameter in the permission update request, an attacker could add victim secondary accounts to their own business account, reset passwords, and subsequently perform unauthorized money transfers.

## Attack scenario (step by step)
1. Attacker creates a secondary user account in their own PayPal business account to obtain the API endpoint structure and request format
2. Attacker identifies the secondary user ID parameter in the PUT request to /businessmanage/users/api/v1/users is a predictable incremental numeric value
3. Attacker systematically enumerates secondary user IDs (e.g., 4461134950 through 4461135000) by modifying the vulnerable parameter
4. For each enumerated ID belonging to victim accounts, attacker's business account gains visibility and control over those secondary user accounts in the manage users section
5. Attacker locates a secondary account with 'Transfer Money' privilege and resets its password via the manage users panel
6. Attacker logs into the compromised secondary account and performs unauthorized money transfers from the victim's PayPal business account to attacker-controlled accounts

## Root cause
PayPal failed to implement proper access controls on the secondary user management API endpoint. The system did not verify that the authenticated user had authorization to modify secondary user accounts belonging to other business accounts. The use of predictable, sequential numeric IDs combined with no input validation on the ID parameter enabled simple enumeration and manipulation.

## Attacker mindset
The attacker demonstrated methodical reconnaissance by first understanding the legitimate API structure using their own accounts, then recognized the enumerable nature of IDs as a pathway to scale the attack across all PayPal secondary users. The attacker understood business account privilege structures and specifically targeted the 'Transfer Money' privilege to maximize impact and financial gain.

## Defensive takeaways
- Implement strict access control checks on all API endpoints - verify the authenticated user owns/manages the resource being accessed before allowing modifications
- Avoid using sequential, predictable identifiers for sensitive resources; use UUIDs or cryptographically random identifiers instead
- Add rate limiting and anomaly detection on ID enumeration attempts in API requests
- Validate that secondary user IDs belong to the authenticated user's business account before processing any modifications
- Implement audit logging for all secondary user account modifications including password changes and privilege updates
- Require additional authentication factors (MFA, verification codes) when modifying critical secondary user accounts or permissions
- Conduct regular access control reviews and penetration testing on business account management APIs
- Implement principle of least privilege - secondary accounts should not inherit modification permissions across other secondary accounts

## Variant hunting
['Check other PayPal business account management endpoints for similar IDOR patterns (team members, API signatures, webhook configurations)', "Test for IDOR in related financial platforms' secondary/delegate account management systems", 'Investigate if other user management parameters in PayPal API use sequential IDs (user roles, team IDs, organization IDs)', 'Search for similar patterns in APIs handling delegated access or privilege management', 'Test if the vulnerability extends to reading sensitive data (viewing transaction history, account balances) for enumerated accounts']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts (Account Takeover)
- T1566 - Phishing (indirect - account compromise)
- T1021 - Remote Services (lateral movement via secondary accounts)

## Notes
This was a high-impact vulnerability affecting millions of PayPal business accounts worldwide. The vulnerability's severity was amplified by PayPal's business model where secondary accounts often have financial transaction permissions. The researcher provided clear PoC steps and demonstrated understanding of business account privilege structures. PayPal confirmed no evidence of exploitation, suggesting responsible disclosure. The vulnerability exemplifies how broken access controls on sequential identifiers can lead to mass account compromise and financial fraud.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
