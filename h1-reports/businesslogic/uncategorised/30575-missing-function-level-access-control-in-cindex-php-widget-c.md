# Missing Function Level Access Control in /cindex.php/widget/customize/

## Metadata
- **Source:** HackerOne
- **Report:** 30575 | https://hackerone.com/reports/30575
- **Submitted:** 2014-10-08
- **Reporter:** adrianomarcmont
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
Most web applications verify function level access rights before making that functionality visible in the UI. However, applications need to perform the same access control checks on the server when each function is accessed. If requests are not verified, attackers will be able to forge requests in order to access functionality without proper authorization.

The URL "https://www.bookfresh.com/cin

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

Most web applications verify function level access rights before making that functionality visible in the UI. However, applications need to perform the same access control checks on the server when each function is accessed. If requests are not verified, attackers will be able to forge requests in order to access functionality without proper authorization.

The URL "https://www.bookfresh.com/cindex.php/widget/customize/" is accessible to anyone even without authentication. The page should only be accessible to authenticated users.

</details>

---
*Analysed by Claude on 2026-05-24*
