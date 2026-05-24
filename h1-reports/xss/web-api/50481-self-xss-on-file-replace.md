# Self Xss on File Replace

## Metadata
- **Source:** HackerOne
- **Report:** 50481 | https://hackerone.com/reports/50481
- **Submitted:** 2015-03-07
- **Reporter:** ishahriyar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
In File manager there is an Replace option to replace files from three resources .
1. from computer
2.incoming
3.Remote files
For remote files if we put 
http://example.com/"><img src=x onerror=confirm('name')>

in the url box
It reflects xss.
Poc: https://www.dropbox.com/s/m7pb9wiwxix1oyu/replacexss.mkv?dl=0

Thanks

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

In File manager there is an Replace option to replace files from three resources .
1. from computer
2.incoming
3.Remote files
For remote files if we put 
http://example.com/"><img src=x onerror=confirm('name')>

in the url box
It reflects xss.
Poc: https://www.dropbox.com/s/m7pb9wiwxix1oyu/replacexss.mkv?dl=0

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
