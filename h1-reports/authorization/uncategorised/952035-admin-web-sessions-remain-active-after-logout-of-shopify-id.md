# Admin web sessions remain active after email change on Shopify ID

## Metadata
- **Source:** HackerOne
- **Report:** 952035 | https://hackerone.com/reports/952035
- **Submitted:** 2020-08-05
- **Reporter:** jaka-tingkir
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Session Management, Privilege Escalation, Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
When a Shopify account email address is changed, active sessions and authentication tokens associated with the old email address are not invalidated. This allows an attacker with access to the old email to maintain persistent admin access to associated stores even after the email has been changed by the legitimate account owner.

## Attack scenario
1. Attacker gains temporary access to a legitimate user's Shopify account (via phishing, credential stuffing, etc.)
2. Attacker initiates a session in their own browser using the compromised credentials
3. Legitimate user discovers the compromise and changes their account email address to regain control
4. Attacker's existing session/authentication token remains valid despite email change
5. Attacker opens another browser and logs in with the old email address, receiving authentication code
6. Attacker gains full admin access to the store, bypassing the email change security measure

## Root cause
Shopify's session invalidation logic does not revoke existing sessions and authentication tokens when an email address is changed on an account. The application likely ties session validity to user ID rather than email, but fails to invalidate existing sessions during account modifications.

## Attacker mindset
An attacker who has gained initial access to a Shopify account can maintain persistence by establishing sessions before the victim mitigates the compromise. Even when the victim changes their email, the attacker's old sessions remain valid, providing a backdoor for continued unauthorized access.

## Defensive takeaways
- Implement automatic session invalidation when account email addresses are changed
- Invalidate all active authentication tokens and sessions across all browsers during sensitive account modifications
- Implement device/session tracking and require re-authentication for accessing stores after email changes
- Add notifications for all active sessions before allowing email changes, with option to terminate them
- Implement step-up authentication or passwordless verification when accessing stores after recent account changes
- Add security logging for email changes and cross-reference with active sessions

## Variant hunting
Test if password changes also fail to invalidate sessions
Check if other account modifications (name, address, phone) invalidate sessions
Test if changing account recovery options (2FA settings) invalidates sessions
Investigate if API tokens are revoked during email changes
Test if session invalidation works across different Shopify product lines (POS, app admin, etc.)
Check if the old email can access other associated stores through the same account

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process
- T1550 - Use Alternate Authentication Material

## Notes
This is a follow-up to report #837729 which identified similar session persistence issues. The vulnerability affects account access control for multi-store scenarios. The reporter provided test credentials and store details for verification, indicating reproducibility. The core issue is insufficient invalidation of authentication state during account modifications.

## Full report
<details><summary>Expand</summary>

previously on #837729 a session is still valid and the store password can be seen.

this time I report that the session is still valid despite changing the email address on the shopify account.

## summary: accounts that have changed email addresses still have permission to enter the store through another browser, so old emails can still have access to the store

## steps for reproduction
1. Change your account email (the account has handled several stores) and confirm (I use Firefox)
2. The email account has been successfully replaced
3. open another browser (chrome beta) and log in with the old email, here you are asked to enter the code from the email and you have successfully logged in the account
4. Try opening your shop and logging in with your old email (here I was directed to enter and still have full access, even after changing my email address).

please see the https://150hy.myshopify.com store (test store) and ████@wearehackerone.com and ██████+top@wearehackerone.com accounts (password = ██████████)

## Impact

access not revoke after changed email address on accounts shopify

</details>

---
*Analysed by Claude on 2026-05-24*
