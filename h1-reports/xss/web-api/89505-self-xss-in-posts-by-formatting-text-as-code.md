# Self-XSS in posts by formatting text as code

## Metadata
- **Source:** HackerOne
- **Report:** 89505 | https://hackerone.com/reports/89505
- **Submitted:** 2015-09-18
- **Reporter:** harrymg
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi I have found an XSS in Slack. To reproduce the issue, just follow this:

1. Go to your Slack account (accountname.slack.com)

2. Below you will see a plus (+) sign, click that, there will be three options, click "Create Post"

3. You will be redirected to a page where you will create it.

4. Type the payload. I used: <svg onload=alert(domain)>. then Highlight it..  on the left side, the

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

Hi I have found an XSS in Slack. To reproduce the issue, just follow this:

1. Go to your Slack account (accountname.slack.com)

2. Below you will see a plus (+) sign, click that, there will be three options, click "Create Post"

3. You will be redirected to a page where you will create it.

4. Type the payload. I used: <svg onload=alert(domain)>. then Highlight it..  on the left side, there are symbols... click it and choose this symbol: ( <>) which is for code..

5. XSS Pop-up

Youtube video for clearer details:

https://youtu.be/dIvNeb2aRrU


THANKS!

</details>

---
*Analysed by Claude on 2026-05-24*
