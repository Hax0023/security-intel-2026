# Campaign Account Balance and History Disclosed in API Response

## Metadata
- **Source:** HackerOne
- **Report:** 1587374 | https://hackerone.com/reports/1587374
- **Submitted:** 2022-05-31
- **Reporter:** sachin_kr
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
During the security assessment of the application, it has been observed that server-side authorization checks are not implemented on the 'GET /campaign-manager-api/campaignManagerAccounts/:campaignId/accountCredits?q=account' HTTP request. As a result, an attacker can fetch the campaign wallet amount details like 'totalCreditAmount', and 'remaining credit amount' history of all the victim's accoun

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

During the security assessment of the application, it has been observed that server-side authorization checks are not implemented on the 'GET /campaign-manager-api/campaignManagerAccounts/:campaignId/accountCredits?q=account' HTTP request. As a result, an attacker can fetch the campaign wallet amount details like 'totalCreditAmount', and 'remaining credit amount' history of all the victim's account.

###Steps to reproduce:
1. Log in to LinkedIn.
2. Create an advertising account. 
███
3. After creating the account go to - the https://www.linkedin.com/campaignmanager/accounts/XXXXX/billing/transactions page.
4. Intercept the vulnerable requests and replay the request using the victim's campaign id. The response will disclose the campaign wallet details and history.
███████

###Vulnerable Request:
```
GET /campaign-manager-api/campaignManagerAccounts/█████████████/accountCredits?q=account HTTP/2
Host: www.linkedin.com
```

###IDs for testing:
███████████████████
████████████
█████████████████
█████████████████
The ids are in series so can be brute forced

## Impact

An attacker can access the complete wallet details like available amount and used amounts and the deposit history of victim's campaign account.

</details>

---
*Analysed by Claude on 2026-05-24*
