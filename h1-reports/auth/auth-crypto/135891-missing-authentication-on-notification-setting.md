# Missing authentication on Notification setting .

## Metadata
- **Source:** HackerOne
- **Report:** 135891 | https://hackerone.com/reports/135891
- **Submitted:** 2016-05-03
- **Reporter:** vijay_kumar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi ,
Notification setting link works without cookies so an attacker can steal link from browser histroy and can change notification setting of victim.
Notification setting link does not expire even after logout.

Steps to reproduce :-
1.Log in as uber rider.
2.Go to profile.
3.Now go to "Manage your email subscription settings".
4.Copy link of this page and open this link in another browser , it w

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

Hi ,
Notification setting link works without cookies so an attacker can steal link from browser histroy and can change notification setting of victim.
Notification setting link does not expire even after logout.

Steps to reproduce :-
1.Log in as uber rider.
2.Go to profile.
3.Now go to "Manage your email subscription settings".
4.Copy link of this page and open this link in another browser , it works perfectly.
5.It also works after logout.

</details>

---
*Analysed by Claude on 2026-05-24*
