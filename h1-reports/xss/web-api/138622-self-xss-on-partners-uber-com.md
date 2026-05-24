# Self-XSS on partners.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 138622 | https://hackerone.com/reports/138622
- **Submitted:** 2016-05-13
- **Reporter:** cyber__sec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I found a reflected XSS vulnerability in password reset page https://partners.uber.com/reset-password. 
I have tested this vulnerability in the latest Chrome and Firefox browsers.

Reproduction Steps:
1- Go to https://login.uber.com/forgot-password and reset password. Then, Click password reset link on your mailbox.
2- Paste  "><img src=x onerror=prompt(document.domain)>   as your new passwor

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

I found a reflected XSS vulnerability in password reset page https://partners.uber.com/reset-password. 
I have tested this vulnerability in the latest Chrome and Firefox browsers.

Reproduction Steps:
1- Go to https://login.uber.com/forgot-password and reset password. Then, Click password reset link on your mailbox.
2- Paste  "><img src=x onerror=prompt(document.domain)>   as your new password and submit.
3- Wait and see XSS payload fired.

Also I added screenshots.

Thanks,

</details>

---
*Analysed by Claude on 2026-05-24*
