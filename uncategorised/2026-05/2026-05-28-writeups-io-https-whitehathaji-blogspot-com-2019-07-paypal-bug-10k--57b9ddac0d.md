# PayPal Secondary User Account Takeover via IDOR - Unauthorized Money Transfer

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** Critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Privilege Escalation, Account Takeover
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account management API allowed attackers to enumerate and takeover secondary user accounts by modifying sequential user IDs in PUT requests. Once compromised, attackers could leverage hijacked accounts with 'Transfer Money' privileges to perform unauthorized fund transfers from victim business accounts.

## Attack scenario (step by step)
1. Attacker creates their own PayPal business account to access the secondary user management API endpoint
2. Attacker captures a legitimate PUT request to /businessmanage/users/api/v1/users that modifies secondary user permissions
3. Attacker identifies that the user ID parameter (e.g., 4446113495) is sequential and enumerable
4. Attacker systematically increments the user ID to enumerate all secondary accounts across different business accounts (e.g., 4446113496, 4446113497, etc.)
5. Attacker modifies enumerated secondary account credentials via the Manage Users interface, gaining access to victim's secondary accounts
6. Attacker logs into compromised secondary accounts with 'Transfer Money' privileges and executes unauthorized fund transfers to their own account

## Root cause
PayPal failed to properly validate object ownership in the secondary user management API. The system used sequential, enumerable numeric IDs without verifying that the requesting user had authorization to modify accounts outside their own business account scope. The PUT endpoint blindly accepted any user ID without ownership validation.

## Attacker mindset
The researcher methodically analyzed the API structure to identify the enumerable pattern, recognizing that sequential IDs combined with missing authorization checks created a complete account takeover path. The attacker understood the privilege model and weaponized the ability to reset passwords on compromised accounts to gain access to financially privileged secondary users.

## Defensive takeaways
- Implement strict authorization checks on all API endpoints - verify user ownership of resources before allowing modifications
- Replace sequential numeric IDs with cryptographically random tokens (UUIDs) to prevent enumeration attacks
- Enforce principle of least privilege - secondary user modifications should only be possible within the context of the authenticated user's own business account
- Implement rate limiting and anomaly detection on account modification operations
- Add audit logging for all secondary user permission changes and password resets
- Conduct regular penetration testing of business account management APIs, focusing on IDOR vectors
- Validate that permission changes align with business logic (e.g., verify account ID matches authenticated user's business)

## Variant hunting
['Check other PayPal account management endpoints (primary users, payment receivers, etc.) for similar IDOR patterns', 'Test wallet transfer APIs for enumerable account references', 'Investigate cryptocurrency or alternative payment processor management interfaces using sequential IDs', 'Search for similar IDOR patterns in business account management features across different permission scopes', 'Examine API endpoints that handle cross-business account operations (invoicing, reports, etc.)']

## MITRE ATT&CK
- T1190
- T1078
- T1021
- T1087
- T1555

## Notes
This vulnerability represents a critical business risk as it directly enables financial fraud. The researcher demonstrated exceptional exploit progression: discovering the IDOR, recognizing the sequential pattern, understanding privilege implications, and connecting it to unauthorized money transfer capabilities. PayPal's response indicating 'no evidence of abuse' suggests the fix was applied proactively before exploitation in the wild. The $10K bounty reflects the severity and financial impact potential.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
