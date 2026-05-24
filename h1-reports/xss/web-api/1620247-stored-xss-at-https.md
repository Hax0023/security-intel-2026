# Stored XSS at https://█████

## Metadata
- **Source:** HackerOne
- **Report:** 1620247 | https://hackerone.com/reports/1620247
- **Submitted:** 2022-06-30
- **Reporter:** r0x0rz
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**
In registeration page ( https://████ ) , first name and last name field are vulnerable to Stored Cross Site Scripting.

## Proof of concept
For the fastly test, use this credentials to login (my test account)
> email: █████████
password: ██████

After login , alert document.cookie will triggered

## Impact

Stored Cross Site Scripting which attacker can execute malicious javascrip

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

**Description:**
In registeration page ( https://████ ) , first name and last name field are vulnerable to Stored Cross Site Scripting.

## Proof of concept
For the fastly test, use this credentials to login (my test account)
> email: █████████
password: ██████

After login , alert document.cookie will triggered

## Impact

Stored Cross Site Scripting which attacker can execute malicious javascript payload.

## System Host(s)
████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Go to registration page ( https://████ ), insert `<svg/onload=confirm(document.cookie)>` payload in firstname and lastname fields and create account.
2. Verified your account.
3. Go to login page and login your account.
4. And XSS will triggered ( XSS also triggered in `My Profile` page) .

## Suggested Mitigation/Remediation Actions
1. Filter input on arrival.
2. Encode data on output.
3. Content Security Policy



</details>

---
*Analysed by Claude on 2026-05-24*
