# PayPal Secondary User Account Takeover via IDOR - $10K Bounty

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** PayPal (HackerOne)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Insecure Direct Object Reference (IDOR), Insufficient Access Control, Account Takeover, Unauthorized Privilege Escalation
- **Category:** uncategorised
- **Writeup:** https://whitehathaji.blogspot.com/2019/07/paypal-bug-10k-all-secondary-users.html

## Summary
An IDOR vulnerability in PayPal's business account user management API allowed attackers to enumerate and take over secondary user accounts across different business accounts. By manipulating sequential user IDs in the PUT request to /businessmanage/users/api/v1/users, an attacker could gain unauthorized access to any secondary account and modify permissions, particularly those with money transfer privileges, enabling unauthorized fund transfers.

## Attack scenario (step by step)
1. Attacker identifies that PayPal's secondary user management API uses sequential, enumerable numeric IDs (e.g., 4446113495)
2. Attacker creates their own PayPal business account and secondary user to capture the user management API request structure
3. Attacker modifies the PUT request by changing the secondary user ID parameter to a different value (e.g., 4446113496) from another business account
4. The API fails to validate that the attacker owns or has authorization to modify the targeted secondary user account
5. Attacker successfully adds the victim's secondary user account to their own business account management interface
6. Attacker changes the victim secondary user's password and logs in with money transfer privileges, then executes unauthorized fund transfers

## Root cause
PayPal's API endpoint /businessmanage/users/api/v1/users lacked proper authorization checks to verify that the authenticated user actually owns or has rights to manage the secondary user account being modified. The API trusted the user-supplied secondary user ID without validating the account ownership relationship, combined with sequential/enumerable IDs that facilitated discovery.

## Attacker mindset
Systematic reconnaissance of API endpoints to identify patterns; recognition that sequential numeric IDs enable enumeration attacks; understanding of business account privilege structures to prioritize high-value compromises (accounts with transfer permissions); leveraging legitimate business account creation to understand API mechanics before pivoting to unauthorized access.

## Defensive takeaways
- Implement proper authorization checks on all API endpoints - verify the authenticated user has explicit rights to manage the requested resource
- Use non-sequential, non-enumerable identifiers (UUIDs) for sensitive resources instead of incremental numeric IDs
- Add request-level validation that secondary user modification requests include the owning business account ID and verify ownership
- Implement robust access control lists (ACLs) binding secondary users to specific business accounts at the database level
- Log and monitor all secondary user account modifications with alerts for cross-account access attempts
- Require additional authentication (e.g., MFA) for password reset operations on secondary accounts
- Conduct regular security testing of account management APIs, particularly focusing on authorization bypass scenarios

## Variant hunting
['Check for similar IDOR patterns in other business account management endpoints (roles, permissions, team management)', 'Audit other PayPal API endpoints that use sequential numeric IDs without proper ownership validation', 'Test password reset, email change, and privilege modification endpoints for similar authorization bypasses', 'Enumerate whether the vulnerability applies to other account types (corporate, merchant, personal accounts with authorized users)', 'Investigate if API responses leak secondary user IDs or account relationships that could facilitate enumeration', 'Test if cross-account modifications are possible in invite/link flows for secondary users']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1563 - Impair Defenses (bypassing access controls)
- T1078 - Valid Accounts (account takeover of secondary accounts)
- T1550 - Use Alternate Authentication Material (session hijacking via account takeover)
- T1021 - Remote Services (lateral movement via secondary account access)
- T1528 - Steal Application Access Token (potential API session compromise)

## Notes
The vulnerability demonstrates a critical gap in API authorization design. The combination of enumerable IDs, missing ownership validation, and high-privilege secondary accounts created a perfect storm for account takeover. PayPal's post-fix confirmation of 'no evidence of abuse' suggests the vulnerability existed for some time. The $10K bounty reflects the critical severity given the direct financial impact potential. The researcher's methodology of creating parallel accounts to understand API structure is a valuable reconnaissance technique applicable across fintech platforms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
