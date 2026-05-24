# Find, private notes Cross-site scripting.

## Metadata
- **Source:** HackerOne
- **Report:** 7917 | https://hackerone.com/reports/7917
- **Submitted:** 2014-04-17
- **Reporter:** smiegles
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi.

When I go to the find page and insert a `private note`, with as content : `<img src='x' onerror='alert(4)'` it will execute directly.

As preview :
1.) http://prntscr.com/3axvz5
2.) http://prntscr.com/3axw3k

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

Hi.

When I go to the find page and insert a `private note`, with as content : `<img src='x' onerror='alert(4)'` it will execute directly.

As preview :
1.) http://prntscr.com/3axvz5
2.) http://prntscr.com/3axw3k

Best regards,

Olivier Beg

</details>

---
*Analysed by Claude on 2026-05-24*
