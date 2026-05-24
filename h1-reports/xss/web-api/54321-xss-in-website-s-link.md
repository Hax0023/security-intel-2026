# Xss in website's link

## Metadata
- **Source:** HackerOne
- **Report:** 54321 | https://hackerone.com/reports/54321
- **Submitted:** 2015-04-02
- **Reporter:** bohdansec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I found Xss in my website's link.

Steps:

Go to this page https://app.shopify.com/services/partners/account/edit
In fileld "Website (optional)" add javascript:alert(document.cookie);//http://dgddfgdfgg.ua
and save

Need registration https://experts.shopify.com/signup

After we can see account. Click link website

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

I found Xss in my website's link.

Steps:

Go to this page https://app.shopify.com/services/partners/account/edit
In fileld "Website (optional)" add javascript:alert(document.cookie);//http://dgddfgdfgg.ua
and save

Need registration https://experts.shopify.com/signup

After we can see account. Click link website

</details>

---
*Analysed by Claude on 2026-05-24*
