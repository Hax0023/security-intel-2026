# Reflected XSS

## Metadata
- **Source:** HackerOne
- **Report:** 1147060 | https://hackerone.com/reports/1147060
- **Submitted:** 2021-04-03
- **Reporter:** fdeleite
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary
Reflected cross-site scripting (XSS) arises when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way. An attacker can execute JavaScript arbitrary code on the victim's session.

## Impact

-  Perform any action within the application that the user can perform.
-   View any information that the user is able to view.
-   Mo

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

## Summary
Reflected cross-site scripting (XSS) arises when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way. An attacker can execute JavaScript arbitrary code on the victim's session.

## Impact

-  Perform any action within the application that the user can perform.
-   View any information that the user is able to view.
-   Modify any information that the user is able to modify.
-   Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user..
- Steal user's cookie. 

 ### Supporting Material/References:

https://hackerone.com/reports/438240
https://portswigger.net/web-security/cross-site-scripting/reflected

## System Host(s)
www.██████.mil

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Go to:

 - https://www.█████████.mil/██████████=%27%3Balert(%27XSS!%27)%2F%2F

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
