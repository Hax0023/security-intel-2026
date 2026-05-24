# The 'Create a New Account' action is vulnerable to CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 109810 | https://hackerone.com/reports/109810
- **Submitted:** 2016-01-10
- **Reporter:** roshanpty
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
The request to create an account wallet doesn't validate if the request is originating from the user itself with the help of an anti-CSRF token. 

Step 1: Craft an HTML page with request to create a wallet in your accounts page. 
https://www.coinbase.com/accounts > New Account > Wallet

Step 2: Open the HTML page in a tab of the browser where a user is already logged in to coinbase. It can be obse

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

The request to create an account wallet doesn't validate if the request is originating from the user itself with the help of an anti-CSRF token. 

Step 1: Craft an HTML page with request to create a wallet in your accounts page. 
https://www.coinbase.com/accounts > New Account > Wallet

Step 2: Open the HTML page in a tab of the browser where a user is already logged in to coinbase. It can be observed that a wallet is created.

PS: In some browsers this may not work. It should be noted that it is not because the application doesn't have a proper CSRF mitigation mechanism, rather the parameter utf8 is improperly rendered.

</details>

---
*Analysed by Claude on 2026-05-24*
