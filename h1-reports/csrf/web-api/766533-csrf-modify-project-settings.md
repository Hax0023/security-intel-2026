# CSRF - Modify Project Settings

## Metadata
- **Source:** HackerOne
- **Report:** 766533 | https://hackerone.com/reports/766533
- **Submitted:** 2019-12-31
- **Reporter:** ahmd_halabi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
**Target Url/Endpoint**
https://my.stripo.email/cabinet/stripeapi/v1/projects/{Project_Id}

**Note**
Attacker just need to know victim project Id.

## Summary:
This CSRF Vulnerability leads to change user's project settings including General Information, Contacts, Social Networks and Other Options.

## Steps To Reproduce:
This POC is a simple example on exploiting this bug. Attacker can exploit it

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

**Target Url/Endpoint**
https://my.stripo.email/cabinet/stripeapi/v1/projects/{Project_Id}

**Note**
Attacker just need to know victim project Id.

## Summary:
This CSRF Vulnerability leads to change user's project settings including General Information, Contacts, Social Networks and Other Options.

## Steps To Reproduce:
This POC is a simple example on exploiting this bug. Attacker can exploit it with more advanced techniques and can really lead to critical issues.
1. Navigate to Project Settings -> Modify any data and intercept the request, send it to repeater, and do the following.
2. Take the HTML code format from burp suite -> Engagement Tools -> Generate CSRF POC.
3. Put the piece of code in an html file, then open it.
4. Now hit on the button and intercept its request.
5. Change POST to PATCH.
6. Copy the patch data from the old intercepted request from repeater and paste it to the current intercepted request and modify the data (email for example).
7. Modify the request header of Content-Type: `Content-Type: application/json;charset=UTF-8`
8. Forward the request and CSRF exploited successfully and the modified data changed successfully  :)

## Supporting Material/References:
Please See this video where I recorded the above PoC in details
██████

## Impact

This attack can be exploited in advanced way to modify all project settings and manipulate its data. Smart attacker can gain a big advantage from this bug. Hope you fix it asap.

**Regards**

</details>

---
*Analysed by Claude on 2026-05-24*
