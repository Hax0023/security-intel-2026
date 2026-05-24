# Account Takeover via Email Confirmation Bypass and URL Path Manipulation on SSO-Protected Merchant Accounts

## Metadata
- **Source:** HackerOne
- **Report:** 796956 | https://hackerone.com/reports/796956
- **Submitted:** 2020-02-14
- **Reporter:** ngalog
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Authentication Bypass, Account Takeover, Improper Access Control, URL Path Traversal, Insufficient Password Verification
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can take over merchant accounts protected by SSO by first bypassing email confirmation, then manipulating the URL path during account merge flow to skip password validation. By changing the URL from /login to /accounts_merge/new-password while maintaining query parameters, the attacker can set a new password on the victim account without providing the legitimate password.

## Attack scenario
1. Attacker creates a new Shopify store with the victim merchant's email address (e.g., ngalog+1@wearehackerone.com)
2. Attacker bypasses email confirmation through a separate vulnerability (referenced as #791775) to confirm the victim's email without legitimate access
3. Attacker initiates account review/merge flow and authenticates with their own store password (which they control)
4. During the account merge process, the system redirects to /login endpoint requesting the victim's master password
5. Attacker manipulates the URL by changing /login to /accounts_merge/new-password while preserving all query parameters
6. System incorrectly allows password reset without validating the original password, enabling attacker to set new credentials and complete account takeover

## Root cause
Insufficient validation of the account merge/password change workflow. The application fails to properly verify user authorization when changing URL paths in the account merge flow. The /accounts_merge/new-password endpoint does not adequately validate that the user has legitimately completed the previous authentication steps (password verification). Additionally, the system trusts URL query parameters without validating the state transitions, allowing an attacker to skip the master password verification requirement.

## Attacker mindset
The attacker demonstrates methodical exploitation of authentication bypass chains. After discovering an email confirmation bypass in a prior report, they strategically sought to prove complete account takeover is possible even with SSO protections. They identified the critical password verification step in the account merge flow as the next target and discovered that URL path manipulation could circumvent this control. This shows a 'layering' approach to security testing - combining multiple vulnerabilities to achieve end-to-end compromise.

## Defensive takeaways
- Implement strict state machine validation for multi-step authentication flows; validate not just URL parameters but the complete sequence of user actions
- Enforce password verification as a security-critical operation that cannot be bypassed through URL manipulation or endpoint switching
- For account merge/recovery flows, require explicit re-authentication with the original account credentials before any password changes
- Implement server-side session state tracking that validates legitimate progression through required steps (e.g., cannot jump from login to password reset without completing intermediate steps)
- Add additional verification when accounts with SSO are involved - consider requiring SSO provider confirmation
- Implement 2FA validation checks at account takeover-critical operations, independent of user preference settings
- Apply consistent authentication context validation across related endpoints (/login, /accounts_merge/new-password, etc.)
- Log and monitor unusual patterns such as account merge attempts from different stores or with unusual email address variations

## Variant hunting
Test other multi-step authentication flows for similar URL path manipulation (password reset, email change, billing address updates)
Attempt to manipulate query parameters across different endpoints in the accounts merge workflow
Test whether other 'protected' endpoints can be accessed by changing URL paths mid-flow (e.g., /accounts_merge/confirm, /accounts_merge/verify-mfa)
Investigate if similar bypasses exist in the SSO integration flow itself when combining with email bypass
Test whether the vulnerability persists if attacker attempts to skip even earlier steps in the merge process
Check if referer validation or origin checks are missing that could prevent cross-endpoint requests
Test account merge flows with different store types or account states
Attempt parameter pollution or duplicate parameter attacks on the merge endpoints

## MITRE ATT&CK
- T1190
- T1556
- T1110
- T1078
- T1566

## Notes
This report builds on prior vulnerability #791775 which established email confirmation bypass. The researcher demonstrates excellent security research methodology by chaining vulnerabilities and testing mitigating controls. The Shopify SSO implementation was expected to be a security boundary, but the account merge flow provided an alternative path to compromise. The reporter notes they will test with 2FA-enabled accounts in follow-up testing, suggesting 2FA may provide partial protection but likely not complete mitigation if the underlying flow logic is flawed. The severity is critical due to complete account takeover with access to all merchant data, store operations, and financial transactions.

## Full report
<details><summary>Expand</summary>

Able to Takeover Merchants Accounts  Even They Have Already Setup SSO, After Bypassing the Email Confirmation

## Summary
This report is based on the scenario that email confirmation has been bypassed already, like shown in #791775.

What happened in #791775 was, I was too excited and didn't take a step further to try to takeover merchant's account even they have SSO setup, and after reading the comment `An important mitigating factor was that this bug only affected user accounts which had not yet adopted our single login system. `, I know I have to find a way to bypass that to prove my point.

## Description
For merchant that have accounts already setup SSO, even attacker has bypassed the email confirmation, they would have no ways to takeover the rest of the accounts of the merchant, because they will need to enter the master password of the merchant in the process of merging accounts.

Let me illustrate this in graphs, in this example, the merchant that has SSO already setup is `ngalog+1@wearehackerone.com`, the attacker sign-up a store h48ngalog.myshopify.com, with email `ngalog+1@wearehackeorne.com`

Stage 1. First, for whatever reason, maybe a new feature appeared that allows attacker to bypass email confirmation again or an old bug bypass, that as an attacker with ngalog+1@wearehackerone.com confirmed, he should see this in the shop

{F716958}

Stage 2. Then, when attacker clicks Review accounts, attacker needs to put in the store password first, which is fine cause attacker signup this store account himself, so it should have no problem

{F716957}

Stage 3. After authenticating, here is the real obstacle, Shopify asks attacker for the main shop's password, for sure the attacker doesn't know the password, otherwise he could just go on and takeover the store without these steps.

{F716959}

Stage 4. Here's the magic step, note that the url path is `/login` now at stage3, change the path to `/accounts_merge/new-password` while keeping the query part the same

{F716960}

Stage 5. The victim `ngalog+1@wearehackerone.com `account has no 2FA configured, after submitting this report I'll try again with the 2FA enabled victim account and see if this still works, for now stay with me, enter a new password of attackers choice, and click do not enable 2FA etc.., and finally you'll be redirected to this page, asking you to confirm the change of password, click the button

{F716961}

And now we are done, you should be redirected to your old store, and feel free to change stores on the upper left switch store tab, or use your new password to login victim's store.

## Steps to reproduce
- Create a store, and confirm your email with victim's email, and this victim should not have 2FA setup, and should have SSO setup already
- Click the button shown in {F716958}
- enter your store's own password
- the url should now be accounts.shopify.com/login?xxxxxx, change `/login` to `/accounts_merge/new-password` while keeping the query part xxx the same {F716960}
- Enter your new password and continue without setting up the 2FA, you can try to setup the 2FA for victim, I never tried, guess it is not important, since the impact would just be locking victim out of their account
- Finally, click confirm button on the password change {F716961}

## Impact

Able to takeover merchant's account even they have SSO enabled after email confirmation bypass

</details>

---
*Analysed by Claude on 2026-05-24*
