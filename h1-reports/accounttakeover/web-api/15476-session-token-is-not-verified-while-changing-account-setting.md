# Session Token is not Verified while changing Account Setting's which Result In account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 15476 | https://hackerone.com/reports/15476
- **Submitted:** 2014-06-07
- **Reporter:** b7882330c6060c6b277c5a1
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Dear Team,

Step-by-step instructions on how to reproduce the problem:

It was found the application is vulnerable to CSRF attack.
To achieve the same,

Session Token is not Verified while changing Account Setting's which Result In account Takeover

Description:-

I have found that while changing Setting Session token is not verified .So an attacker can basically plot a CSRF attack whic

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

Dear Team,

Step-by-step instructions on how to reproduce the problem:

It was found the application is vulnerable to CSRF attack.
To achieve the same,

Session Token is not Verified while changing Account Setting's which Result In account Takeover

Description:-

I have found that while changing Setting Session token is not verified .So an attacker can basically plot a CSRF attack which would change the default email of the user and this would led to account takeover.

POC:-

I have made proof of concept video of the same:-https://www.youtube.com/watch?v=oCpAu18ULQQ
The Above Video is Unlisted.

Regard :-
Shubham Gupta

</details>

---
*Analysed by Claude on 2026-05-24*
