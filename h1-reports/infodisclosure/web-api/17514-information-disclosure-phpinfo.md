# Information Disclosure (phpinfo())

## Metadata
- **Source:** HackerOne
- **Report:** 17514 | https://hackerone.com/reports/17514
- **Submitted:** 2014-06-25
- **Reporter:** yourdarkshadow
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
URL :- https://staging.uzbey.com/phpinfo.php

Description :-
phpinfo() is a debug functionality that prints out detailed information on both the system and the PHP configuration.

An attacker can obtain information such as: 
•Exact PHP version.
•Exact OS and its version.
•Details of the PHP configuration.
•Internal IP addresses.
•Server environment variables.
•Loaded PHP extensions and 

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

URL :- https://staging.uzbey.com/phpinfo.php

Description :-
phpinfo() is a debug functionality that prints out detailed information on both the system and the PHP configuration.

An attacker can obtain information such as: 
•Exact PHP version.
•Exact OS and its version.
•Details of the PHP configuration.
•Internal IP addresses.
•Server environment variables.
•Loaded PHP extensions and their configurations.
This information can help an attacker gain more information on the system. After gaining detailed information, the attacker can research known vulnerabilities for that system under review. The attacker can also use this information during the exploitation of other vulnerabilities. 

</details>

---
*Analysed by Claude on 2026-05-24*
