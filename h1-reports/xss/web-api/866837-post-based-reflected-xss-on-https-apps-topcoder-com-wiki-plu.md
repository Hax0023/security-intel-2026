# Post Based Reflected XSS on https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action

## Metadata
- **Source:** HackerOne
- **Report:** 866837 | https://hackerone.com/reports/866837
- **Submitted:** 2020-05-05
- **Reporter:** meryem0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi :) A post based reflected XSS occurs when creating bookmarks.

## Steps To Reproduce:
`Title` and `Labels` parameters are vulnerable to XSS on https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action. This form uses POST request so i added HTML file below. When someone opens this html file, or we can add it into our website, XSS will execute.

{F816815}
{F81681

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
Hi :) A post based reflected XSS occurs when creating bookmarks.

## Steps To Reproduce:
`Title` and `Labels` parameters are vulnerable to XSS on https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action. This form uses POST request so i added HTML file below. When someone opens this html file, or we can add it into our website, XSS will execute.

{F816815}
{F816816}

## Impact

XSS can use to steal cookies or to run arbitrary code on victim's browser.

</details>

---
*Analysed by Claude on 2026-05-24*
