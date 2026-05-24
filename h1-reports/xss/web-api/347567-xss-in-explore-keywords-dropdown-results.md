# XSS in "explore-keywords-dropdown" results.

## Metadata
- **Source:** HackerOne
- **Report:** 347567 | https://hackerone.com/reports/347567
- **Submitted:** 2018-05-04
- **Reporter:** gcurtiss_
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
It seems that people have exploited this vulnerability before on this website, however, it remains unpatched, so here I am reporting the vulnerability.

A XSS vulnerability exists when a restaurant or dish is created with a malicious name. The title of the dish or restaurant is not properly filtered by the web application. Any code in the dish or restaurant name is executed on the client.

DEMO: h

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

It seems that people have exploited this vulnerability before on this website, however, it remains unpatched, so here I am reporting the vulnerability.

A XSS vulnerability exists when a restaurant or dish is created with a malicious name. The title of the dish or restaurant is not properly filtered by the web application. Any code in the dish or restaurant name is executed on the client.

DEMO: https://www.zomato.com/kingman-ks/restaurants, search for: single quote, double quote, GT angle bracket. '">

## Impact

An attacker could achieve XSS and inject hooks into the web browser (e.g. BeEF)

</details>

---
*Analysed by Claude on 2026-05-24*
