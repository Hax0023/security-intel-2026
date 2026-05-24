# Deactivated Staff Account Login via Shopify Mobile App

## Metadata
- **Source:** HackerOne
- **Report:** 175490 | https://hackerone.com/reports/175490
- **Submitted:** 2016-10-13
- **Reporter:** 0xm1racle
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Access Control, Session Management
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A deactivated staff account could still successfully authenticate and log in through the Shopify mobile application, despite being disabled by the account owner. This allowed unauthorized access to shop data and functions through a disabled credential.

## Attack scenario
1. Owner creates and manages staff account with appropriate permissions
2. Owner deactivates staff account through admin panel to revoke access
3. Attacker (or disgruntled employee) attempts login with deactivated credentials on mobile app
4. Mobile app successfully authenticates deactivated staff credentials
5. Attacker gains access to shop data, customers, and orders despite account deactivation
6. Unauthorized actions performed under deactivated staff identity

## Root cause
The mobile application's authentication logic does not properly validate the account deactivation status during login. The backend likely returns an auth token without checking the staff account's active status, or the mobile app accepts tokens without verifying current account state.

## Attacker mindset
A disgruntled former employee or insider threat could maintain persistent access after being removed from the organization. Alternatively, an attacker with compromised credentials could bypass revocation attempts by using the mobile app instead of web interface.

## Defensive takeaways
- Implement account status validation on every authentication request across all clients (web, mobile, API)
- Revoke all existing session tokens when an account is deactivated
- Add real-time account status checks before granting access to protected resources
- Ensure mobile app uses same authentication and authorization logic as web platform
- Implement audit logging for authentication attempts with deactivated accounts
- Add multi-channel deactivation enforcement (don't rely on client-side checks)
- Implement token expiration and refresh validation with account status verification

## Variant hunting
Test other disabled account types (owner, partner accounts)
Check if deactivated accounts retain API access tokens
Test if browser caching allows deactivated account login after clearing app cache
Verify deactivation works across all Shopify applications and integrations
Check if suspended (vs deactivated) accounts have the same issue
Test race conditions between deactivation and active login attempts

## MITRE ATT&CK
- T1078 - Valid Accounts
- T1110 - Brute Force
- T1555 - Credentials from Password Managers
- T1556 - Modify Authentication Process
- T1550 - Use Alternate Authentication Material

## Notes
Low-complexity vulnerability with high business impact. The fix likely required backend enforcement rather than client-side changes. This is a critical privilege escalation vector in multi-user commerce environments. Report demonstrates clear PoC with reproducible steps.

## Full report
<details><summary>Expand</summary>

Hi Shopify,

Deactivated staff account is able to login in shopify mobile app.

__STEPS__

1. Login your owner account
2. Go to Staff Accounts and deactivate your staff account
3. Login to your staff account in your shopify mobile app

__As you can see  you were able to login even the staff account was deactivated by the account owner__

</details>

---
*Analysed by Claude on 2026-05-24*
