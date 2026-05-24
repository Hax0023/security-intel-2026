# Stored XSS from Display Settings triggered on Save and viewing realtime search demo

## Metadata
- **Source:** HackerOne
- **Report:** 156387 | https://hackerone.com/reports/156387
- **Submitted:** 2016-08-03
- **Reporter:** ctee
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Here are the steps to trigger the XSS:

1. Create a JSON record that will contain the following attribute:
     **{"<img src=1 onerror=alert(document.domain)>": "XSS attribute"}**

2. Go to  **Indices -> Display** and select the attribute **<img src=1 onerror=alert(document.domain)>** under **Attributes for Faceting** and click save. 

3. Note that XSS is triggered multiple times on that page.

4.

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

Here are the steps to trigger the XSS:

1. Create a JSON record that will contain the following attribute:
     **{"<img src=1 onerror=alert(document.domain)>": "XSS attribute"}**

2. Go to  **Indices -> Display** and select the attribute **<img src=1 onerror=alert(document.domain)>** under **Attributes for Faceting** and click save. 

3. Note that XSS is triggered multiple times on that page.

4. XSS  is now triggered on **https://www.algolia.com/explorer#?index=index_name** as it also shows the attribute.

5. Create a public UI Demo and to the public url, xss is triggered. I've created a demo url:  https://www.algolia.com/realtime-search-demo/xsstest


</details>

---
*Analysed by Claude on 2026-05-24*
