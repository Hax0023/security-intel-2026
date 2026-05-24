# Missing CSRF Protection in  /stats EndPoint.

## Metadata
- **Source:** HackerOne
- **Report:** 415350 | https://hackerone.com/reports/415350
- **Submitted:** 2018-09-27
- **Reporter:** kaustubh
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
##EndPoint /affiliates/stats. doesnot verify the CSRF Tokens##


## Steps To Reproduce:

 1. Login with the your account 
 2. Navigate to the URL https://chaturbate.com/affiliates/stats.. 
 3. Check the stats in default its todays date or this week in select period.
4. Intercept the request and change the parameter to whatever you want to set.
5. generate the POC And open it in browser
6. You can 

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

##EndPoint /affiliates/stats. doesnot verify the CSRF Tokens##


## Steps To Reproduce:

 1. Login with the your account 
 2. Navigate to the URL https://chaturbate.com/affiliates/stats.. 
 3. Check the stats in default its todays date or this week in select period.
4. Intercept the request and change the parameter to whatever you want to set.
5. generate the POC And open it in browser
6. You can see the changes in the form.

## Supporting Material/References:
Please find attached for the CSRF POC and CSRF_1 for PreCSRF And CSRF_2 For Post CSRF.

## Impact

Attacker may change the parameters in stat or may force user to download the malicious .

</details>

---
*Analysed by Claude on 2026-05-24*
