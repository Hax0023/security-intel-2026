# The contribution save option seem to be vulnerable to CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 151827 | https://hackerone.com/reports/151827
- **Submitted:** 2016-07-16
- **Reporter:** roshanpty
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
The application is vulnerable to Cross Site Request Forgery
====================

Description
---------------------
The option in the application to save weekly contribution for a project is vulnerable to Cross Site Request forgery. 
**Note:** I am unable to perform the action itself normally. But it is obvious that the application uses no protection against CSRF and the token named **csrf_token**

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

The application is vulnerable to Cross Site Request Forgery
====================

Description
---------------------
The option in the application to save weekly contribution for a project is vulnerable to Cross Site Request forgery. 
**Note:** I am unable to perform the action itself normally. But it is obvious that the application uses no protection against CSRF and the token named **csrf_token** is being passed in the cookie instead of a post parameter or HTTP header. 

Detailed Steps:
---------------------
**Step 1:** Open a project and modify the weekly contribution for the same. 
{F105367}
**Step 2:** Send the request to save the modified value.
{F105368}
**Step 3:** It can be observed that no kind of CSRF protection is employed and the request can be recreated in the following URL format. If anyone clicks on the link in a browser where they are already logged in to gratipay, the amount will be automatically updated.
https://gratipay.com/<project>/payment-instruction.json?amount=<amount>

</details>

---
*Analysed by Claude on 2026-05-24*
