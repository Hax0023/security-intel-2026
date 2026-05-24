# Cross Site Scripting (XSS) - app.relateiq.com

## Metadata
- **Source:** HackerOne
- **Report:** 2439 | https://hackerone.com/reports/2439
- **Submitted:** 2014-02-28
- **Reporter:** quistertow
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
I found a XSS vulnerability in relateiq.com !
1. Go to https://app.relateiq.com/ and click "Register as a new user"
2. Agree the terms and click Continue. Now choose to connect to MS exchange (Microsoft Exchange
Click to connect MS Exchange or Office365)
3.Now enter a random email and click "Connect email"
4. You will receive a error message and 2 new inputs . In the email field put this dada

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

I found a XSS vulnerability in relateiq.com !
1. Go to https://app.relateiq.com/ and click "Register as a new user"
2. Agree the terms and click Continue. Now choose to connect to MS exchange (Microsoft Exchange
Click to connect MS Exchange or Office365)
3.Now enter a random email and click "Connect email"
4. You will receive a error message and 2 new inputs . In the email field put this dada@c.com"><img src=x onerror=alert(document.domain)>  and in the "Override Endpoint Address" put a random website (eg:google.com)
5.Now click on "Connect email" and you will see the XSS alert.

</details>

---
*Analysed by Claude on 2026-05-24*
