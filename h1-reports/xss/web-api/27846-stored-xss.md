# Stored xss

## Metadata
- **Source:** HackerOne
- **Report:** 27846 | https://hackerone.com/reports/27846
- **Submitted:** 2014-09-11
- **Reporter:** detroitsmash
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi!

There's a stored xss on ads.twitter.com under "Add New App" section at https://ads.twitter.com/accounts/18ce53wsl3g/campaigns/new_objective/app_installs. 

There's a option to add android application by Google play app id, so i searched for a app on play store with name " "><img src=x onerror=alert(1)>" " and then i got this app https://play.google.com/store/apps/details?id=com.rssappmake

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

Hi!

There's a stored xss on ads.twitter.com under "Add New App" section at https://ads.twitter.com/accounts/18ce53wsl3g/campaigns/new_objective/app_installs. 

There's a option to add android application by Google play app id, so i searched for a app on play store with name " "><img src=x onerror=alert(1)>" " and then i got this app https://play.google.com/store/apps/details?id=com.rssappmaker.athe319.

So to reproduce this copy paste the app id "com.rssappmaker.athe319" in that box and then click on "add app" button. After that this xss will be triggered. See the attached image poc.png

Tested in latest version of chrome.

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
