# Server-Side Request Forgery (SSRF)

## Metadata
- **Source:** HackerOne
- **Report:** 382048 | https://hackerone.com/reports/382048
- **Submitted:** 2018-07-16
- **Reporter:** t-pwn
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I've found a Server-Side Request Forgery (SSRF)

Steps to reproduce:

+ start listening on your server 
+ navigate to http://██████/help/ACPS.htm#http://$yourserver:$port
+ you will get the request

██████

## Impact

Server-Side Request Forgery (SSRF) Attack

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

I've found a Server-Side Request Forgery (SSRF)

Steps to reproduce:

+ start listening on your server 
+ navigate to http://██████/help/ACPS.htm#http://$yourserver:$port
+ you will get the request

██████

## Impact

Server-Side Request Forgery (SSRF) Attack

</details>

---
*Analysed by Claude on 2026-05-24*
