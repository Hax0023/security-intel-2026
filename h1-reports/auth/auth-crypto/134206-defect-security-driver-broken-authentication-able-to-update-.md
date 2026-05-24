# Defect-Security | Driver-Broken Authentication | Able to update the Subscription Setting anonymously

## Metadata
- **Source:** HackerOne
- **Report:** 134206 | https://hackerone.com/reports/134206
- **Submitted:** 2016-04-24
- **Reporter:** sadhu16
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Steps to execute the issue/defect

1:Logged into account on domain (https://riders.uber.com) with one of the accounts (account type-Driver)

2:Now go to Manage your email subscription settings and note the link mentioned below


-View the subscription setting (i.e. subscription setting Uber Global Updates -checked)

-note the url -https://subscriptions.uber.com/user/483c39a2-9e7a-43fb-91a4-980370a

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

Steps to execute the issue/defect

1:Logged into account on domain (https://riders.uber.com) with one of the accounts (account type-Driver)

2:Now go to Manage your email subscription settings and note the link mentioned below


-View the subscription setting (i.e. subscription setting Uber Global Updates -checked)

-note the url -https://subscriptions.uber.com/user/483c39a2-9e7a-43fb-91a4-980370aa45c3/e911dd42abea2617e625d2547de8038a3e9a42b47097ad570d4b68b1ce25dba9?_ga=1.134668273.1418643578.1461496136

3:Now go to another browser where no authentication is done, now open the same url in Google Chrome

4:After link got opened, now going to modify the subscription setting -(i.e. subscription setting Uber Global Updates -Unchecked)


5:Now Again go to Browser Firefox and refresh the same url as a result of previous step subscription setting got updated

i.e. Uber Global Updates  gets  -Unchecked  from checked


I am successfully able to update the Subscription Setting of an authenticated user anonymously




</details>

---
*Analysed by Claude on 2026-05-24*
