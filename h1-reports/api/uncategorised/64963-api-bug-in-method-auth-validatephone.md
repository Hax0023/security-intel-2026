# API: Bug in method auth.validatePhone

## Metadata
- **Source:** HackerOne
- **Report:** 64963 | https://hackerone.com/reports/64963
- **Submitted:** 2015-05-30
- **Reporter:** vladislav805
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** api
- **CVEs:** None
- **Category:** uncategorised

## Summary
The bug is that auth.validatePhone does not validate the parameter "sid". In theory he should be in the format "2fa_$userId_$appId_$hash", but to get the correct result (send SMS/make call) enough only "2fa_$userId_$anyText".

For example, these requests will send a SMS:
https://api.vk.com/method/auth.validatePhone?sid=2fa_23048942_lolka
https://api.vk.com/method/auth.validatePhone?sid=2fa_667

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

The bug is that auth.validatePhone does not validate the parameter "sid". In theory he should be in the format "2fa_$userId_$appId_$hash", but to get the correct result (send SMS/make call) enough only "2fa_$userId_$anyText".

For example, these requests will send a SMS:
https://api.vk.com/method/auth.validatePhone?sid=2fa_23048942_lolka
https://api.vk.com/method/auth.validatePhone?sid=2fa_66748_блаблабла

It turns out that with this endlessly send SMS with the activation code, and to call if the request to add voice=1:
https://api.vk.com/method/auth.validatePhone?sid=2fa_66748_блаблабла&voice=1

There is also another bug. SMS and calls will be carried out in any case, even if the user has disabled two-factor authentication.
// I don't know, are you interested. But there is a bug - I reported.

</details>

---
*Analysed by Claude on 2026-05-24*
