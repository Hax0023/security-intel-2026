# CSRF in function "Set as primary" on  accounts page

## Metadata
- **Source:** HackerOne
- **Report:** 10829 | https://hackerone.com/reports/10829
- **Submitted:** 2014-05-03
- **Reporter:** b76fad49b0533cc7149d9a4
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
I would like to report this CSRF vulnerability in coinbase on function "set as primary" for a account in accounts page. 

Steps:
1) Login to your coinbase account (which atleast has two accounts)
2) Go to "accounts" page and out of the two accounts click "set as primary" link for one of the accounts which is not primary.
3) Capturing the request in proxy, you will find that there are no anti 

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

I would like to report this CSRF vulnerability in coinbase on function "set as primary" for a account in accounts page. 

Steps:
1) Login to your coinbase account (which atleast has two accounts)
2) Go to "accounts" page and out of the two accounts click "set as primary" link for one of the accounts which is not primary.
3) Capturing the request in proxy, you will find that there are no anti CSRF token used for this function. 

Issue: Attacker simply send a link of a page to the victim with a iframe running something like this "https://coinbase.com/accounts/535e52d301c95bda2100005b/set_as_primary". When the victim will click the link of coinbase will get executed in the back without victims consent. 

NOTE: In the POC video attached, i have tried to show that for the delete account function there is an "authenticity token" sent but for set as primary function there is no token used, which might cause a CSRF on this. 

</details>

---
*Analysed by Claude on 2026-05-24*
