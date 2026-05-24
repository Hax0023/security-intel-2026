# idor on upload profile functionality 

## Metadata
- **Source:** HackerOne
- **Report:** 741683 | https://hackerone.com/reports/741683
- **Submitted:** 2019-11-20
- **Reporter:** risinghunter
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Vulnerable URL: https://██████████/███████ID/#Common/EditOne/Person/{account_id}
steps to reproduce:
1).browse the image and click on the upload button
2).capture this request in burp suite 
3). change the value 'personId' parameter to account2 account_id 
(please see screenshot1)
4).then goes to account2, then you will see the uploaded image is successfully goes to the approved tab 

please see v

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

Vulnerable URL: https://██████████/███████ID/#Common/EditOne/Person/{account_id}
steps to reproduce:
1).browse the image and click on the upload button
2).capture this request in burp suite 
3). change the value 'personId' parameter to account2 account_id 
(please see screenshot1)
4).then goes to account2, then you will see the uploaded image is successfully goes to the approved tab 

please see video attach below you will understand completely

## Impact

an attacker is able to change profile image of any user

</details>

---
*Analysed by Claude on 2026-05-24*
