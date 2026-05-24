# Allow authenticated users can edit, trash,and add new in BuddyPress Emails function

## Metadata
- **Source:** HackerOne
- **Report:** 833782 | https://hackerone.com/reports/833782
- **Submitted:** 2020-03-29
- **Reporter:** hoangkien1020
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
## Description:

Allow author can edit, trash,and add new your posts in BuddyPress Emails function
And editor can edit,trash, add new any posts in BuddyPress Emails default.
## Steps To Reproduce:

Step 1 : Create two accounts: Admin and Author
Step 2: Login with admin account. In admin account, give author to admin account.
Step 4: Login with author within dashboard
Access link:
*domain/wp-admin/

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

## Description:

Allow author can edit, trash,and add new your posts in BuddyPress Emails function
And editor can edit,trash, add new any posts in BuddyPress Emails default.
## Steps To Reproduce:

Step 1 : Create two accounts: Admin and Author
Step 2: Login with admin account. In admin account, give author to admin account.
Step 4: Login with author within dashboard
Access link:
*domain/wp-admin/edit.php?post_type=bp-email*
Step 5: Revoke author to author privilege in admin account
Step 6: Within author dashboard, author can edit, trash,and add new
PoC by video:
https://bit.ly/2UH7iLz
## Recommendations
Valid user current session access.

## Impact

Author can edit, trash,and add new in BuddyPress Emails.
And editor can edit,trash, add new any posts in BuddyPress Emails default.

</details>

---
*Analysed by Claude on 2026-05-24*
