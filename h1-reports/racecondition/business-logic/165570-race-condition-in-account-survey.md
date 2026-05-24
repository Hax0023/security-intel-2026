# Race Condition in account survey

## Metadata
- **Source:** HackerOne
- **Report:** 165570 | https://hackerone.com/reports/165570
- **Submitted:** 2016-09-03
- **Reporter:** cablej
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** business-logic

## Summary
There exists a race condition in the beginning survey, allowing a user to get $100 in credit multiple times. In my example, I made 2 asynchronous requests, and was credited with $200.

POC:

1. Create a new slack team.
2. Set your password, and find the account creation survey.
3. Complete the survey, and intercept the request using a proxy such as BurpSuite.
4. Repeat the request asynchronously, 

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

There exists a race condition in the beginning survey, allowing a user to get $100 in credit multiple times. In my example, I made 2 asynchronous requests, and was credited with $200.

POC:

1. Create a new slack team.
2. Set your password, and find the account creation survey.
3. Complete the survey, and intercept the request using a proxy such as BurpSuite.
4. Repeat the request asynchronously, such as in the command line by executing `(command) & (command)`.
5. The survey will be credited to your account multiple times. See the attached screenshot.

Please let me know if you need any more information.

</details>

---
*Analysed by Claude on 2026-05-24*
