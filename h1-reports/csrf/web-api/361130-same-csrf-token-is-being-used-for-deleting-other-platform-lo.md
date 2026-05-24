# Same CSRF token is being used for deleting other platform login’s within an account and across other liberapay Account’s

## Metadata
- **Source:** HackerOne
- **Report:** 361130 | https://hackerone.com/reports/361130
- **Submitted:** 2018-06-02
- **Reporter:** mah1ndra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
>We’ve got  “Accounts Elsewhere” option in the profile section. where we can connect our liberapay account with multiple other platform accounts.

>While deleting those Multiple other platform accounts same CSRF token is being used.

>I’ve signed up with a couple of liberapay accounts. Where I found the using of same CSRF token within the account and across other accounts.

## Impact

In the first

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

>We’ve got  “Accounts Elsewhere” option in the profile section. where we can connect our liberapay account with multiple other platform accounts.

>While deleting those Multiple other platform accounts same CSRF token is being used.

>I’ve signed up with a couple of liberapay accounts. Where I found the using of same CSRF token within the account and across other accounts.

## Impact

In the first account in "Accounts ElseWhere" section, I've logged in with Google+ account successfully and while deleting the account I got CSRF token = J0Lk5iXTpp40iDN5KNcrI24bulPcF0PV
Next, I found the same CSRF token is being during deleting all other available other platform logins.

I've created another liberapay account and in "Account ElseWhere" section. I've logged in with my Facebook account and while deleting it I came across same CSRF token used in other account = J0Lk5iXTpp40iDN5KNcrI24bulPcF0PV.

So, I'Ve found same CSRF token is being used for deleting other platform accounts within a liberapay account and across liberapay accounts.

I'm dropping the POC video below.

</details>

---
*Analysed by Claude on 2026-05-24*
