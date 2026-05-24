# Stored XSS in partners dashboard

## Metadata
- **Source:** HackerOne
- **Report:** 271765 | https://hackerone.com/reports/271765
- **Submitted:** 2017-09-25
- **Reporter:** bastianwelfrid
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hello


Stored XSS and UI redressing on https://partners.shopify.com/[partnerID]/confirm.

PoC:

1.Change your First Name and Last Name with XSS payload on https://accounts.shopify.com/account
2.Create an account on https://partners.shopify.com/ or if you have an account on https://partners.shopify.com/,go to https://partners.shopify.com/[partnerID]/complete

You'll see the stored XSS


1. https:/

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

Hello


Stored XSS and UI redressing on https://partners.shopify.com/[partnerID]/confirm.

PoC:

1.Change your First Name and Last Name with XSS payload on https://accounts.shopify.com/account
2.Create an account on https://partners.shopify.com/ or if you have an account on https://partners.shopify.com/,go to https://partners.shopify.com/[partnerID]/complete

You'll see the stored XSS


1. https://partners.shopify.com/[partnerID]/confirm
2. https://partners.shopify.com/[partnerID]/complete
are missing with X-Frame-Options header.

Maybe an attacker can attack user with clickjacking.


</details>

---
*Analysed by Claude on 2026-05-24*
