# clickjacing can lead to account takeover

## Metadata
- **Source:** HackerOne
- **Report:** 2119892 | https://hackerone.com/reports/2119892
- **Submitted:** 2023-08-22
- **Reporter:** hyk3n
- **Program:** Unknown
- **Bounty:** $200
- **Severity:** low
- **Vuln:** UI Redressing (Clickjacking)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
hello team .
while testing the site we found an endpoint call https://sketch.pixiv.net/draw 
{F2626044}
 using  it we can trick the user to fake login with the use of clickjackingpoc  : https://github.com/shifa123/clickjackingpoc
as poc shown :
{F2626057}

## Impact

Users are tricked into performing all sorts of unintended actions are such as typing in the password, clicking on ‘Delete my account

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

hello team .
while testing the site we found an endpoint call https://sketch.pixiv.net/draw 
{F2626044}
 using  it we can trick the user to fake login with the use of clickjackingpoc  : https://github.com/shifa123/clickjackingpoc
as poc shown :
{F2626057}

## Impact

Users are tricked into performing all sorts of unintended actions are such as typing in the password, clicking on ‘Delete my account’ button, liking a post, deleting a post, commenting on a blog. In other words all the actions that a normal user can do on a legitimate website can be done using clickjacking.

</details>

---
*Analysed by Claude on 2026-05-24*
