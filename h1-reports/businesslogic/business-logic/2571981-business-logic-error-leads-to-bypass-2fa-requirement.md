# Business Logic error leads to bypass 2FA requirement 

## Metadata
- **Source:** HackerOne
- **Report:** 2571981 | https://hackerone.com/reports/2571981
- **Submitted:** 2024-06-24
- **Reporter:** abdulprkr
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Business Logic Errors
- **CVEs:** None
- **Category:** business-logic

## Summary
Hi team,

##Summary
I have identified a business logic issue in the 2FA requirement. I noticed that the organization enables the 2FA requirement so that only reporters who have set up 2FA can report, due to security reasons. This is because the report contains sensitive information, and if a hacker's credentials are compromised, the 2FA protection should be in place. This ensures that the vulnerab

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

Hi team,

##Summary
I have identified a business logic issue in the 2FA requirement. I noticed that the organization enables the 2FA requirement so that only reporters who have set up 2FA can report, due to security reasons. This is because the report contains sensitive information, and if a hacker's credentials are compromised, the 2FA protection should be in place. This ensures that the vulnerability reported by the hacker remains secure. However, if the hacker adds another hacker as a collaborator, the hackerone does not check whether the invited hacker has set up 2FA or not. The invited hacker can join the report without any 2FA requirement, which contains the same sensitive information that the organization has mandated 2FA to protect. Therefore, it is necessary to ensure that the invited hacker also has 2FA set up. Otherwise, they should not be able to accept the invitation until they set up 2FA. This would ensure that only those hackers who have set up 2FA can access the organization's report.

##Step to Reproduce:
Step 1: Create 2 account one with 2FA enable (A) & another without 2FA (B)
Step 2: Select Program which required 2FA & allow collabration 
Step 3: Create Report Using account (A) & add account (B) ass collaborator
Step 4: Submit Report 
Step 5: Observe that invitation sent Successfully
Step 6: Now accept Invitation & observe that now you can access the report without 2FA requirement

## Impact

>Sensitive Information Exposure: The primary objective of implementing 2FA is to secure sensitive information in reports. If a hacker without 2FA is invited as a collaborator, they can access this sensitive information without the additional security layer. This defeats the purpose of having 2FA, leaving sensitive data vulnerable to unauthorized access.

>Increased Risk of Data Breaches: If a hacker's credentials are compromised, the 2FA protection is supposed to mitigate this risk. Allowing a collaborator without 2FA exposes the organization to potential data breaches, as the compromised credentials can be used to gain access to reports containing critical vulnerabilities.

</details>

---
*Analysed by Claude on 2026-05-24*
