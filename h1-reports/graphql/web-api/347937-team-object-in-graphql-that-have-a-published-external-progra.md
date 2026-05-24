# Team object in GraphQL that have a published external program may expose existence of a private program

## Metadata
- **Source:** HackerOne
- **Report:** 347937 | https://hackerone.com/reports/347937
- **Submitted:** 2018-05-06
- **Reporter:** nismo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**

Hi Team!

On Team object the parameter "i_cannot_create_jira_webhook_reasons" is not NULL and gets the following default states when called for all programs ["CANNOT_VIEW","FEATURE_GATED","PROGRAM_PERMISSION_REQUIRED"]

If a Company Program runs a Private Program or a Public On the "FEATURE_GATED" is missing (Since the feature is not gated anymore) and therefore an attacker can find 

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

Hi Team!

On Team object the parameter "i_cannot_create_jira_webhook_reasons" is not NULL and gets the following default states when called for all programs ["CANNOT_VIEW","FEATURE_GATED","PROGRAM_PERMISSION_REQUIRED"]

If a Company Program runs a Private Program or a Public On the "FEATURE_GATED" is missing (Since the feature is not gated anymore) and therefore an attacker can find if a Company is running a private program

##POC

* Company ██████ (not runnig private gives "i_cannot_create_jira_webhook_reasons":["CANNOT_VIEW","FEATURE_GATED","PROGRAM_PERMISSION_REQUIRED"]

* Company █████████ (running private) gives "i_cannot_create_jira_webhook_reasons":["CANNOT_VIEW","PROGRAM_PERMISSION_REQUIRED"]

* Even Company HackerOne  (running public) gives "i_cannot_create_jira_webhook_reasons":["CANNOT_VIEW","PROGRAM_PERMISSION_REQUIRED"]

All private programs and public has an overriden  "FEATURE_GATED" so you get the idea

#Solutiion

NULL the value maybe

PS: Thanks to @jobert who encouraged me to search deeper after the #347383 duplicate!

Thanks
**nismo**

## Impact

Knowing companies that run private programs on Hackerone

</details>

---
*Analysed by Claude on 2026-05-24*
