# Sensei LMS IDOR to send message

## Metadata
- **Source:** HackerOne
- **Report:** 1592596 | https://hackerone.com/reports/1592596
- **Submitted:** 2022-06-06
- **Reporter:** ghimire_veshraj
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there, hope you are doing great.
So, there is an option to send message to teacher privately by student on Sensei LMS.
Each message sent by student will have different ID,
Student1 cannot access or send message to the message from Student2 (which is meant to be private with teacher)
Similarly Student2 cannot view/send message sent by student1 to the teacher.

But due to lack of access control, 

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

Hi there, hope you are doing great.
So, there is an option to send message to teacher privately by student on Sensei LMS.
Each message sent by student will have different ID,
Student1 cannot access or send message to the message from Student2 (which is meant to be private with teacher)
Similarly Student2 cannot view/send message sent by student1 to the teacher.

But due to lack of access control, it is possible for any student to reply on any thread of Student to teacher just by simply changing ID of the thread which is numeric.

This may sound a bit complex but i will try to explain this with video POC, please let me know if you still didn't understood the vulnerability here:
{F1759226}

## Impact

Any student can reply to other student's thread which is meant to be private between the original student [who sent message] and teacher.

</details>

---
*Analysed by Claude on 2026-05-24*
