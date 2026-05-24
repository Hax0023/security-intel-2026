# Stored XSS in comments

## Metadata
- **Source:** HackerOne
- **Report:** 148751 | https://hackerone.com/reports/148751
- **Submitted:** 2016-07-01
- **Reporter:** kelunik
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Comments can contain an author's website. This website is used in the href attribute of link elements and isn't filtered. Thus it allows URLs like `javascript:alert(1)` to be used. These URLs must be filtered by protocol, e.g. only allow http and https.

These attacks are blocked by the default CSP, but clients not supporting CSP or changed CSPs may be affected.

This issue affects [Airship](https

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

Comments can contain an author's website. This website is used in the href attribute of link elements and isn't filtered. Thus it allows URLs like `javascript:alert(1)` to be used. These URLs must be filtered by protocol, e.g. only allow http and https.

These attacks are blocked by the default CSP, but clients not supporting CSP or changed CSPs may be affected.

This issue affects [Airship](https://github.com/paragonie/airship) Version 1.1.2 and lower.

</details>

---
*Analysed by Claude on 2026-05-24*
