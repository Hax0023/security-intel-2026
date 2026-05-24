# Reflected XSS due to vulnerable version of sockjs

## Metadata
- **Source:** HackerOne
- **Report:** 1100326 | https://hackerone.com/reports/1100326
- **Submitted:** 2021-02-10
- **Reporter:** chip_sec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
There is reflected XSS on *.simperium.com. The bug exists due to a vulnerable version of sockjs library.

## Platform(s) Affected:
simperium.com
js.simperium.com

## Steps To Reproduce:
  1. Visit https://simperium.com/sock/1/0/0/0/htmlfile?c=alert('XSS')//
  2. You will see an alert message because of executed JS

## Impact

XSS may be used by an attacker to perform a lot of things, f

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
There is reflected XSS on *.simperium.com. The bug exists due to a vulnerable version of sockjs library.

## Platform(s) Affected:
simperium.com
js.simperium.com

## Steps To Reproduce:
  1. Visit https://simperium.com/sock/1/0/0/0/htmlfile?c=alert('XSS')//
  2. You will see an alert message because of executed JS

## Impact

XSS may be used by an attacker to perform a lot of things, for example, to steal user session

</details>

---
*Analysed by Claude on 2026-05-24*
