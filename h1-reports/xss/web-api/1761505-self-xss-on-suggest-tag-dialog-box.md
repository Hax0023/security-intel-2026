# Self-XSS on Suggest Tag dialog box

## Metadata
- **Source:** HackerOne
- **Report:** 1761505 | https://hackerone.com/reports/1761505
- **Submitted:** 2022-11-03
- **Reporter:** j3rry4unt
- **Program:** Unknown
- **Bounty:** $50
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Stored cross-site scripting  arises when an application receives data from an untrusted source and includes that data within its later HTTP responses in an unsafe way.

vulnerable URL : https://www.xvideos.com/video57921571/friend_b._if_d.

Vulnerability Description : Application have a add tag functionality when i put java script like <script>alert(1)</script> after that stored XSS vu

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

## Summary:
Stored cross-site scripting  arises when an application receives data from an untrusted source and includes that data within its later HTTP responses in an unsafe way.

vulnerable URL : https://www.xvideos.com/video57921571/friend_b._if_d.

Vulnerability Description : Application have a add tag functionality when i put java script like <script>alert(1)</script> after that stored XSS vulnerability arise.

Step to Reproduce : 
Step 1 : Go to following URL https://www.xvideos.com/video53284603/b.
Note : you don't need an account to do this
Step 2 : There is a add tag functionality insert the following information : <script>alert(1)</script>
Step 3 : Click the add button 
Step 4 : you will see a java script popup box showing your domain

Check the attached Video POC to see the actual XSS vulnerability

## Impact

If an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user.
When the victim accesses the page containing the JavaScript payload, their browser will make a HTTP request to the attacker’s server

</details>

---
*Analysed by Claude on 2026-05-24*
