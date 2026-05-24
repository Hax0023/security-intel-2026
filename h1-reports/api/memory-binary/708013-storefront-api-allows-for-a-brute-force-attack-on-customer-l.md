# StoreFront API allows for a brute force attack on customer login by not timing out ALL attempts

## Metadata
- **Source:** HackerOne
- **Report:** 708013 | https://hackerone.com/reports/708013
- **Submitted:** 2019-10-04
- **Reporter:** clew
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Restriction of Authentication Attempts
- **CVEs:** None
- **Category:** memory-binary

## Summary
It seems that the service used for login purposes could be brute forced. the system fails when the password is incorrect, after some unsuccessful attempts the following message is shown:

 
{"data":{"customerAccessTokenCreate":null},"errors":[{"message":"Login attempt limit exceeded. Please try again later.","locations":[{"line":1,"column":10}],"path":["customerAccessTokenCreate"]}]}

 
However, i

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

It seems that the service used for login purposes could be brute forced. the system fails when the password is incorrect, after some unsuccessful attempts the following message is shown:

 
{"data":{"customerAccessTokenCreate":null},"errors":[{"message":"Login attempt limit exceeded. Please try again later.","locations":[{"line":1,"column":10}],"path":["customerAccessTokenCreate"]}]}

 
However, it still possible to continue brute forcing and if you try with the real password it will work again. So in our case, we have been able to perform brute force attack.  

We feel Shopify should enforce the "limit exceeded" error for BOTH valid and invalid passwords.

## Impact

If the brute force attack succeeds, the attacker will then gain access to that user's shopify account, including contact information and order history.

</details>

---
*Analysed by Claude on 2026-05-24*
