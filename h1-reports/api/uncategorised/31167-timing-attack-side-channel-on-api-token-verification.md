# Timing Attack Side-Channel on API Token Verification

## Metadata
- **Source:** HackerOne
- **Report:** 31167 | https://hackerone.com/reports/31167
- **Submitted:** 2014-10-12
- **Reporter:** voodookobra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cryptographic Issues - Generic
- **CVEs:** None
- **Category:** uncategorised

## Summary
https://github.com/joola/joola/blob/develop/lib/dispatch/users.js#L514

Because tokens are compared with the `===` operator, this may be susceptible to timing attacks. More info: http://codahale.com/a-lesson-in-timing-attacks/

This is probably not the lowest hanging fruit for an attacker, but it's something you might want to fix. :)

Replacement utility: https://github.com/cryptocat/cryptoc

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

https://github.com/joola/joola/blob/develop/lib/dispatch/users.js#L514

Because tokens are compared with the `===` operator, this may be susceptible to timing attacks. More info: http://codahale.com/a-lesson-in-timing-attacks/

This is probably not the lowest hanging fruit for an attacker, but it's something you might want to fix. :)

Replacement utility: https://github.com/cryptocat/cryptocat/blob/32fd02f8d899e219a004281eb0ce364cb52dd62a/src/core/js/lib/otr.js#L145-L152

</details>

---
*Analysed by Claude on 2026-05-24*
