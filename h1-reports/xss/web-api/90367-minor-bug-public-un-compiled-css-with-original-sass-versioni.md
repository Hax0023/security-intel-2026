# Minor Bug: Public un-compiled CSS with original sass, versioning, source map, comments, etc.

## Metadata
- **Source:** HackerOne
- **Report:** 90367 | https://hackerone.com/reports/90367
- **Submitted:** 2015-09-24
- **Reporter:** ericr
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A stylesheet is available in a non-minified, non-compiled format. It includes sass, versioning, a source map, a style guide, comments, etc. (see base64 encoded string at the very end of the document).

https://hackerone.com/assets/application.css

This alone is obviously not an exploit. However, it can divulge information under the pretense that original sass, style guide, comments, etc. are priva

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

A stylesheet is available in a non-minified, non-compiled format. It includes sass, versioning, a source map, a style guide, comments, etc. (see base64 encoded string at the very end of the document).

https://hackerone.com/assets/application.css

This alone is obviously not an exploit. However, it can divulge information under the pretense that original sass, style guide, comments, etc. are private and thus are an appropriate medium for not-so-public things. In other words, it can lead to some interesting internal information disclosure.

</details>

---
*Analysed by Claude on 2026-05-24*
