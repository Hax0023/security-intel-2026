# Two Factor Authentication Bypass via Google Apps OAuth Login

## Metadata
- **Source:** HackerOne
- **Report:** 178293 | https://hackerone.com/reports/178293
- **Submitted:** 2016-10-26
- **Reporter:** dhaval
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Misconfiguration, Insufficient Access Controls, OAuth Integration Flaw
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A misconfiguration in Shopify's authentication system allows attackers to bypass two-factor authentication (2FA) by authenticating via Google Apps OAuth login. Once a user signs in through Google Apps, their 2FA is automatically disabled without notification, allowing subsequent standard logins to proceed without 2FA verification.

## Attack scenario
1. Attacker identifies a target Shopify admin account that has 2FA enabled with Google Authenticator
2. Attacker discovers that Google Apps login is enabled as an alternative login method in account settings
3. Attacker initiates a Google Apps OAuth login flow at the login endpoint with google_apps=1 parameter
4. OAuth authentication succeeds and user is logged in without 2FA challenge being enforced
5. System automatically disables 2FA protections associated with the account upon Google Apps login
6. Attacker or subsequent login attempts can now access the admin panel using standard credentials without 2FA code requirement

## Root cause
The authentication system failed to enforce 2FA checks during OAuth-based login flows. The implementation treats Google Apps OAuth login as a separate authentication pathway that bypasses 2FA validation logic. Additionally, the system automatically disables 2FA when OAuth login is used, rather than maintaining 2FA as a security requirement across all authentication methods.

## Attacker mindset
An attacker with knowledge of the target's email would attempt to use the Google Apps login option as an easier bypass vector, especially if they can control or compromise the associated Google account. The automatic disabling of 2FA creates a persistent vulnerability requiring no ongoing 2FA code interception.

## Defensive takeaways
- Enforce 2FA checks consistently across all authentication pathways, including OAuth and third-party login methods
- Never automatically disable 2FA when alternative login methods are activated; instead, require 2FA on all paths or maintain separate security policies
- Require explicit user confirmation before disabling security features like 2FA
- Send security notifications (email/SMS) whenever 2FA status changes or is disabled
- Implement security tests that verify 2FA is enforced across all login flows and authentication methods
- Audit OAuth/SSO integrations to ensure they don't introduce security regressions in existing protections
- Consider requiring 2FA re-verification before enabling alternative login methods that might bypass it

## Variant hunting
Check if other SSO/OAuth providers (Apple Sign-In, Microsoft, GitHub, etc.) have similar 2FA bypass behavior
Test if other security features (API keys, webhook restrictions) are similarly disabled when OAuth login is activated
Investigate whether the google_apps parameter can be manipulated to affect other authentication logic
Check if account recovery methods bypass 2FA verification in similar ways
Test if 2FA re-enablement can be achieved through alternative paths after being disabled
Examine whether session tokens from OAuth login have different security properties than standard 2FA-verified sessions

## MITRE ATT&CK
- T1190
- T1078
- T1556
- T1621

## Notes
This report demonstrates a critical design flaw where security features are degraded rather than maintained during feature additions. The lack of notification when 2FA is disabled suggests poor security event logging. The vulnerability affects the availability and integrity of the 2FA security control. The report's simplicity and clarity made it easy to understand but lacked technical depth regarding exploitation difficulty and scope of affected users.

## Full report
<details><summary>Expand</summary>

Hey

There seems to be a weird misconfiguration which leads to bypass of two factor authorisation

#### Scenario

1. Let's assume you have setup Two Factor Authorisation with Google Authenticator

2. You now activate `Google Apps` from `Login services` at https://shop-1.myshopify.com/admin/settings/account

3. Now your try to "Sign In with Google" `https://shop-1.myshopify.com/admin/auth/login?google_apps=1`

What's weird is no two factor code is required and you directly land in Admin Panel

#### Issue

Issue here is Two Factor Authorisation is disabled as soon as you "Sign In with Google" and now you cannot even enable it because you can't see any Two Factor Authenticator Tab in Accounts

And now when you try to simple login with correct credentials you can access Admin Panel without Two Factor Code from Google Authenticator at `https://shop-1.myshopify.com/admin/auth/login`

Also there is no indication to via mail or notification that Two Factor Authorisation has been disabled when Two Factor Authorisation is disabled
While it shouldn't be disabled in the first place


</details>

---
*Analysed by Claude on 2026-05-24*
