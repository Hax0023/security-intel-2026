# Sensitive Information Disclosure https://cards-dev.twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 268888 | https://hackerone.com/reports/268888
- **Submitted:** 2017-09-16
- **Reporter:** hassham
- **Program:** Unknown
- **Bounty:** $280
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Dear Twitter Team, 

While researching through one of your domain cards-dev.twitter.com i discovered that the host is disclosing sensitive information when a user browses to a specific directory  
https://cards-dev.twitter.com:443/keys/.

The application downloads a file json.json which discloses the following information
`"customer_key":"████"` 
`"customer_secret":"█████████"`
`"jira_password":"█

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

Dear Twitter Team, 

While researching through one of your domain cards-dev.twitter.com i discovered that the host is disclosing sensitive information when a user browses to a specific directory  
https://cards-dev.twitter.com:443/keys/.

The application downloads a file json.json which discloses the following information
`"customer_key":"████"` 
`"customer_secret":"█████████"`
`"jira_password":"██████"`

I am checking that can this information be used to further escalate any vulnerability. 

Regards, 


</details>

---
*Analysed by Claude on 2026-05-24*
