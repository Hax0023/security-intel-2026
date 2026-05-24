# MD5 used for Key-Auth signatures

## Metadata
- **Source:** HackerOne
- **Report:** 32944 | https://hackerone.com/reports/32944
- **Submitted:** 2014-10-27
- **Reporter:** voodookobra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cryptographic Issues - Generic
- **CVEs:** None
- **Category:** uncategorised

## Summary
https://github.com/WP-API/Key-Auth/blob/f9b74b3e4df667cfb44baba556eafde65fa3aec9/key-auth.php#L65

MD5 is vulnerable to length-extension attacks.

Maybe consider changing this to `hash_hmac('sha256', json_encode($args), $secret)`?

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

https://github.com/WP-API/Key-Auth/blob/f9b74b3e4df667cfb44baba556eafde65fa3aec9/key-auth.php#L65

MD5 is vulnerable to length-extension attacks.

Maybe consider changing this to `hash_hmac('sha256', json_encode($args), $secret)`?

</details>

---
*Analysed by Claude on 2026-05-24*
