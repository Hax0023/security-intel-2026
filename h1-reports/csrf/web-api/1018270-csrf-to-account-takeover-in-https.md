# CSRF to account takeover in https://█████/

## Metadata
- **Source:** HackerOne
- **Report:** 1018270 | https://hackerone.com/reports/1018270
- **Submitted:** 2020-10-25
- **Reporter:** i_hack_everyone
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi DoD team,
I found a CSRF to account takeover in https://███████/

## NOTE:
Try to open the site in firefox because chrome sometimes is not allowing to open the site.

## Summary:
There is no protection against CSRF in changing email which lead to CSRF to account takeover on  https://██████/.

## Step-by-step Reproduction Instructions
## I have made a video POC in which I have shown the account 

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

Hi DoD team,
I found a CSRF to account takeover in https://███████/

## NOTE:
Try to open the site in firefox because chrome sometimes is not allowing to open the site.

## Summary:
There is no protection against CSRF in changing email which lead to CSRF to account takeover on  https://██████/.

## Step-by-step Reproduction Instructions
## I have made a video POC in which I have shown the account takeover clearly Please do watch for better understanding
1. Login as victim and check your infos in the account details
2. Open the CSRF malicious file which I have attached (csrf_POC.html)
3. Now the email is different (you can also change your name and other fields as well)
4. Now you can simply takeover the account
5. All you have to do is click on reset password on main page and enter the email you used to trick the victim and you will get instructions to reset the password. And you can successfully takeover the account

## Suggested Mitigation/Remediation Actions
Use captchas and CSRF-tokens for be sure that the victim is changing the datas knowing that.

## Impact

It is a critical issue as i was able to takeover anyone account using this attack. This vulnerability is high/critical because I was able to perform account takeover

</details>

---
*Analysed by Claude on 2026-05-24*
