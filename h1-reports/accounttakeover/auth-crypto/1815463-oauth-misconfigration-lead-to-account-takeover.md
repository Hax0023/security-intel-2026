# oauth misconfigration lead to account takeover

## Metadata
- **Source:** HackerOne
- **Report:** 1815463 | https://hackerone.com/reports/1815463
- **Submitted:** 2022-12-22
- **Reporter:** greymanx1
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Incorrect Authorization
- **CVEs:** None
- **Category:** auth-crypto

## Summary
## Summary:
misconfigration in aouth 2.0 login with google account in "accounts.reddit.com"

## Impact:
misconfigration leads to account takeover

## Steps To Reproduce:

 1.  go to "https://accounts.reddit.com/".
 2. and login with your google account.
 3. after login, logout from your account.
 4. after logout go to "https://accounts.reddit.com/account/register/" and register with email you sign

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

## Summary:
misconfigration in aouth 2.0 login with google account in "accounts.reddit.com"

## Impact:
misconfigration leads to account takeover

## Steps To Reproduce:

 1.  go to "https://accounts.reddit.com/".
 2. and login with your google account.
 3. after login, logout from your account.
 4. after logout go to "https://accounts.reddit.com/account/register/" and register with email you signed in before in google account oauth.
 5. as like you see it's created a new account 


  * [attachment / reference]

## Impact

attacker can login with any user's email thats lead to account takeover

</details>

---
*Analysed by Claude on 2026-05-24*
