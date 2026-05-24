# Incorrect Functionality of Password reset links

## Metadata
- **Source:** HackerOne
- **Report:** 280529 | https://hackerone.com/reports/280529
- **Submitted:** 2017-10-19
- **Reporter:** saikiran-10099
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
Vulnerability:-
->Password reset links should work in such a way that "only the last generated password reset link should be valid" i.e; if two tokens are generated at a time, then 2nd token must work and 1st token must be invalid.
->If not, another case is that "if some number of reset links are generated at a time, if any one link is used in that links, then all remaining links should get invali

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

Vulnerability:-
->Password reset links should work in such a way that "only the last generated password reset link should be valid" i.e; if two tokens are generated at a time, then 2nd token must work and 1st token must be invalid.
->If not, another case is that "if some number of reset links are generated at a time, if any one link is used in that links, then all remaining links should get invalid".

This is the standard practice followed and implemented by all secured websites that are running bug bounty programs on hackerone.

Any issues, please let me know...

Thank you 

</details>

---
*Analysed by Claude on 2026-05-24*
