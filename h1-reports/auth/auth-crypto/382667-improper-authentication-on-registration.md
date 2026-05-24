# Improper authentication on registration

## Metadata
- **Source:** HackerOne
- **Report:** 382667 | https://hackerone.com/reports/382667
- **Submitted:** 2018-07-17
- **Reporter:** lezibintlgent
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
> Hope you are doing well, one can register himself to semrush with any email ID. It means that there is no authentication mechanism if that email id is valid/invalid. Therefore a person with email ID that does not exist can also register and login to your platform.

**Summary:** 
[one can register himself to semrush with any email ID. It means that there is no authentication mechanism if that ema

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

> Hope you are doing well, one can register himself to semrush with any email ID. It means that there is no authentication mechanism if that email id is valid/invalid. Therefore a person with email ID that does not exist can also register and login to your platform.

**Summary:** 
[one can register himself to semrush with any email ID. It means that there is no authentication mechanism if that email id is valid/invalid. Therefore a person with email ID that does not exist can also register and login to your platform.
]

**Description:** 
[Hope you are doing well, one can register himself to semrush with any email ID. It means that there is no authentication mechanism if that email id is valid/invalid. Therefore a person with email ID that does not exist can also register and login to your platform.
]

## Browsers Verified In:

  * [Google chrome]
  * [Mozilla]

## Steps To Reproduce:

[reproduce steps]
  1. [Register the email ID that does not exist]
  2. [Click register button and then login to the account]
  3. [Signout and again sign in using previous email ID]

## Supporting Material/References:
[**Obligated field**]
  * Screenshots
)

## Impact

Attacker can take benefit by using this weak access control and further login with the fake account that doesnot exit.

</details>

---
*Analysed by Claude on 2026-05-24*
