# Cryptographic Side Channel in OAuth Library

## Metadata
- **Source:** HackerOne
- **Report:** 31168 | https://hackerone.com/reports/31168
- **Submitted:** 2014-10-12
- **Reporter:** voodookobra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cryptographic Issues - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Because hashes and tokens are compared with the `!==` and `===` operators, these checks may be susceptible to timing attacks. More info: http://codahale.com/a-lesson-in-timing-attacks/

Affected code:

https://github.com/WP-API/OAuth1/blob/45197eca2925f5022192903d3639decd0ae1811c/lib/class-wp-json-authentication-oauth1.php#L562
https://github.com/WP-API/OAuth1/blob/45197eca2925f5022192903d363

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

Because hashes and tokens are compared with the `!==` and `===` operators, these checks may be susceptible to timing attacks. More info: http://codahale.com/a-lesson-in-timing-attacks/

Affected code:

https://github.com/WP-API/OAuth1/blob/45197eca2925f5022192903d3639decd0ae1811c/lib/class-wp-json-authentication-oauth1.php#L562
https://github.com/WP-API/OAuth1/blob/45197eca2925f5022192903d3639decd0ae1811c/lib/class-wp-json-authentication-oauth1.php#L290

</details>

---
*Analysed by Claude on 2026-05-24*
