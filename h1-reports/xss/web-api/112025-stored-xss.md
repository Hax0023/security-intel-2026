# Stored XSS

## Metadata
- **Source:** HackerOne
- **Report:** 112025 | https://hackerone.com/reports/112025
- **Submitted:** 2016-01-21
- **Reporter:** manish121
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

Bug: Stored XSS
Payload: "><img src=x onerror=prompt(document.domain);>
Browser Used: Google Chrome
OS: Windows 7

Steps to Reproduce:

1) Log in to your account
2) Click on My Courses
3) Choose any enrolled courses
4) Click on Add Discussion
5) Click on Link -> Insert Link
6) In URL use above Payload
7) In Text write anything
8) Click on Insert 
9) Now click on that Text
10) Javascript wi

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

Hello,

Bug: Stored XSS
Payload: "><img src=x onerror=prompt(document.domain);>
Browser Used: Google Chrome
OS: Windows 7

Steps to Reproduce:

1) Log in to your account
2) Click on My Courses
3) Choose any enrolled courses
4) Click on Add Discussion
5) Click on Link -> Insert Link
6) In URL use above Payload
7) In Text write anything
8) Click on Insert 
9) Now click on that Text
10) Javascript will get executed.

Please check the link of PoC video..
https://www.dropbox.com/s/i2l5v7av597frj8/Udemy%20XSS.avi?dl=0

Thanks,
Manish Agrawal.

</details>

---
*Analysed by Claude on 2026-05-24*
