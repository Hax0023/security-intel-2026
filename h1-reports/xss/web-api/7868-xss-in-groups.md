# XSS in Groups

## Metadata
- **Source:** HackerOne
- **Report:** 7868 | https://hackerone.com/reports/7868
- **Submitted:** 2014-04-17
- **Reporter:** nahamsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Visit the following link after logging in:
http://www.localize.io/pages/create_project/3D

Add a new group with an XSS string (as group name) and you will see the XSS execting.


String used:
<object data=data:text/html;base64,PHN2Zy9vbmxvYWQ9YWxlcnQoNCk+></object>?

Thanks,
Ben

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

Visit the following link after logging in:
http://www.localize.io/pages/create_project/3D

Add a new group with an XSS string (as group name) and you will see the XSS execting.


String used:
<object data=data:text/html;base64,PHN2Zy9vbmxvYWQ9YWxlcnQoNCk+></object>?

Thanks,
Ben

</details>

---
*Analysed by Claude on 2026-05-31*
