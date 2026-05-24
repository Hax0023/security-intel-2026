# Stored XSS in concrete5 5.7.0.4.

## Metadata
- **Source:** HackerOne
- **Report:** 30019 | https://hackerone.com/reports/30019
- **Submitted:** 2014-10-05
- **Reporter:** yujitounai
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello.

I found stored XSS in concrete5 5.7.0.4.

If the user have file upload permission
the user can upload the file named like 
"><svg onload=confirm(document.cookie)>.txt
and the file name is displayed without being escaped.

and when other user access the file manager page,
Execute Javascript code on page load.

Regards.


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

Hello.

I found stored XSS in concrete5 5.7.0.4.

If the user have file upload permission
the user can upload the file named like 
"><svg onload=confirm(document.cookie)>.txt
and the file name is displayed without being escaped.

and when other user access the file manager page,
Execute Javascript code on page load.

Regards.


</details>

---
*Analysed by Claude on 2026-05-24*
