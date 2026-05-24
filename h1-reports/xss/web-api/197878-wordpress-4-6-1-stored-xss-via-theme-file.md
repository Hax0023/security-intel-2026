# WordPress <= 4.6.1 Stored XSS Via Theme File

## Metadata
- **Source:** HackerOne
- **Report:** 197878 | https://hackerone.com/reports/197878
- **Submitted:** 2017-01-12
- **Reporter:** madrobot
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello __Team__,

__Description__:-
>Vulnerable code is located at /wp-admin/includes/class-theme-installer-skin.php

__POC__:-
https://nextcloud.com/readme.html

{F151887}



__FIX__:-
Upgrade wordpress to latest


__Refer__:-
>https://wpvulndb.com/vulnerabilities/8718
>https://www.mehmetince.net/low-severity-wordpress/

__Attack Scenario__:-
1 – Attacker uploads a theme as a zip file.
2 – Webmast

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

Hello __Team__,

__Description__:-
>Vulnerable code is located at /wp-admin/includes/class-theme-installer-skin.php

__POC__:-
https://nextcloud.com/readme.html

{F151887}



__FIX__:-
Upgrade wordpress to latest


__Refer__:-
>https://wpvulndb.com/vulnerabilities/8718
>https://www.mehmetince.net/low-severity-wordpress/

__Attack Scenario__:-
1 – Attacker uploads a theme as a zip file.
2 – Webmaster who just want to download a theme and then upload, takes a theme file.
3 – And upload it without verify content of zip file.


__Regards__,
Santhosh


</details>

---
*Analysed by Claude on 2026-05-24*
