# XSS on Vimeo

## Metadata
- **Source:** HackerOne
- **Report:** 45484 | https://hackerone.com/reports/45484
- **Submitted:** 2015-01-28
- **Reporter:** niyaax
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Poc video:
XSS on Vimeo: http://youtu.be/w5QgEEcMARY

1. Go to https://vimeo.com/settings/profile
2. Add a link with the payload on URL: javascript:alert(document.domain+"http://")
3. Click the link and payload will execute.

Thanks
@niyaax

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

Poc video:
XSS on Vimeo: http://youtu.be/w5QgEEcMARY

1. Go to https://vimeo.com/settings/profile
2. Add a link with the payload on URL: javascript:alert(document.domain+"http://")
3. Click the link and payload will execute.

Thanks
@niyaax

</details>

---
*Analysed by Claude on 2026-05-24*
