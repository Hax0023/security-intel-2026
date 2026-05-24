# XSS On meta tags in profile page

## Metadata
- **Source:** HackerOne
- **Report:** 159984 | https://hackerone.com/reports/159984
- **Submitted:** 2016-08-17
- **Reporter:** plazmaz
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The profile page (https://gitlab.com/u/<user>) does not properly sanitize quotation marks, allowing for injection of attributes into the meta tags. This allows for redirection to phishing sites and other various nefarious things. I've managed to get my [profile page](https://gitlab.com/u/Plazmaz) to redirect to Bing by setting my bio to 
`0;url=http://www.bing.com" http-equiv="refresh`

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

The profile page (https://gitlab.com/u/<user>) does not properly sanitize quotation marks, allowing for injection of attributes into the meta tags. This allows for redirection to phishing sites and other various nefarious things. I've managed to get my [profile page](https://gitlab.com/u/Plazmaz) to redirect to Bing by setting my bio to 
`0;url=http://www.bing.com" http-equiv="refresh`

</details>

---
*Analysed by Claude on 2026-05-24*
