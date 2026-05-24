# Stored XSS in Name of Team Member Invitation

## Metadata
- **Source:** HackerOne
- **Report:** 786301 | https://hackerone.com/reports/786301
- **Submitted:** 2020-01-30
- **Reporter:** abdulsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
hello team
i have found an stored in add team member
##Step to reproduce
1. Go to  https://localizestaging.com/organization/team?filter=all
2. click on add team member
3. On the name, enter payload:  </script><svg onload=alert(document.domain)>    
4. and in the email  add  your victim email
4. when he join the team the xss  will trigger.
{F701271}

now  victim , can't logout, he can't do anything

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

hello team
i have found an stored in add team member
##Step to reproduce
1. Go to  https://localizestaging.com/organization/team?filter=all
2. click on add team member
3. On the name, enter payload:  </script><svg onload=alert(document.domain)>    
4. and in the email  add  your victim email
4. when he join the team the xss  will trigger.
{F701271}

now  victim , can't logout, he can't do anything in his account

best regards
@moodiabdoul3

## Impact

the victim can nothing in his account

</details>

---
*Analysed by Claude on 2026-05-24*
