# Open redirect in switch account functionality

## Metadata
- **Source:** HackerOne
- **Report:** 390663 | https://hackerone.com/reports/390663
- **Submitted:** 2018-08-05
- **Reporter:** sumni
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Open Redirect
- **CVEs:** CVE-2019-5433
- **Category:** uncategorised

## Summary
To reproduce this vulnerability:
1. You have to be logged in user
2. Enter address: http://<your_local_installation>/www/admin/account-switch.php?return_url=http://127.0.0.1:12345/test 

This is due to unrestricted redirection url passed in in the `return_url` parameter. I would recommend to use some kind of whitelisting or a check if you are redirecting to the same domain you were before.

## Imp

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

To reproduce this vulnerability:
1. You have to be logged in user
2. Enter address: http://<your_local_installation>/www/admin/account-switch.php?return_url=http://127.0.0.1:12345/test 

This is due to unrestricted redirection url passed in in the `return_url` parameter. I would recommend to use some kind of whitelisting or a check if you are redirecting to the same domain you were before.

## Impact

This kind of open redirect vulnerabilities are used in fishing campaigns. I assume that in this case a support request containing a crafted url would have a higher chances of success. For additional malicious url obfuscation you can:
- add some unused parameters that would suggest identifiers of campaigns, other accounts and other revive specific information
- register a domain name similar to the attacked one

</details>

---
*Analysed by Claude on 2026-05-24*
