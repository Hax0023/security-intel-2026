# Unauthenticated reflected XSS in preview_as_user function

## Metadata
- **Source:** HackerOne
- **Report:** 643442 | https://hackerone.com/reports/643442
- **Submitted:** 2019-07-15
- **Reporter:** arcturian
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
An unauthenticated, reflected cross-site-scripting attack is possible due to the unsanitised `cID` parameter in the preview_as_user functionality.

Example URL: `https://LOCAL-CONCRETE-INSTALL/ccm/system/panels/page/preview_as_user/preview?cID=%22%3E%3C/iframe%3E%3Cscript%3Ealert(1)%3C/script%3E%3C!--`

The error is in the `concrete/views/panels/page/preview_as/frame.php` file, line 4:
```
[..]
sr

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

An unauthenticated, reflected cross-site-scripting attack is possible due to the unsanitised `cID` parameter in the preview_as_user functionality.

Example URL: `https://LOCAL-CONCRETE-INSTALL/ccm/system/panels/page/preview_as_user/preview?cID=%22%3E%3C/iframe%3E%3Cscript%3Ealert(1)%3C/script%3E%3C!--`

The error is in the `concrete/views/panels/page/preview_as/frame.php` file, line 4:
```
[..]
src="<?= URL::to('/ccm/system/panels/page/preview_as_user/render') . '?&cID=' . Request::request('cID') ?>
[..]
```

Solutions would be to either cast this value to an int with `intval()`, or pass the value through `htmlentities()` before rendering it. Or both!

## Impact

An attacker could steal cookies or perform actions on other users behalf.

</details>

---
*Analysed by Claude on 2026-05-24*
