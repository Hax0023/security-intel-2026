# Race condition on https://judge.me/people

## Metadata
- **Source:** HackerOne
- **Report:** 1566017 | https://hackerone.com/reports/1566017
- **Submitted:** 2022-05-11
- **Reporter:** netboom
- **Program:** Unknown
- **Bounty:** $250
- **Severity:** low
- **Vuln:** Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')
- **CVEs:** None
- **Category:** memory-binary

## Summary
##summary:An attacker can increase the followers of  the users of judge.me

Tools required : 
1.burpsuit
2.turbo intruder

##steps to reproduce:
1.visit https://judge.me/people
2.like a user and intercept the request
3.now  send it to turbo intruder and configure the script to 
     race.py

## Impact

The attacker can increase their followers in a bad way by creating fake followers

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

##summary:An attacker can increase the followers of  the users of judge.me

Tools required : 
1.burpsuit
2.turbo intruder

##steps to reproduce:
1.visit https://judge.me/people
2.like a user and intercept the request
3.now  send it to turbo intruder and configure the script to 
     race.py

## Impact

The attacker can increase their followers in a bad way by creating fake followers

</details>

---
*Analysed by Claude on 2026-05-24*
