# Reflected XSS on help.steampowered.com

## Metadata
- **Source:** HackerOne
- **Report:** 390429 | https://hackerone.com/reports/390429
- **Submitted:** 2018-08-04
- **Reporter:** xpaw
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
URL: https://help.steampowered.com/en/wizard/HelpWithGameIssue/?appid=704740&issueid=125&option=%3Ch1%3Eunfiltered

It puts `option` option into a translation token `<div class="help_page_title">#Help_Game_MissingItemsTitle{user controlled string here}`

And if there's no such translation token, it just prints out the entire user input unescaped.

## Impact

XSS.

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

URL: https://help.steampowered.com/en/wizard/HelpWithGameIssue/?appid=704740&issueid=125&option=%3Ch1%3Eunfiltered

It puts `option` option into a translation token `<div class="help_page_title">#Help_Game_MissingItemsTitle{user controlled string here}`

And if there's no such translation token, it just prints out the entire user input unescaped.

## Impact

XSS.

</details>

---
*Analysed by Claude on 2026-05-24*
