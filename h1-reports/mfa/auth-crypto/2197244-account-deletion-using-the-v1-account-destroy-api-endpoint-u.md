# Account deletion using /v1/account/destroy API endpoint bypassing 2FA verification

## Metadata
- **Source:** HackerOne
- **Report:** 2197244 | https://hackerone.com/reports/2197244
- **Submitted:** 2023-10-07
- **Reporter:** erdy
- **Program:** Mozilla
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Missing Authentication, Missing Authorization, Broken Authentication, Insufficient Security Controls, Lack of Multi-Factor Authentication Enforcement
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The POST /v1/account/destroy endpoint fails to enforce 2FA verification and does not require authentication headers, allowing an unauthenticated attacker to delete user accounts with only knowledge of the email and password. Since authPW is computed client-side using publicly available source code, attackers can calculate valid credentials and perform unauthorized account deletion.

## Attack scenario
1. Attacker obtains a target user's email and password through phishing, credential stuffing, or data breach
2. Attacker reviews publicly available Mozilla FXA authentication client source code to understand authPW calculation logic
3. Attacker calculates the valid authPW for the target account using the exposed algorithm
4. Attacker sends POST request to /v1/account/destroy with email and calculated authPW, without Authorization header
5. Server processes request without verifying 2FA status or requiring valid authentication session
6. Target user's Firefox account is permanently deleted, denying access to all associated services

## Root cause
The account destruction endpoint lacks proper security controls: (1) does not enforce 2FA verification despite it being a sensitive operation, (2) does not require valid authentication tokens/session, (3) accepts password-derived credentials without validating an active authenticated session, and (4) relies on client-side credential computation that is publicly documented

## Attacker mindset
An attacker with leaked or compromised passwords could perform account sabotage at scale, targeting competitors, journalists, or political figures by permanently deleting their Mozilla accounts and associated data. The attack requires no social engineering or technical complexity once credentials are obtained.

## Defensive takeaways
- Enforce mandatory 2FA verification for all sensitive account operations including deletion, regardless of authentication method
- Require valid, server-issued authentication tokens/sessions for destructive API endpoints
- Validate that API requests originate from authenticated sessions with matching user context
- Implement rate limiting and account deletion confirmation mechanisms (email verification, time delays)
- Add account deletion audit logging and alert users to deletion attempts via registered email
- Consider moving sensitive credential calculations to server-side only, avoiding public exposure of crypto algorithms
- Implement IP address and device fingerprint validation for high-risk operations
- Use Authorization headers as mandatory requirement for all authenticated endpoints

## Variant hunting
Test other destructive endpoints (/v1/account/reset, /v1/account/lock) for similar 2FA bypass
Check if password reset endpoint requires 2FA verification
Test if other sensitive operations (payment methods, recovery codes, session termination) enforce 2FA
Verify if the lack of Authorization header validation exists in other authentication endpoints
Investigate whether user impersonation is possible using only email + authPW without session
Check if account recovery endpoints bypass 2FA requirements
Test API endpoints across different environments (staging, production) for consistent vulnerability
Examine similar Mozilla services (Pocket, MDN, etc.) for same vulnerability pattern

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583 - Acquire Infrastructure
- T1589 - Gather Victim Identity Information
- T1556 - Modify Authentication Process
- T1098 - Modify User Account
- T1531 - Account Access Removal
- T1040 - Network Sniffing

## Notes
This is a critical vulnerability affecting Firefox account security. The public availability of authentication algorithm source code significantly lowers the attack barrier. The fact that authPW can be computed without server interaction violates security principles. This vulnerability likely affects all users whose passwords have been compromised in any capacity. Mozilla should immediately require 2FA for account deletion and implement session validation for all destructive operations.

## Full report
<details><summary>Expand</summary>

## Summary:
The account deletion endpoint at `POST /v1/account/destroy` does not check for 2FA and doesn't require an authorization header. Therefore, an unauthenticated attacker who knows the password of a user can delete their account without the need of 2FA.

## Steps To Reproduce:

  1. Send a POST request to https://api-accounts.stage.mozaws.net/v1/account/destroy with the following body (do not include an Authorization header, if it is included and doesn't match the e-mail in the body, the request will fail):
```
{"email":"<email>","authPW":"<authPW>"}
```
The authPW can be calculated by the attacker since it is created client-side and the source code is [publicly available](https://github.com/mozilla/fxa/blob/fd716ec3f3461d22b847f337f6b1e899d671ee0d/packages/fxa-auth-client/lib/crypto.ts#L18).

Please refer to {F2756126} to calculate the authPW.

## Supporting Material/References:

An example of a successful account deletion:
{F2756132}

## Impact

## Summary:
An unauthenticated attacker can delete Firefox accounts of other users without needing 2FA, if the attacker knows their password.

</details>

---
*Analysed by Claude on 2026-05-24*
