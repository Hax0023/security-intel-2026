# XSS (stored) Wizard is saving executable code

## Metadata
- **Source:** HackerOne
- **Report:** 384517 | https://hackerone.com/reports/384517
- **Submitted:** 2018-07-20
- **Reporter:** nitin_24
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
issue: xss(stored)
Stored XSS occurs when a web application gathers input from a user which might be malicious, and then stores that input in a data store for later use. The stored input is not correctly filtered. As a consequence, the malicious data will appear to be part of the web site and run within the user’s browser under the privileges of the web application.

poc:
url: https://imgsrcxonerr

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

issue: xss(stored)
Stored XSS occurs when a web application gathers input from a user which might be malicious, and then stores that input in a data store for later use. The stored input is not correctly filtered. As a consequence, the malicious data will appear to be part of the web site and run within the user’s browser under the privileges of the web application.

poc:
url: https://imgsrcxonerrorprompt2.rocket.chat

## Impact

Attackers can execute scripts in a victim’s browser to hijack user sessions, deface web sites, insert hostile content, redirect users, hijack the user’s browser using malware, etc.

</details>

---
*Analysed by Claude on 2026-05-24*
