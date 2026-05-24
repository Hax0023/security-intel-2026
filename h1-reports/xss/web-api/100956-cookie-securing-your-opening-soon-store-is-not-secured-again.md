# Cookie securing your "Opening soon" store is not secured against XSS

## Metadata
- **Source:** HackerOne
- **Report:** 100956 | https://hackerone.com/reports/100956
- **Submitted:** 2015-11-22
- **Reporter:** hafolife
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
PoC:
1) Protect your e-shop with a password (Storefront password)
2) Go to your e-shop URL and enter the password to access the store
3) There is a cookie created - name: storefront_digest - this cookie contains the password (in a secure way) which protects your store
4) This cookie is not marked as HttpOnly, so if there is e.g. XSS, anyone can steal this cookie
5) With this cookie anyone can acce

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

PoC:
1) Protect your e-shop with a password (Storefront password)
2) Go to your e-shop URL and enter the password to access the store
3) There is a cookie created - name: storefront_digest - this cookie contains the password (in a secure way) which protects your store
4) This cookie is not marked as HttpOnly, so if there is e.g. XSS, anyone can steal this cookie
5) With this cookie anyone can access your "Opening soon" e-shop, even if he doesn't know the password

Before you answered I would like to confirm that I read shopify terms and:
1) I don't care about he password strength. It is not important in that case
2) I am pretty sure that this cookie - storefront_digest - is a sensitive cookie since by stealing this cookie you can access resources you shouldn't be able to...

Thank you. 

</details>

---
*Analysed by Claude on 2026-05-24*
