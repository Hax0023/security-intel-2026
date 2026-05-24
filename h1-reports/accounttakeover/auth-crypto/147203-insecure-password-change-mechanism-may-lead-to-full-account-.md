# Insecure password change mechanism may lead to full account takeover

## Metadata
- **Source:** HackerOne
- **Report:** 147203 | https://hackerone.com/reports/147203
- **Submitted:** 2016-06-25
- **Reporter:** shawarkhan
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cryptographic Issues - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
###Description:
The password change mechanism which is located at https://www.fantasytote.com/users/edit is insecure as there is no old password field deployed in it. Any unauthorized user can access the account and can change the password directly without knowing the old password. The current password or old password field is necessary because it prevents any unauthorized user from changing the p

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

###Description:
The password change mechanism which is located at https://www.fantasytote.com/users/edit is insecure as there is no old password field deployed in it. Any unauthorized user can access the account and can change the password directly without knowing the old password. The current password or old password field is necessary because it prevents any unauthorized user from changing the password.

Facebook, Google and many other companies have deployed this fix.

###Steps to Reproduce:

* Goto https://www.fantasytote.com
* Sign in 
* Goto https://www.fantasytote.com/users/edit
* You will see password change area
* Change the password and it will be changed without prompting the old password

###Fix / Patch:
Deploy a mechanism that asks the user for the old password in order to change his password. If the user knows his old password, the password should be changed otherwise not.

Waiting for positive response,
Thanks.

</details>

---
*Analysed by Claude on 2026-05-24*
