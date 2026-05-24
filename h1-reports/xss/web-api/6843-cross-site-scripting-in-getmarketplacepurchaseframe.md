# Cross-Site Scripting in getMarketplacePurchaseFrame

## Metadata
- **Source:** HackerOne
- **Report:** 6843 | https://hackerone.com/reports/6843
- **Submitted:** 2014-04-10
- **Reporter:** melvin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The `$mp->getProductBlockID()` variable in the `getMarketplacePurchaseFrame` function ([view on Github](https://github.com/concrete5/concrete5/blob/851806af393fa2958d52db9b48e0a8c83100f609/web/concrete/core/libraries/marketplace.php#L176)) is not being filtered properly to protect against HTML injection/XSS.

This leads to XSS vulnerabilities in (for example) `connect.php` on line 14 ([view on G

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

The `$mp->getProductBlockID()` variable in the `getMarketplacePurchaseFrame` function ([view on Github](https://github.com/concrete5/concrete5/blob/851806af393fa2958d52db9b48e0a8c83100f609/web/concrete/core/libraries/marketplace.php#L176)) is not being filtered properly to protect against HTML injection/XSS.

This leads to XSS vulnerabilities in (for example) `connect.php` on line 14 ([view on Github](https://github.com/concrete5/concrete5/blob/851806af393fa2958d52db9b48e0a8c83100f609/web/concrete/single_pages/dashboard/extend/connect.php#L14)) when visiting a URL like: *dashboard/extend/connect/"%20onmouseover="alert(document.cookie)">*.

</details>

---
*Analysed by Claude on 2026-05-24*
