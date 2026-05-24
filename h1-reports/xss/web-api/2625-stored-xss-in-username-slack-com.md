# Stored XSS in username.slack.com

## Metadata
- **Source:** HackerOne
- **Report:** 2625 | https://hackerone.com/reports/2625
- **Submitted:** 2014-03-01
- **Reporter:** prakharprasad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi 

There is a stored XSS in username.slack.com.

Steps to reproduce:

1. Login to your Slack
2. Goto "Create Private Group" and with any name and purpose
3. Goto https://manish.slack.com/messages/group/files/
4. Upload a file hitting upload icon (^)  filename shall be "><img src=x onerror=alert(1);>.jpeg
5. After file is uploaded click on the image or file title, JS will execute as the

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

Hi 

There is a stored XSS in username.slack.com.

Steps to reproduce:

1. Login to your Slack
2. Goto "Create Private Group" and with any name and purpose
3. Goto https://manish.slack.com/messages/group/files/
4. Upload a file hitting upload icon (^)  filename shall be "><img src=x onerror=alert(1);>.jpeg
5. After file is uploaded click on the image or file title, JS will execute as the filename is considered as payload

I've attached the image showing XSS.

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
