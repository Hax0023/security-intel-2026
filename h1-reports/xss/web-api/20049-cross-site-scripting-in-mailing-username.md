# Cross-site Scripting in mailing (username)

## Metadata
- **Source:** HackerOne
- **Report:** 20049 | https://hackerone.com/reports/20049
- **Submitted:** 2014-07-14
- **Reporter:** melvin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
There appears to be a Cross-site Scripting vulnerability related to [my previous report](https://hackerone.com/reports/2735) in the newsletter mailing. See my attached screenshot.

The steps to exploit and the impact are the same as in the previous report, but to exploit this specific XSS an attacker would have to register an account with someone else's e-mail address. 

Because the previous i

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

There appears to be a Cross-site Scripting vulnerability related to [my previous report](https://hackerone.com/reports/2735) in the newsletter mailing. See my attached screenshot.

The steps to exploit and the impact are the same as in the previous report, but to exploit this specific XSS an attacker would have to register an account with someone else's e-mail address. 

Because the previous issue is fixed, this implies that there is no global sanitation for e-mails. I recommend checking all mailing scripts/tools for proper sanitation of variables (like the username).

</details>

---
*Analysed by Claude on 2026-05-24*
