# http://jetpack.me/ Self XSS

## Metadata
- **Source:** HackerOne
- **Report:** 14303 | https://hackerone.com/reports/14303
- **Submitted:** 2014-05-31
- **Reporter:** smiegles
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there :)

I found a self XSS located at the front page of http://jetpack.me/, To reproduce this you have to scroll to the `Every feature!` part and search for `<img src=x onerror=alert(1)>` in the search engine.

Best regards,

Olivier Beg

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

Hi there :)

I found a self XSS located at the front page of http://jetpack.me/, To reproduce this you have to scroll to the `Every feature!` part and search for `<img src=x onerror=alert(1)>` in the search engine.

Best regards,

Olivier Beg

</details>

---
*Analysed by Claude on 2026-05-24*
