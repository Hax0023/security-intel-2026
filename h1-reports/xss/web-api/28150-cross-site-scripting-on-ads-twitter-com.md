# Cross site scripting on ads.twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 28150 | https://hackerone.com/reports/28150
- **Submitted:** 2014-09-15
- **Reporter:** anandpingsafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

Steps to reproduce the issue:
1) Go to this link https://ads.twitter.com/accounts/XXXX/tweets where is XXXX is your account id.

2) Click on Compose Tweet option and enter "><svg/onload=prompt(123);>

3) Click on "Tweet" Button now.

You will prompt dialog box with "123" in it.

POC video: https://www.dropbox.com/s/64li7wv7gq2brlz/twitterxss.mov?dl=0

Please fix this.

Best Reg

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

Steps to reproduce the issue:
1) Go to this link https://ads.twitter.com/accounts/XXXX/tweets where is XXXX is your account id.

2) Click on Compose Tweet option and enter "><svg/onload=prompt(123);>

3) Click on "Tweet" Button now.

You will prompt dialog box with "123" in it.

POC video: https://www.dropbox.com/s/64li7wv7gq2brlz/twitterxss.mov?dl=0

Please fix this.

Best Regards,
Anand Prakash

</details>

---
*Analysed by Claude on 2026-05-24*
