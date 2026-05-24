# Weak Random Number Generator for Auth Tokens

## Metadata
- **Source:** HackerOne
- **Report:** 31166 | https://hackerone.com/reports/31166
- **Submitted:** 2014-10-12
- **Reporter:** voodookobra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cryptographic Issues - Generic
- **CVEs:** None
- **Category:** uncategorised

## Summary
https://github.com/joola/joola/blob/a534c3dca1a0deaec99c192978e61a35dd3a9069/lib/common/index.js#L90-L98

`Math.random()` is not sufficient for cryptographic purposes (such as authentication tokens).

An example replacement that uses `window.crypto.getRandomValues()` is available here:

https://github.com/resonantcore/lib/blob/9362480647b304aee6819ea94a18409241e79378/js/diceware/diceware.js#

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

https://github.com/joola/joola/blob/a534c3dca1a0deaec99c192978e61a35dd3a9069/lib/common/index.js#L90-L98

`Math.random()` is not sufficient for cryptographic purposes (such as authentication tokens).

An example replacement that uses `window.crypto.getRandomValues()` is available here:

https://github.com/resonantcore/lib/blob/9362480647b304aee6819ea94a18409241e79378/js/diceware/diceware.js#L60-L94

Further information:
https://media.blackhat.com/us-13/US-13-Soeder-Black-Box-Assessment-of-Pseudorandom-Algorithms-WP.pdf

</details>

---
*Analysed by Claude on 2026-05-24*
