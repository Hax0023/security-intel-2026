# XSS / SELF XSS

## Metadata
- **Source:** HackerOne
- **Report:** 906201 | https://hackerone.com/reports/906201
- **Submitted:** 2020-06-23
- **Reporter:** ferdihermawan1337
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
I found xss but i think its self xss

POC

1. Go to yourstore.myshopify.com
2. Go to settings > import 
3. Upload wrong file csv with file name payload xss "><img src=xx onerror=alert(document.domain)>

## Impact

xss attack

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

I found xss but i think its self xss

POC

1. Go to yourstore.myshopify.com
2. Go to settings > import 
3. Upload wrong file csv with file name payload xss "><img src=xx onerror=alert(document.domain)>

## Impact

xss attack

</details>

---
*Analysed by Claude on 2026-05-12*
