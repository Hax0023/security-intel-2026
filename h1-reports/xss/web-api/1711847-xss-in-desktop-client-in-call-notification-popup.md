# XSS in Desktop Client in call notification popup

## Metadata
- **Source:** HackerOne
- **Report:** 1711847 | https://hackerone.com/reports/1711847
- **Submitted:** 2022-09-25
- **Reporter:** b911bade858ce8e6a0f50f8
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Resource Injection
- **CVEs:** CVE-2022-39333
- **Category:** web-api

## Summary
## Summary:
The `Nextcloud Desktop Client` application does not properly neutralize the name of a group conversation before using it.

## Steps To Reproduce:
### Server Machine:
1. Install the `Nextcloud Server` application
2. Create an administrator account
3. Create a user account

### Client Machine:
4. Install the `Nextcloud Desktop Client` application on a machine that is running the `Windows

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
The `Nextcloud Desktop Client` application does not properly neutralize the name of a group conversation before using it.

## Steps To Reproduce:
### Server Machine:
1. Install the `Nextcloud Server` application
2. Create an administrator account
3. Create a user account

### Client Machine:
4. Install the `Nextcloud Desktop Client` application on a machine that is running the `Windows 10` operating system
5. Log in to the user account

### Server Machine:
6. Log in to the administrator account
7. Install the `Nextcloud Talk` application
8. Open the `Nextcloud Talk` application
9. Create a group conversation with the name `<img src="https://avatars.githubusercontent.com/u/99037623">`
10. Add the user to the group conversation
11. Start a call in the group conversation

### Client Machine:
12. Observe that the name of the group conversation is treated as `HyperText Markup Language`

Please do note that group conversation messages are also treated as `HyperText Markup Language`.

## Supporting Material/References:
{F1953705}
{F1953706}
{F1953851}

## Impact

An attacker can inject arbitrary `HyperText Markup Language` in to the `Nextcloud Desktop Client` application.

</details>

---
*Analysed by Claude on 2026-05-24*
