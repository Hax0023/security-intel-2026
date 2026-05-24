# email field doesn't filtered against XSS

## Metadata
- **Source:** HackerOne
- **Report:** 17287 | https://hackerone.com/reports/17287
- **Submitted:** 2014-06-23
- **Reporter:** sasi2103
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
Pre-configuration, create new contact in Gmail with mail a"><img src=y onerror=prompt(...);>

1. Go to Invites.
2. Click on Invite Gmail Friends.
3. Accept the pop up.
4. XSS will activate on the email field.


Few issues continue during this issue:
1. When you click on this email address you get failure on AJAX functionally.
2. If you try to do the same scenario I describe the syst

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

Hi,
Pre-configuration, create new contact in Gmail with mail a"><img src=y onerror=prompt(...);>

1. Go to Invites.
2. Click on Invite Gmail Friends.
3. Accept the pop up.
4. XSS will activate on the email field.


Few issues continue during this issue:
1. When you click on this email address you get failure on AJAX functionally.
2. If you try to do the same scenario I describe the system throw Error
The website encountered an unexpected error. Please try again later.

Sasi


</details>

---
*Analysed by Claude on 2026-05-24*
