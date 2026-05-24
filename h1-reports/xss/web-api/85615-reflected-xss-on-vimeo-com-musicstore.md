# Reflected XSS on vimeo.com/musicstore

## Metadata
- **Source:** HackerOne
- **Report:** 85615 | https://hackerone.com/reports/85615
- **Submitted:** 2015-08-30
- **Reporter:** stefanovettorazzi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
__Description__

The value of the parameter _section_ is reflected in the Javascript function `MusicStoreCommon.initialize()` without escaping, which allows to insert Javascript code.

__Proof of concept__
1. Go to https://vimeo.com/musicstore?section=%27-alert(document.domain)-%27.
2. `alert(document.domain)` is executed.

This reflected XSS is reproducible on Chrome, Safari and Firefox.

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

__Description__

The value of the parameter _section_ is reflected in the Javascript function `MusicStoreCommon.initialize()` without escaping, which allows to insert Javascript code.

__Proof of concept__
1. Go to https://vimeo.com/musicstore?section=%27-alert(document.domain)-%27.
2. `alert(document.domain)` is executed.

This reflected XSS is reproducible on Chrome, Safari and Firefox.

</details>

---
*Analysed by Claude on 2026-05-24*
