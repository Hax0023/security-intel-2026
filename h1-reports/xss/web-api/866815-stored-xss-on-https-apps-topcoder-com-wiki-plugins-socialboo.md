# Stored XSS on https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action

## Metadata
- **Source:** HackerOne
- **Report:** 866815 | https://hackerone.com/reports/866815
- **Submitted:** 2020-05-05
- **Reporter:** meryem0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi :) Adding javascript url causes to stored XSS when creating bookmark.

## Steps To Reproduce:

Go to https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action . Write `javascript:alert(document.domain)` on url input and fill other areas. After create, go `https://apps.topcoder.com/wiki/display/tcwiki/<TITLE>` and when you click the title on this page, XSS will e

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

## Summary:
Hi :) Adding javascript url causes to stored XSS when creating bookmark.

## Steps To Reproduce:

Go to https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action . Write `javascript:alert(document.domain)` on url input and fill other areas. After create, go `https://apps.topcoder.com/wiki/display/tcwiki/<TITLE>` and when you click the title on this page, XSS will execute.

PoC:
https://apps.topcoder.com/wiki/display/tcwiki/powerpuff_hackerone_test
{F816754}

## Impact

XSS can use to steal cookies or to run arbitrary code on victim's browser.

</details>

---
*Analysed by Claude on 2026-05-24*
