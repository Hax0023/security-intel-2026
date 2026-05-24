# Spamming any user from Reset Password Function

## Metadata
- **Source:** HackerOne
- **Report:** 223525 | https://hackerone.com/reports/223525
- **Submitted:** 2017-04-24
- **Reporter:** atruba
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
It is possible to spam any user whose email-id is known.

csrfmiddlewaretoken token can be used more than one.
Users can be spammed heavily by just Brute force attack on password reset page.

Implementtion:
Implement a Captcha.

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

It is possible to spam any user whose email-id is known.

csrfmiddlewaretoken token can be used more than one.
Users can be spammed heavily by just Brute force attack on password reset page.

Implementtion:
Implement a Captcha.

</details>

---
*Analysed by Claude on 2026-05-24*
