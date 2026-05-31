# Stored XSS in Slack (weird, trial and error)

## Metadata
- **Source:** HackerOne
- **Report:** 96337 | https://hackerone.com/reports/96337
- **Submitted:** 2015-10-28
- **Reporter:** harrymg
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi slack. I found a weird, trial and error Stored XSS in Slack... I hope you can get clear of this and get it too.. and I hope you can find the XSS too. Anyway here it is (according to what I did):

1. Go to your Slack or create a new Slack team.
2. In slackbot.. enter this payload:
                        <img class="emoji" alt="😯" src="x" /><svg onload=prompt(document.domain)>
3. Then, Create a 

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

Hi slack. I found a weird, trial and error Stored XSS in Slack... I hope you can get clear of this and get it too.. and I hope you can find the XSS too. Anyway here it is (according to what I did):

1. Go to your Slack or create a new Slack team.
2. In slackbot.. enter this payload:
                        <img class="emoji" alt="😯" src="x" /><svg onload=prompt(document.domain)>
3. Then, Create a new post and enter the same payload too (as title, and in one paragraph, one code)
4. Share it to slackbot,, and comment using the XSS payload given
5. Then create a snippet.. enter the payload as well... and it is HTML or any format..
6. Add comment using the XSS payload.
7. Click Create snippet

then I refreshed my slack.. I suddenly got an XSS payload.. In some cases, this will work immediately.. but sometimes... you will have to repeat the process. trial and error..

I hope you understand my report... I have provided videos and pictures for clearer details.

Thanks!

Video link: https://youtu.be/UtYrymMgMb8


</details>

---
*Analysed by Claude on 2026-05-31*
