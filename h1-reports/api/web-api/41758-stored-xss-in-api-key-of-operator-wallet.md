# Stored XSS in api key of operator wallet

## Metadata
- **Source:** HackerOne
- **Report:** 41758 | https://hackerone.com/reports/41758
- **Submitted:** 2014-12-23
- **Reporter:** 4lemon
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
1. Make an operation wallet
2. Open wallet settings
3. Press "New key"
4. In source code remove "maxlength=30" of key's name input tag - no length check on server-side
5. Fill name input with "<a href="example.com">asdf</a>" (PoC)
6. Press "Generate Key" 
7. After that when open wallet settings we got XSS.
8. In case we can share this type of wallet this xss can be used against another user

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

1. Make an operation wallet
2. Open wallet settings
3. Press "New key"
4. In source code remove "maxlength=30" of key's name input tag - no length check on server-side
5. Fill name input with "<a href="example.com">asdf</a>" (PoC)
6. Press "Generate Key" 
7. After that when open wallet settings we got XSS.
8. In case we can share this type of wallet this xss can be used against another user.
Problem is that there is some filter on server side and at this moment i trying to find way to bypass it and fire javascript command.

</details>

---
*Analysed by Claude on 2026-05-24*
