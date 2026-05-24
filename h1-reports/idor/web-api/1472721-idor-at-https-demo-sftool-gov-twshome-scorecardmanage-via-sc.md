# IDOR at https://demo.sftool.gov/TwsHome/ScorecardManage/ via scorecard name

## Metadata
- **Source:** HackerOne
- **Report:** 1472721 | https://hackerone.com/reports/1472721
- **Submitted:** 2022-02-06
- **Reporter:** imthatt
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Team,

I have found a broken access control vulnerability on https://demo.sftool.gov/ under your /tws directory. 
I made two accounts.
One account i browsed to /tws and created a new scorecard. Here i can submit all information I need. The scorecard name is in the end of the URL https://demo.sftool.gov/TwsHome/ScorecardManage/testdsfdfsf
I logged out this account
I logged into attacker account.

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

Hi Team,

I have found a broken access control vulnerability on https://demo.sftool.gov/ under your /tws directory. 
I made two accounts.
One account i browsed to /tws and created a new scorecard. Here i can submit all information I need. The scorecard name is in the end of the URL https://demo.sftool.gov/TwsHome/ScorecardManage/testdsfdfsf
I logged out this account
I logged into attacker account. I browse to https://demo.sftool.gov/TwsHome/ScorecardManage/testdsfdfsf (the last part is the name of the other accounts score card). I can now view the scorecard and even edit the score card from the attackers account. I can add accounts to read only and edit permissions on the score card and change information as-well as download the score card.

Log back into the victim account and the scorecard information has been changed, downloaded and attacker has assigned permissions.

We can brute force scorecard names but i am not doing this as the above on my accounts already shows the issue.

Many thanks
Holla

## Impact

An attacker can read, edit and download and assign permissions to another users scorecard.

</details>

---
*Analysed by Claude on 2026-05-24*
