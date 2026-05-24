# Invalid Phabricator API token revealed through error message when escalating a report

## Metadata
- **Source:** HackerOne
- **Report:** 335123 | https://hackerone.com/reports/335123
- **Submitted:** 2018-04-09
- **Reporter:** bigbug
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** none
- **Vuln:** Information Exposure Through an Error Message
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Summary**

While trying to create a phabricator task by escalating to phabricator, error message contains the API token as a part of the pop up. This is seen when a user tries to enter an invalid API token.

**Description**

It was seen that after setting up phabricator integration in a program, when trying to escalate a report to phabricator, if the API token entered was invalid in terms of len

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

**Summary**

While trying to create a phabricator task by escalating to phabricator, error message contains the API token as a part of the pop up. This is seen when a user tries to enter an invalid API token.

**Description**

It was seen that after setting up phabricator integration in a program, when trying to escalate a report to phabricator, if the API token entered was invalid in terms of length/authenticity, the error message contains the entered API token. 

This was seen when trying to escalate a report using a phabricator instance and previously used API token. 

**Steps to reproduce**

1. Visit https://hackerone.com/*program name*/phabricator_integration
1. Enter an instance URL
1. Enter the API token incorrectly.
1. Now navigate to any report you want to escalate.
1. Click on Edit References.
1. Click on "Create phabricator task"
1. Error message will appear with API token.

+ Invalid token error

{F283480}


+ Invalid length error

{F283481}

Above image contains an API token that was entered incorrectly in terms of length. 

Both of the above errors contain the API token that was entered incorrectly.

**Fix**

1. One thing to mention is that the integration page does not validate the API token lengths while entering. API token lengths should be checked on integration setting page itself.
1. Validity of API token should also be checked while saving integration settings itself.

## Impact

1. API tokens are not normally displayed anywhere else after setting up the integration. Team members with limited permissions who normally have no access to such information can see the API tokens.
1. Mistyped API token like the one below could easily reveal actual API tokens. The mistyped API tokens could be part of actual API tokens. 

{F283481}

</details>

---
*Analysed by Claude on 2026-05-24*
