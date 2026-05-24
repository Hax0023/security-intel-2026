# Two-Factor Authentication SMS Code Reuse Across Multiple Accounts

## Metadata
- **Source:** HackerOne
- **Report:** 66223 | https://hackerone.com/reports/66223
- **Submitted:** 2015-06-05
- **Reporter:** dia2diab
- **Program:** Coinbase
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Authentication Bypass, Two-Factor Authentication Weakness, Account Takeover, Insufficient Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical flaw in Coinbase's SMS-based 2FA implementation allows an attacker to authenticate multiple accounts sharing the same phone number by swapping SMS verification codes between email addresses. An attacker can log into account A using account B's SMS code and vice versa, completely bypassing 2FA security controls.

## Attack scenario
1. Attacker creates or compromises two Coinbase accounts (Account A and Account B) that both use the same phone number for SMS 2FA
2. Attacker initiates login to Account A from one browser, receives SMS code 6020930
3. Attacker simultaneously initiates login to Account B from another browser, receives SMS code 1091566
4. Attacker intentionally swaps the codes: enters code 1091566 for Account A and code 6020930 for Account B
5. Both accounts successfully authenticate despite mismatched code-to-account associations
6. Attacker gains unauthorized access to multiple accounts, potentially stealing funds or sensitive data

## Root cause
The backend SMS 2FA verification logic validates that the submitted code matches a valid SMS code for the shared phone number, but fails to verify that the code corresponds to the specific email/account that initiated the login request. The system only checks if a code is valid for the phone number rather than validating the code-to-account mapping.

## Attacker mindset
An attacker would recognize that SMS 2FA provides a false sense of security when the same phone number is shared across multiple accounts. By understanding this implementation weakness, they can systematically compromise multiple high-value accounts (such as cryptocurrency exchange accounts) with minimal additional effort, since obtaining one account's credentials grants access to all accounts using the same phone number.

## Defensive takeaways
- Implement strict one-to-one mapping between phone numbers and accounts; prevent phone number reuse or enforce additional verification when multiple accounts share a phone
- Validate that the SMS code provided corresponds to both the phone number AND the specific account/email address that requested authentication
- Associate SMS codes with session tokens tied to the specific login attempt, not just the phone number
- Implement rate limiting and alerting when multiple login attempts using the same phone number occur in short timeframes
- Log and monitor code mismatch attempts as potential fraud indicators
- Consider requiring additional verification when accounts share phone numbers
- Use TOTP or hardware keys as primary 2FA mechanisms instead of SMS, or use SMS only as a secondary factor

## Variant hunting
Test if the same vulnerability exists with shared email addresses across multiple accounts with different phone numbers
Check whether backup codes can be used interchangeably across accounts
Verify if the vulnerability applies to other authentication factors (security questions, backup email verification)
Test if timing windows matter: can codes from non-overlapping login sessions be swapped
Assess whether the vulnerability extends to account recovery flows using SMS
Check if the same phone number can be registered to accounts in different regions or with different currencies

## MITRE ATT&CK
- T1110 - Brute Force
- T1187 - Forced Authentication
- T1556 - Modify Authentication Process
- T1621 - Multi-Factor Authentication Interception

## Notes
This vulnerability is particularly severe for cryptocurrency exchanges like Coinbase where account compromise directly leads to financial loss. The reporter clearly demonstrated the flaw by providing specific test cases showing the logic error. The vulnerability requires either existing account access or knowledge of multiple account email addresses, reducing but not eliminating the practical risk. The 2FA mechanism is rendered completely ineffective for users who share phone numbers across multiple accounts, which may occur in corporate environments, families, or through social engineering where an attacker creates secondary accounts.

## Full report
<details><summary>Expand</summary>

Hello Coinbase Security Team

I just found a problem in Two-factor authentication mechanism, here is the details and how to reproduce this issue:

I have two accounts with two emails on `████` i active `2FA` on the both of two emails with this phone number `██████████.

From `Chrome` i will try to login using my first email `█████` and now i recieved my code related to this email here `6020930`.

From `FireFox` i will try to do the same thing using my second email `████████` and now i recieved my second code for the second email `1091566`.

Logically, the following steps must be excuted to make the two accounts be logged in:

`████████` => `6020930`
`████` => `1091566`

But the problem is when i change the two code and emails to be 
`███` => `1091566`
`███████` => `6020930`

I found myself be logged in with two accounts and there is no problem there, The exactly problem is you allow accounts that have the same number to be logged in with each other verification code if they request a login via SMS.

Thank you.
█████ 

</details>

---
*Analysed by Claude on 2026-05-24*
