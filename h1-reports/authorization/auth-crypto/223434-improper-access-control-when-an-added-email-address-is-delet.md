# Improper Access Control: Deleted Email Authentication Link Allows Account Access and Re-addition

## Metadata
- **Source:** HackerOne
- **Report:** 223434 | https://hackerone.com/reports/223434
- **Submitted:** 2017-04-24
- **Reporter:** h1bountyoverflow
- **Program:** Not specified in report
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Access Control, Authentication Bypass, Token Validation Flaw, Email Verification Logic Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can use a previously sent email confirmation link to regain access to an account and automatically re-add a removed email address, even after the user has explicitly deleted it from their authentication methods. The application fails to invalidate pending verification tokens when associated email addresses are removed, allowing an old confirmation link to restore deleted authentication credentials.

## Attack scenario
1. Legitimate user creates account with email A and receives confirmation link
2. User adds email B as secondary authentication and receives confirmation link for email B
3. User removes email A from authentication tab due to compromise concerns
4. Attacker who previously compromised email A clicks the original confirmation link from step 2
5. Application processes the old token and automatically adds email B back to attacker-controlled account
6. Attacker now has account access and can authenticate using the re-added email address

## Root cause
The application does not invalidate or check the current state of email addresses when processing confirmation tokens. It treats an old, valid token as authoritative without verifying that the email address is still part of the user's active authentication methods or that the token belongs to an email the user still wants to authenticate with.

## Attacker mindset
An attacker with access to a user's old email account (or who captures confirmation links before they're clicked) can exploit this flaw to maintain or regain persistent access to an account even after the user attempts to revoke that authentication method. This is particularly dangerous if the attacker still has access to the compromised email account.

## Defensive takeaways
- Invalidate all pending email verification tokens when an email address is removed from the account
- Implement email confirmation expiration windows (e.g., 24-48 hours)
- Check that the email being confirmed still exists in the user's pending authentication list before processing confirmation tokens
- Log and alert users of authentication changes and failed confirmation attempts
- Require additional verification (SMS, security question, or re-authentication) when re-adding recently removed authentication methods
- Implement rate limiting on confirmation link usage
- Send confirmation to user's registered email when email addresses are added/removed from authentication

## Variant hunting
Check if password reset tokens have similar issues after account recovery email is changed
Test if 2FA enrollment links can be reused after 2FA is disabled
Verify that API authentication tokens are invalidated when associated email is removed
Test recovery code validity after account recovery email removal
Check if SSO/OAuth linked emails can be re-added via old confirmation tokens
Test concurrent email addition/removal race conditions
Verify backup email removal behavior in password reset flows

## MITRE ATT&CK
- T1078.001
- T1190
- T1621

## Notes
This report lacks specific details about the vulnerable application, bounty amount, and response timeline. The vulnerability represents a classic example of improper state validation in multi-step authentication flows. The attacker doesn't need ongoing access to the compromised email account if they've already captured the confirmation link, though having such access increases the attack window significantly.

## Full report
<details><summary>Expand</summary>

Hi team,

There is improper access control kind of vulnerability present in your web application.


Steps to reproduce:

1. Create an account.
2.You will recevie a link on email about confrimation.
2. Login into it and add another email address in authentication tab and You will recevie a link on the new email about confrimation.
3.Remove the the any email address from it authentication tab. (Suppose your old email address got lost or hacked).

Now suppose I removed old email address from authentication tab because i doubt the my old email id got hacked.

Logically when user click on the link recived in the step 2 the user should not be allowed to enter in the application because we have removed the email from authentication tab.

When attacker click on the old link recieved in the step 2 will be able to login into the application and the old email id will be automatically added to authentication tab in that account even the we have alredy removed that email address from our account.


Please let me know if anything more is required .!



</details>

---
*Analysed by Claude on 2026-05-24*
