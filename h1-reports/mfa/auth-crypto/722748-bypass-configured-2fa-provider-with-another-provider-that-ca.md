# Bypass Configured 2FA Provider with Another Provider at Login

## Metadata
- **Source:** HackerOne
- **Report:** 722748 | https://hackerone.com/reports/722748
- **Submitted:** 2019-10-25
- **Reporter:** christophwurst
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Two-Factor Authentication (2FA) Bypass, Insufficient Access Control, Missing Validation
- **CVEs:** CVE-2019-15617
- **Category:** auth-crypto

## Summary
Nextcloud 17 allows users to set up alternative 2FA providers during the login challenge phase without validating that a 2FA provider is already configured. An attacker can bypass an enforced 2FA requirement by setting up a new provider when prompted with a previously configured one, allowing login without completing the original 2FA method.

## Attack scenario
1. Administrator enforces mandatory 2FA for all users in Nextcloud 17
2. Legitimate user configures a 2FA provider (e.g., TOTP) via settings or during initial login setup
3. User logs out of their account
4. Attacker with the user's credentials attempts login and enters the password successfully
5. System prompts for the configured 2FA provider challenge
6. Attacker navigates to /login/setupchallenge endpoint and sets up a different 2FA provider instead of completing the original challenge
7. System grants authentication without validating completion of the original 2FA method

## Root cause
Missing authorization and validation check in the /login/setupchallenge endpoint. The application does not verify that a 2FA provider is already configured before allowing setup of an alternative provider, nor does it enforce that the originally configured provider must be completed first.

## Attacker mindset
An attacker with valid credentials but without access to the user's configured 2FA method (lost phone, forgotten backup codes, etc.) can exploit this to gain unauthorized access by substituting an alternative 2FA method they control.

## Defensive takeaways
- Implement strict validation that prevents 2FA provider setup during active authentication challenges
- Ensure 2FA provider configuration is only permitted outside of the login challenge phase
- Validate that users complete the originally configured 2FA method before allowing alternative methods
- Enforce a whitelist approach: only allow setup of new 2FA providers when not in a challenge state
- Add authorization checks to ensure /login/setupchallenge is only accessible at appropriate times
- Implement audit logging for 2FA provider changes during authentication flows
- Use session state management to track whether a user has already satisfied 2FA requirements

## Variant hunting
Check if other authentication endpoints allow provider changes mid-challenge (e.g., /login/validate, /login/confirm)
Test if backup codes or recovery mechanisms can be accessed during active 2FA challenge
Verify if disabling an already-configured provider is possible during login challenge
Investigate whether the vulnerability applies to other 2FA providers (WebAuthn, U2F, SMS, etc.)
Test if users can modify their 2FA settings via API endpoints during authentication
Check if the vulnerability exists in subsequent Nextcloud versions with different auth flows
Test whether rapid sequential 2FA setup requests can bypass validation
Investigate if same-provider re-setup is possible during challenge to reset state

## MITRE ATT&CK
- T1586 - Compromise Accounts
- T1110 - Brute Force
- T1556 - Modify Authentication Process
- T1528 - Steal Application Access Token

## Notes
This vulnerability demonstrates a critical flaw in authentication flow design where the application conflates two separate operations: authentication challenge completion and security settings modification. The /login/setupchallenge endpoint should not be accessible during an active 2FA challenge. The bug is particularly severe because enforced 2FA is a compensating control, and this bypass completely negates its security benefit. The vulnerability affects the core authentication mechanism and would likely impact all user accounts in an organization that enforces mandatory 2FA.

## Full report
<details><summary>Expand</summary>

In Nextcloud 17 there is the possibility to set up 2FA providers at login. A missing check allows the following steps

1) Enforce 2FA for all users
2) As a user, configure a 2FA provider (via settings or at login)
3) Log out
4) Log in again (password only)
5) When prompted with the earlier set up provider, go to /login/setupchallenge
6) Set up another provider that hasn't been set up before
7) You're logged in

## Impact

Bypass a user's second-factor authentication protection.

</details>

---
*Analysed by Claude on 2026-05-24*
