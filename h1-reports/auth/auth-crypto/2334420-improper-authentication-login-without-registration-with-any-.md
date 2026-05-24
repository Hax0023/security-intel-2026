# Improper Authentication (Login without Registration with any user) at ████

## Metadata
- **Source:** HackerOne
- **Report:** 2334420 | https://hackerone.com/reports/2334420
- **Submitted:** 2024-01-25
- **Reporter:** archyxsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi Team!

I found a security issue in ███████. An attacker could login as a any user without registration in the page and above all it can change the session of a victim and authenticate him as any user. 

The problem is at the endpoint  ██████████ which, thanks to the **signin** parameter, allows to authenticate anyone with any user.

## Impact

Authentication bypass (Login as any user without au

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

Hi Team!

I found a security issue in ███████. An attacker could login as a any user without registration in the page and above all it can change the session of a victim and authenticate him as any user. 

The problem is at the endpoint  ██████████ which, thanks to the **signin** parameter, allows to authenticate anyone with any user.

## Impact

Authentication bypass (Login as any user without authentication)
Force a victim to change session with other user

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Go to ██████████
2. To check the authentication bypass go to ████:

███

As the link corresponds to a GET request you can force any user to log out and authenticate to any other account.

Additional bonus: *clientid and clientsecret are stored in the page source*

███████

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
