# Email Verification Bypass via Race Condition

## Metadata
- **Source:** HackerOne
- **Report:** 3020733 | https://hackerone.com/reports/3020733
- **Submitted:** 2025-03-02
- **Reporter:** sijojohnson
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An email verification bypass vulnerability was discovered in the my.malwarebytes.com.

##Steps to Reproduce

- Create an account using an attacker email: sijojohnson+attacker@wearehackerone.com.
- Verify the account.
- Go to account settings and update the email address to sijojohnson+attacker2@wearehackerone.com.
- Capture the request using a tool like Burp Suite.
- Send the request to Repeater t

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

An email verification bypass vulnerability was discovered in the my.malwarebytes.com.

##Steps to Reproduce

- Create an account using an attacker email: sijojohnson+attacker@wearehackerone.com.
- Verify the account.
- Go to account settings and update the email address to sijojohnson+attacker2@wearehackerone.com.
- Capture the request using a tool like Burp Suite.
- Send the request to Repeater twice and  forward the request.
- In Repeater, modify Request 1 by changing the email to the victim's email (e.g., sijojohnson+victim@wearehackerone.com).
- In Request 2, use the attacker's email (sijojohnson+attacker2@wearehackerone.com).
- Group both requests, select Send Group in Parallel, and send the requests.
- Observe the email inbox—both the victim's and attacker's email addresses will receive the same OTP.
- Go to confirmation page displayed,  Enter the  OTP (both OTP's are same),
- Capture the request, and replace the email with the victim’s email.
- Send the modified request and observe the response.
- The victim’s email address is now successfully verified.

##PoC

{F4105917}

## Impact

- This vulnerability allows an attacker to take control of an account associated with a victim's email by changing the registered email address.
- It presents a risk of data theft, unauthorized transactions, and further exploitation of linked accounts.
- Users' personal and sensitive data may be compromised.

</details>

---
*Analysed by Claude on 2026-05-24*
