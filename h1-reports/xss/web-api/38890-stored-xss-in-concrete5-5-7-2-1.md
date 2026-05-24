# stored XSS in concrete5 5.7.2.1

## Metadata
- **Source:** HackerOne
- **Report:** 38890 | https://hackerone.com/reports/38890
- **Submitted:** 2014-12-10
- **Reporter:** yujitounai
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello.

I found stored XSS in concrete5 5.7.2.1.

If the user have file upload permission
the user can upload the file named like 
"><img src=0 onerror=confirm(document.cookie)>.txt
or 
change title like below
<svg onload=confirm(document.cookie)>
on the properties page.

and when other user access the file manager page,
and open the delete page or open the properties page,
Javascrip

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

I found stored XSS in concrete5 5.7.2.1.

If the user have file upload permission
the user can upload the file named like 
"><img src=0 onerror=confirm(document.cookie)>.txt
or 
change title like below
<svg onload=confirm(document.cookie)>
on the properties page.

and when other user access the file manager page,
and open the delete page or open the properties page,
Javascript execute.

I reported same issue in 5.7.0.4. and fixed [#30019]
but this fix is not sufficient.

Regards.


</details>

---
*Analysed by Claude on 2026-05-24*
