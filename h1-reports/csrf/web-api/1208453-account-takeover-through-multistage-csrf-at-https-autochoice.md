# Account takeover through multistage CSRF at https://autochoice.fas.gsa.gov/AutoChoice/changeQAOktaAnswer and ../AutoChoice/changePwOktaAnswer

## Metadata
- **Source:** HackerOne
- **Report:** 1208453 | https://hackerone.com/reports/1208453
- **Submitted:** 2021-05-25
- **Reporter:** rptl
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

Account takeover is possible through CSRF vulnerability at 'Change Security Question/Answer'  & ' Change Password'.
The endpoints - https://autochoice.fas.gsa.gov/AutoChoice/changeQAOktaAnswer & https://autochoice.fas.gsa.gov/AutoChoice/changePwOktaAnswer both are vulnerable to CSRF attack .==The CSRF token/or its presence is not validated at server side.==

Since, the password update functio

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

Hi,

Account takeover is possible through CSRF vulnerability at 'Change Security Question/Answer'  & ' Change Password'.
The endpoints - https://autochoice.fas.gsa.gov/AutoChoice/changeQAOktaAnswer & https://autochoice.fas.gsa.gov/AutoChoice/changePwOktaAnswer both are vulnerable to CSRF attack .==The CSRF token/or its presence is not validated at server side.==

Since, the password update functionality requires 'Secret Answer' Value & 'New Password'. Therefore, in multistage CSRF Secret Answer was updated first & then using that new secret answer, new password was set for the account using second stage.

Both CSRF request are performed through the same html POC. Upon execution of POC html, changes will  be reflected after few seconds as timeout is set for the first request to complete.  Also, there is no need to know the security question either, which itself is updated in the first stage.

POC Video - {F1314428}

CSRF Html file -  {F1314439}

@Triage Team - Since, this report involves two CSRFs for different functionalities, should I have filed two different  reports ?  as I would be losing rep. points.

## Impact

Account takeover through CSRF

</details>

---
*Analysed by Claude on 2026-05-24*
