# XSS in Desktop Client via user status and information

## Metadata
- **Source:** HackerOne
- **Report:** 1707977 | https://hackerone.com/reports/1707977
- **Submitted:** 2022-09-21
- **Reporter:** b911bade858ce8e6a0f50f8
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Resource Injection
- **CVEs:** CVE-2022-39332
- **Category:** web-api

## Summary
## Summary:
The `Nextcloud Desktop Client` application does not properly neutralize the `Full Name` and `Status Message` of users before using them.

## Steps To Reproduce:

### Server Machine:
1. Install the `Nextcloud Server` application
2. Log into your account
3. Navigate to your profile page
4. Set the `Full Name` of your user to `<img src="https://avatars.githubusercontent.com/u/99037623">`


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

## Summary:
The `Nextcloud Desktop Client` application does not properly neutralize the `Full Name` and `Status Message` of users before using them.

## Steps To Reproduce:

### Server Machine:
1. Install the `Nextcloud Server` application
2. Log into your account
3. Navigate to your profile page
4. Set the `Full Name` of your user to `<img src="https://avatars.githubusercontent.com/u/99037623">`
5. Set the `Status Message` of your user to `<img src="https://avatars.githubusercontent.com/u/99037623">`

### Client Machine:
6. Install the `Nextcloud Desktop Client` application onto a machine that is running the `Windows 10` operating system
7. Log into your account
8. Open the main dialog window of the `Nextcloud Desktop Client` application
9. Observe that the `Full Name` and `Status Message` of your user are treated as `HyperText Markup Language`

## Supporting Material/References:
{F1945608}

## Impact

An attacker can inject arbitrary `HyperText Markup Language` into the `Nextcloud Desktop Client` application.

</details>

---
*Analysed by Claude on 2026-05-24*
