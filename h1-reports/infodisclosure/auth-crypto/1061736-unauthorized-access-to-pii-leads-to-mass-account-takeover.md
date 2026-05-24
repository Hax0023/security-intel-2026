# Unauthorized access to PII leads to MASS account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 1061736 | https://hackerone.com/reports/1061736
- **Submitted:** 2020-12-18
- **Reporter:** takester
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Business Logic Errors
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi, I hope you doing well
I found a critical endpoint which disclosed the personal information which can use to takeover any account present on https://██████████
#Steps:
1. Visit the link https://www.████████/███████    you will get my details,  including first name and last name, mobile number and email_address related to the account.
2. Go to the forgot password link present at https://www.████

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

Hi, I hope you doing well
I found a critical endpoint which disclosed the personal information which can use to takeover any account present on https://██████████
#Steps:
1. Visit the link https://www.████████/███████    you will get my details,  including first name and last name, mobile number and email_address related to the account.
2. Go to the forgot password link present at https://www.███████/ click on it.
3. Enter the mail address later you will be taken to another page which will ask you to enter mail address and pin
4. After entering mail address enter the pin as "████" as █████████ is at the endpoint.
5. It will validate and will ask you to change the password of that account.

###Note:  To get email list and pin list just decrease the number at the endpoint 
for example https://www.████████/███will give you another mail_address and pin will be ██████████

## Impact

An attacker can able to takeover any account that is present on that side.

</details>

---
*Analysed by Claude on 2026-05-24*
