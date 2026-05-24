# Stored XSS on this link https://sehacure.slack.com/help/requests/

## Metadata
- **Source:** HackerOne
- **Report:** 2639 | https://hackerone.com/reports/2639
- **Submitted:** 2014-03-01
- **Reporter:** anandpingsafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

This is a little tricky one.

First of all go to your profile page and change your name to "><img src=x onerror=prompt(12);>
Save it.
Wait!!! You will not see a javascript pop up there because there is proper input validation on the profile page.

Now to see the prompt box

1) Go to this link  https://sehacure.slack.com/help/requests/new
2) Add a new ticket. Now submit it. 
3) Now

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

This is a little tricky one.

First of all go to your profile page and change your name to "><img src=x onerror=prompt(12);>
Save it.
Wait!!! You will not see a javascript pop up there because there is proper input validation on the profile page.

Now to see the prompt box

1) Go to this link  https://sehacure.slack.com/help/requests/new
2) Add a new ticket. Now submit it. 
3) Now view your ticket.You will now be shown a prompt box.
4) Please have a look at the attached screenshot the inputs are not validated over there.

I have changed my name to }') ">ppp>
and i am attaching the source code view of the same.No, input encoding is done there.

Please have a check.

Best,
Anand

</details>

---
*Analysed by Claude on 2026-05-24*
