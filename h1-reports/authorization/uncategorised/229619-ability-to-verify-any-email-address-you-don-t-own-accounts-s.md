# Email Address Verification Bypass via Token Leakage in accounts.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 229619 | https://hackerone.com/reports/229619
- **Submitted:** 2017-05-18
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Authentication, Insufficient Input Validation, Token Handling Flaw, Account Takeover
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can verify ownership of any email address they do not own by exploiting a token leakage vulnerability in the email change functionality. The confirmation token is exposed in the resend verification link, allowing an attacker to complete email verification without receiving the confirmation email.

## Attack scenario
1. Attacker logs into their own accounts.shopify.com account
2. Attacker initiates email change process and enters target email address (victim's email)
3. System sends verification email to target address but also displays resend link containing the confirmation token
4. Attacker copies the confirmation token from the resend URL
5. Attacker navigates directly to the verification endpoint with the token without needing to receive the verification email
6. System validates the token and completes email change, effectively taking over the target email account

## Root cause
The confirmation token is transmitted in the URL during the resend operation, making it accessible to the authenticated user without requiring them to actually receive the verification email. The verification endpoint likely only validates the token without verifying that the requester actually owns the email address or received the original email.

## Attacker mindset
An attacker would recognize that the resend functionality exposes the sensitive confirmation token in plaintext within a URL. They would realize that if the verification process only checks token validity rather than email ownership, they could bypass the email verification step entirely and hijack any email address they target.

## Defensive takeaways
- Never include sensitive tokens (confirmation, reset, verification) in URLs; use secure session cookies or POST requests instead
- Implement email verification that requires the recipient to click a link in their inbox, not just token possession
- Add rate limiting and anomaly detection to email change operations from accounts
- Log and alert on email change attempts, especially to external domains
- Verify that email change requests are correlated with actual email receipt before completing the change
- Use single-use, short-lived tokens that cannot be accessed through resend endpoints
- Require additional authentication factors (password re-entry, 2FA) for account-critical changes like email

## Variant hunting
Check password reset functionality for similar token leakage in resend endpoints
Review all email change/update endpoints across Shopify ecosystem (admin.shopify.com, etc)
Test other account recovery mechanisms for token exposure
Examine 2FA setup/change processes for confirmation token leakage
Check for similar patterns in payment method verification flows
Review session handling around sensitive account modifications

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1555 - Credentials from Password Managers
- T1589 - Gather Victim Identity Information
- T1566 - Phishing

## Notes
This is a critical account takeover vulnerability with minimal complexity. The attacker only needs a valid Shopify account to target any email address. The fix requires fundamental redesign of the email verification flow to ensure tokens are not exposed and verification requires actual email access. The vulnerability likely affects multiple email-related operations (password reset, 2FA, etc) making this a systemic issue in Shopify's token handling architecture.

## Full report
<details><summary>Expand</summary>

## Summary: 
During testing it's been found that in `accounts.shopify.com` it's possible to change your email address to any email address that you don't own and confirm that email due to the confirmation token being leaked.

## Steps to reproduce: 
1. Login to `https://accounts.shopify.com/account`
2. Click **Change** Next to email
3. Enter any new email address
4. You'll see a message saying:
 
```
Verification email sent
We sent you an email to verify that you own "email@example.com". We'll change your email once you verify that you own it.
```
with a link to resend the verification email or cancel the change.
5.- Copy the resend link, it will look like this: `https://accounts.shopify.com/email-change/<Confirmation-TOKEN>/resend`
6.- Go to `https://accounts.shopify.com/email-change/<Confirmation-TOKEN>/` and the email will be verified even though you don't own it.

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
