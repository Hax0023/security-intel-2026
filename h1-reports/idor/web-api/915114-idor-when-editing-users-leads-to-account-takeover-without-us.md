# IDOR when editing users leads to Account Takeover without User Interaction at CrowdSignal

## Metadata
- **Source:** HackerOne
- **Report:** 915114 | https://hackerone.com/reports/915114
- **Submitted:** 2020-07-04
- **Reporter:** bugra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi team,
If you click `Edit` button on any user of your team at https://app.crowdsignal.com/users/list-users.php, you will send a GET request to `https://app.crowdsignal.com/users/invite-user.php?id=(userid)&popup=1`
In this endpoint, `id` parameter is vulnerable for IDOR. When you change the user ID, you will see victim's email in response like that :
{F893392}
And if you click `Updat

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
Hi team,
If you click `Edit` button on any user of your team at https://app.crowdsignal.com/users/list-users.php, you will send a GET request to `https://app.crowdsignal.com/users/invite-user.php?id=(userid)&popup=1`
In this endpoint, `id` parameter is vulnerable for IDOR. When you change the user ID, you will see victim's email in response like that :
{F893392}
And if you click `Update Permissions` button, you will log-in to victim's account directly.
Also, user IDs are sequential. And they have a simple range with `00010006` to `19920500+`

## Steps To Reproduce:

  1. Log-in to your team account at CrowdSignal
  1. Go to https://app.crowdsignal.com/users/invite-user.php?id=19920465&popup=1
  1. You will see my email, and if you click `Update Permissions`, you will takeover my account.
  1. You can change the user ID to random number with `00010006` - `19920500` range.

## Impact

IDOR leads to account takeover without user interaction

Thanks,
Bugra

</details>

---
*Analysed by Claude on 2026-05-24*
