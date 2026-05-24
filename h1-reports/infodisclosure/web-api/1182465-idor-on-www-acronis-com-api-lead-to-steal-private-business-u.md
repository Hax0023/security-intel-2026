# IDOR on www.acronis.com API lead to steal private business user information

## Metadata
- **Source:** HackerOne
- **Report:** 1182465 | https://hackerone.com/reports/1182465
- **Submitted:** 2021-05-02
- **Reporter:** f_m
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary
Hi acronis team, i found an endpoint : `www.acronis.com/en-us/api/v1/lead/id:929-HVV-335&token:_mch-acronis.com-<integer value>` that is vulnerable to IDOR. with this vulnerability an attacker can steal private info such as company name, user name and surname, telephone number etc...

## Steps To Reproduce

  1. once logged in into account.acronis.com go to :  https://www.acronis.com/en

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

## Summary
Hi acronis team, i found an endpoint : `www.acronis.com/en-us/api/v1/lead/id:929-HVV-335&token:_mch-acronis.com-<integer value>` that is vulnerable to IDOR. with this vulnerability an attacker can steal private info such as company name, user name and surname, telephone number etc...

## Steps To Reproduce

  1. once logged in into account.acronis.com go to :  https://www.acronis.com/en-us/api/v1/lead/id:929-HVV-335&token:_mch-acronis.com-1614775941608-39235
  2. you will see all my private account information
  
███

NOTE: the only part that change from account to account is the last part of the token(the last 5 digits) and since it's an integer is totally guessable.

## Recommendations

implement a check on the endpoint or use a random token value instead of an integer

## Impact

an attacker can steal private info from other users profile

</details>

---
*Analysed by Claude on 2026-05-24*
