# Race Condition in Flag Submission

## Metadata
- **Source:** HackerOne
- **Report:** 454949 | https://hackerone.com/reports/454949
- **Submitted:** 2018-12-04
- **Reporter:** dropper
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')
- **CVEs:** None
- **Category:** memory-binary

## Summary
**Summary:**

This report describes a Race Condition Vulnerability which allow an authenticated user to submit the same Flag multiple times. Increasing the user points and therefore the chances to get an invitation to a private program.

### Steps To Reproduce
To  reproduce this bug, you need to:
1. Login with a valid user account
2. Solve one of the challenges and get a Flag. It can be the Trivia

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

**Summary:**

This report describes a Race Condition Vulnerability which allow an authenticated user to submit the same Flag multiple times. Increasing the user points and therefore the chances to get an invitation to a private program.

### Steps To Reproduce
To  reproduce this bug, you need to:
1. Login with a valid user account
2. Solve one of the challenges and get a Flag. It can be the Trivial one (worth 1 point).
3. Go to the submit page, put the Flag that was found and intercept the POST request that is sent during the Flag submission. You can use Burp Suite for that, for example.
4. Then, you just have to submit the POST several times in a short time frame. I recommend a script with multi threads or "Race The Web" tool that I will mention below.
5. Enjoy your extra points with the same flag.

### Tool Used During PoC
To the PoC I used "Race The Web", available at: https://github.com/insp3ctre/race-the-web
With this tool we can send the requests faster than we could with Burp Intruder. Getting better results. 

### Supporting Material/References (Screenshots)
The outcome is shown below:
 {F385429}
I've used the Trivial Flag 70 times and earned 2 invitations.

### Note
I've created a new user to do this PoC. In case you want to delete, the e-mail is: ███████

## Impact

An attacker could use this Race Condition vulnerability to earn extra points and increase the chances to get invited to a private program without the need to solve other chalanges available.

</details>

---
*Analysed by Claude on 2026-05-24*
