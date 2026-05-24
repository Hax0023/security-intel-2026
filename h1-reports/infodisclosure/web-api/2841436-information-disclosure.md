# information disclosure 

## Metadata
- **Source:** HackerOne
- **Report:** 2841436 | https://hackerone.com/reports/2841436
- **Submitted:** 2024-11-14
- **Reporter:** rono_07
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** infodisclosure
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:

web.archive.org -website
web. Archive is a website like google search, but he saves all links. Wayback disclosing URL's without users' permission,


Anyone can access them maybe (emails and passwords) they are notes they should be private and see everything
just by searching about random notes
and it doesn't work like that , its should be:
only people who i want them to see my notes c

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

web.archive.org -website
web. Archive is a website like google search, but he saves all links. Wayback disclosing URL's without users' permission,


Anyone can access them maybe (emails and passwords) they are notes they should be private and see everything
just by searching about random notes
and it doesn't work like that , its should be:
only people who i want them to see my notes can access them
not any random people find my notes on web.archive.org/

url : https://web.archive.org/web/*/https://github.com/curl/curl*
url : https://web.archive.org/web/*/https://curl.se*


Fix:
block web.archive.org from disclose your websites.
so i really hope you will review that and fix it to keep your users safe because they maybe save emails or passwords or company information's and they want to share them only with company employers, i will wait an update from you :)

## Impact

attacker can access notes without permission

</details>

---
*Analysed by Claude on 2026-05-24*
