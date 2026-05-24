# Client side authentication leads to Auth Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1877989 | https://hackerone.com/reports/1877989
- **Submitted:** 2023-02-17
- **Reporter:** kalkii
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi Team

I have found  that to access the data of endpoint ```https://████████/███/?#/``` as user has to submit a password/passphrase.
When we provide wrong password then we get and error message asked to get pass assistance message  ```Contact ████ for password assistance.``` 
After analyzing the JS file I found that when correct password is provide a parameter is set in the localstorage "███████

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

Hi Team

I have found  that to access the data of endpoint ```https://████████/███/?#/``` as user has to submit a password/passphrase.
When we provide wrong password then we get and error message asked to get pass assistance message  ```Contact ████ for password assistance.``` 
After analyzing the JS file I found that when correct password is provide a parameter is set in the localstorage "███████:true"

## Impact

Auth bypass lead to sensitive data exposer like phone number, email id etc.

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Visit https://███/█████/?#/
2. Set a new parameter in local storage name ```█████``` and value ```true```
3. Reload the page

█████

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
