# https://polldaddy.com storage.swf XSS

## Metadata
- **Source:** HackerOne
- **Report:** 9522 | https://hackerone.com/reports/9522
- **Submitted:** 2014-04-24
- **Reporter:** smiegles
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I found a flash based XSS located here :
`https://polldaddy.com/swf/storage.swf?onload=alert(1)`

It happends in the `ExternalInterface.Call` Function, when a parameter is inserted unfiltered it will allow XSS, you can patch it by only allowing :
A-Z a-z 0-9

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

Hi,

I found a flash based XSS located here :
`https://polldaddy.com/swf/storage.swf?onload=alert(1)`

It happends in the `ExternalInterface.Call` Function, when a parameter is inserted unfiltered it will allow XSS, you can patch it by only allowing :
A-Z a-z 0-9

Best regards,

Olivier Beg

</details>

---
*Analysed by Claude on 2026-05-24*
