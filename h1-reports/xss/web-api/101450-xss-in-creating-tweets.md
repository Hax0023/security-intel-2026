# XSS in creating tweets

## Metadata
- **Source:** HackerOne
- **Report:** 101450 | https://hackerone.com/reports/101450
- **Submitted:** 2015-11-24
- **Reporter:** haxs101
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
I found an XSS while tweeting my product.
To reproduce:
* Create new tweet.
* Select any product.
* Input in message content `"><img src=x onerror=alert(document.domain)>
* XSS executes.
* Hit Publish. XSS also executes.



Cheers!


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
I found an XSS while tweeting my product.
To reproduce:
* Create new tweet.
* Select any product.
* Input in message content `"><img src=x onerror=alert(document.domain)>
* XSS executes.
* Hit Publish. XSS also executes.



Cheers!


</details>

---
*Analysed by Claude on 2026-05-24*
