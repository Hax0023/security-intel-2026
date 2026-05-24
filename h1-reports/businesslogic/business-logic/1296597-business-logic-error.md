# Business logic error

## Metadata
- **Source:** HackerOne
- **Report:** 1296597 | https://hackerone.com/reports/1296597
- **Submitted:** 2021-08-09
- **Reporter:** scianto05
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Business Logic Errors
- **CVEs:** None
- **Category:** business-logic

## Summary
Hi UPCHIEVE SECURITY TEAM

I'm Anto

Vulnerability :
Business logic error
There is no password verification while changing a password.

Steps to Reproduce :
1). Go to (https://hackers.upchieve.org/resetpassword).
2). Click the change password.
3). If your old password was ex:  hacker and in new password enter the same password ex: hacker.
4). The password will be updated.

There is no password che

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

Hi UPCHIEVE SECURITY TEAM

I'm Anto

Vulnerability :
Business logic error
There is no password verification while changing a password.

Steps to Reproduce :
1). Go to (https://hackers.upchieve.org/resetpassword).
2). Click the change password.
3). If your old password was ex:  hacker and in new password enter the same password ex: hacker.
4). The password will be updated.

There is no password check mechanism on there.
Fix it by making an alert
" Your new password must be different"

## Impact

Business logic error
Please let me know if this can be fixed :)

Regards,
Anto

</details>

---
*Analysed by Claude on 2026-05-24*
