# Insecure Direct Object Reference - access to other user/group DM's

## Metadata
- **Source:** HackerOne
- **Report:** 53858 | https://hackerone.com/reports/53858
- **Submitted:** 2015-03-29
- **Reporter:** akhil-reni
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
**Hello**,

I found a way to access group DM's which i don't have access to,
Conditions to be met:
- Should have been in that DM group atleast once.

Exploitation ways:
===============
- let's say they're three twitter profiles, Naruto , Goku and Eren.
- Naruto creates a DM group in between himself , Goku and Eren.
- Now Eren leaves the DM group, at this moment Goku and Naruto think that

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

I found a way to access group DM's which i don't have access to,
Conditions to be met:
- Should have been in that DM group atleast once.

Exploitation ways:
===============
- let's say they're three twitter profiles, Naruto , Goku and Eren.
- Naruto creates a DM group in between himself , Goku and Eren.
- Now Eren leaves the DM group, at this moment Goku and Naruto think that their DM's are private and Eren won't be able to see the DM's cause he just the left group.
- But Eren can still access the DM's by just navigating himself to 
`https://mobile.twitter.com/a/messages/582225197727506432/delete`

  where **582225197727506432** is the DM id.

Steps to Reproduce:
=================
- Create three profiles A,B and C
- From account A create a DM group for A, B and C
- Leave the DM group from account C 
- Now message something in the DM group from account A or account B.
- A unique DM id will be created for that message.
- Note down the DM ID and 
 From Account C navigate yourself to 
`https://mobile.twitter.com/a/messages/[DM ID]/delete`
Replace the [DM ID] with your noted DM ID in the above steps.

POC: http://i.imgur.com/j08a01n.png


**Regards
Wesecureapp**

</details>

---
*Analysed by Claude on 2026-05-24*
