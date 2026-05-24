# CSRF on https://apps.topcoder.com/wiki/pages/doattachfile.action

## Metadata
- **Source:** HackerOne
- **Report:** 867473 | https://hackerone.com/reports/867473
- **Submitted:** 2020-05-06
- **Reporter:** meryem0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi :) There is a CSRF on attaching files to wiki pages.

## Steps To Reproduce:
There is no CSRF token or anything like that on https://apps.topcoder.com/wiki/pages/doattachfile.action?pageId= . I added the poc html file below. When someone opens this html file, or we can add it into our website, he/she creates an attachment unwillingly.

This file creates csrf.txt on https://apps.topc

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
Hi :) There is a CSRF on attaching files to wiki pages.

## Steps To Reproduce:
There is no CSRF token or anything like that on https://apps.topcoder.com/wiki/pages/doattachfile.action?pageId= . I added the poc html file below. When someone opens this html file, or we can add it into our website, he/she creates an attachment unwillingly.

This file creates csrf.txt on https://apps.topcoder.com/wiki/pages/doattachfile.action?pageId=165871793

Note: This only works to signed-in users. Because unauthorized users cannot upload attachments. There is a mistake on https://apps.topcoder.com/wiki/login.action now. If you encounter an error, you can login on main site (https://accounts.topcoder.com/member) then try.

## Impact

An attacker can force other users to upload files without their knowledge.

</details>

---
*Analysed by Claude on 2026-05-24*
