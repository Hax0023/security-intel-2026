# Access Permission Not Revoked After Email Deletion/Change on Partner Account

## Metadata
- **Source:** HackerOne
- **Report:** 870001 | https://hackerone.com/reports/870001
- **Submitted:** 2020-05-10
- **Reporter:** jaka-tingkir
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Privilege Escalation, Session Management Flaw, Account Enumeration
- **CVEs:** None
- **Category:** uncategorised

## Summary
A partner account can retain full access to delegated stores and collaborator permissions even after the associated email address is deleted or changed from the partner account. An attacker can leverage a former partner email to maintain unauthorized access to stores that had previously granted collaborator permissions, bypassing the intended access revocation mechanism.

## Attack scenario
1. Attacker creates a Shopify partner account using a business email address (e.g., attacker@company.com) and confirms ownership
2. Attacker receives collaboration invitation from a shop owner and accepts, gaining store access as a collaborator
3. Attacker changes the partner account's primary email to their personal email (attacker@personal.com) and confirms the change
4. Attacker logs out and attempts to log in using the old email address (attacker@company.com) through accounts.shopify.com
5. Despite the old email being removed from the partner account, the attacker successfully authenticates and gains access
6. Attacker navigates to the previously delegated store and discovers they retain full collaborator permissions, accessing sensitive store data and functionality

## Root cause
The application fails to revoke or invalidate access tokens/sessions associated with partner accounts when an email address is removed or changed. The access control mechanism ties permissions to the partner account identifier rather than properly invalidating all authentication paths when account details are modified. The system likely maintains a stale email-to-account mapping that is not properly cleaned up during email change operations.

## Attacker mindset
An insider threat or former business partner seeks persistent unauthorized access to stores they previously had legitimate access to. By changing their primary email, they exploit the system's failure to invalidate old email-based authentication paths, maintaining backdoor access even after being offboarded from the partner program.

## Defensive takeaways
- Implement explicit session and token revocation upon email address changes or account modifications
- Audit all authentication mechanisms (email-based, session tokens, API keys) and invalidate them when account attributes change
- Enforce email verification across all access paths before granting store access
- Implement a grace period for access changes with explicit notifications to store owners when collaborator account details are modified
- Log all account modification events and cross-reference against active access grants to catch and revoke stale permissions
- Regularly audit access lists against active partner accounts to identify orphaned or invalid access grants
- Implement account linking that explicitly requires re-authorization when primary email changes
- Add role-based access controls with mandatory re-consent when account identifiers change

## Variant hunting
Check if other account attributes (phone number, company name, address) changes also fail to revoke access
Test if API keys issued under old email remain valid after email change
Verify if staff accounts have the same privilege escalation path after email modification
Check if removing an account entirely from partner program still leaves access grants intact
Test cross-partner access scenarios where a user has multiple partner accounts with overlapping store permissions
Verify if changing email on app developer accounts also bypasses access revocation
Test if explicitly denying a collaborator still allows access through the old email path

## MITRE ATT&CK
- T1098 - Account Manipulation
- T1199 - Trusted Relationship
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process
- T1562 - Impair Defenses

## Notes
The report demonstrates a critical business logic flaw in access control implementation. The vulnerability allows privilege persistence through email manipulation, affecting the integrity of the Shopify partner ecosystem. The attacker maintains access under the original partner account name despite the triggering email being removed, suggesting access tokens are bound to account IDs rather than email credentials. This is particularly severe as it affects B2B access patterns where email rotation is common in business environments.

## Full report
<details><summary>Expand</summary>

I can get increased privileges from accounts that have been deleted from shopify partners.

a partner uses another business email account and when the business email has been replaced or deleted from a partner, it turns out that the account still has full access as a collaborator account or still has permission as a partner account.

## Steps For Reproductions
1. create a partner account and use another business account email, and confirm
2. Add the store as a collaboration, and receive permission from the shop owner
3. Open a shop that has given permission
4. Return to partners, change business email to your email, and confirm
5. open an account from the email that has been used in a business email (step 1), try logging in to the added store (step 2). You can not enter and look email is not registered at the store
6. try logging in to `accounts.shopify.com` and successfully entering the shopify account
7. entered the store that was added, after successfully logging in it turns out that this account entered using the name of the partner account ██████████

## Impact

The account can enter the collaboration store using the permission as a collaboration account even though it has been deleted from the partner account and is not part of the partner

</details>

---
*Analysed by Claude on 2026-05-24*
