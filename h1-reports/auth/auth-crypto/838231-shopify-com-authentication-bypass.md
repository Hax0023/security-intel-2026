# *.shopify.com - Authentication bypass

## Metadata
- **Source:** HackerOne
- **Report:** 838231 | https://hackerone.com/reports/838231
- **Submitted:** 2020-04-03
- **Reporter:** nooblife
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** auth
- **CVEs:** None
- **Category:** auth-crypto

## Summary
I´ve found a flaw in the authentication process when accessing the website https://upcoming.shopify.com. There seems to be an HTTP Authentication in place to prevent access without authentication. Please follow below POC to get access to https://upcoming.shopify.com without login. The website is full with weird behavior and i´m able to register new accounts via https://upcoming.shopify.com. That c

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

I´ve found a flaw in the authentication process when accessing the website https://upcoming.shopify.com. There seems to be an HTTP Authentication in place to prevent access without authentication. Please follow below POC to get access to https://upcoming.shopify.com without login. The website is full with weird behavior and i´m able to register new accounts via https://upcoming.shopify.com. That could maybe lead to some internal issues.

***Normal request***
{F772305}

***POC**
1) Go to: https://upcoming.shopify.com/tools
2) From that point you can travel to any endpoint

{F772313}
{F772314}
{F772315}

## Impact

High

</details>

---
*Analysed by Claude on 2026-05-24*
