# Insecure direct object reference - have access to deleted DM's

## Metadata
- **Source:** HackerOne
- **Report:** 52646 | https://hackerone.com/reports/52646
- **Submitted:** 2015-03-19
- **Reporter:** akhil-reni
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
**Hello**,

The bug is straight and simple, 
I have access to deleted DM's.
Once a DM is deleted a user/app will still be able to access the DM's using show DM endpoint

Attack Scenario
====================
Their are two accounts Sam and Molly ,
Sam Dm's Molly something important and both quickly delete the Dm's after the chat,
Sam has given access to a 3rd party app which can access his

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

**Hello**,

The bug is straight and simple, 
I have access to deleted DM's.
Once a DM is deleted a user/app will still be able to access the DM's using show DM endpoint

Attack Scenario
====================
Their are two accounts Sam and Molly ,
Sam Dm's Molly something important and both quickly delete the Dm's after the chat,
Sam has given access to a 3rd party app which can access his DM's.
When Sam DM's molly every DM gets a unique id like 123456
and the DM can be accessed using the following API call ,
https://api.twitter.com/1.1/direct_messages/show.json?id={DM-id}
Now let's say Sam and Molly both deleted the DM ,
but the 3rd party app can still access the deleted DM using the above end point.

Steps to reproduce
==========================
- Create 2 account's A and B
- From account A Dm account B
- Note down the Dm id , and make an api 
https://api.twitter.com/1.1/direct_messages/show.json?id=[noted-dm-id]
- Now delete the DM
- Repeat the api call 
https://api.twitter.com/1.1/direct_messages/show.json?id=578631102144741376
- You will still have access to the deleted DM.

*POC: Check for video attached*



**Regards,
Wesecureapp**



</details>

---
*Analysed by Claude on 2026-05-24*
