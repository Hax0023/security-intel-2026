# Idor on the DELETE /comments/

## Metadata
- **Source:** HackerOne
- **Report:** 861849 | https://hackerone.com/reports/861849
- **Submitted:** 2020-04-28
- **Reporter:** tandav
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
[Idor on /comments]

## Steps To Reproduce:
[Make sure you have 2 different ID's to maintain 2 different session for ensurity]

  1. The request can be tamper with the ID of different (comment) both the functions of edit/delete can be used
  2. Delete gets hampered with the Captcha which is thrown but the Comment of different user can be observed in the request
  3. Assume user 1"victi

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
[Idor on /comments]

## Steps To Reproduce:
[Make sure you have 2 different ID's to maintain 2 different session for ensurity]

  1. The request can be tamper with the ID of different (comment) both the functions of edit/delete can be used
  2. Delete gets hampered with the Captcha which is thrown but the Comment of different user can be observed in the request
  3. Assume user 1"victim" made a comment "comment X" user 2 can edit the request for editing his comment "Y" to "X" further as the attacker failed editing the comment of victim, further disabling the edit option for user 1 :| that will make user 1"victim" left with only option to delete the comment. sed very sed
  4. Even this works widely with Burp_Intruder that means it doesn't even have rate limit.

## Impact

An attacker with a privilege to the user can harness the activities of any user around intentionally or target them widely.

</details>

---
*Analysed by Claude on 2026-05-24*
