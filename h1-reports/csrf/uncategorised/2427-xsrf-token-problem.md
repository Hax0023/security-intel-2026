# XSRF token problem

## Metadata
- **Source:** HackerOne
- **Report:** 2427 | https://hackerone.com/reports/2427
- **Submitted:** 2014-02-28
- **Reporter:** shahmeer-amir
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
Your web application generates XSRF token values inside cookies which is not a best practice for web applications as revelation of cookies can reveal XSRF Tokens as well. Authenticity tokens should be kept separate from cookies and should be isolated to change operations in the account only.

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

Your web application generates XSRF token values inside cookies which is not a best practice for web applications as revelation of cookies can reveal XSRF Tokens as well. Authenticity tokens should be kept separate from cookies and should be isolated to change operations in the account only.

</details>

---
*Analysed by Claude on 2026-05-24*
