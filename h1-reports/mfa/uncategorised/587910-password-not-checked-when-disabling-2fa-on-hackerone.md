# Password Validation Bypass When Disabling 2FA on HackerOne

## Metadata
- **Source:** HackerOne
- **Report:** 587910 | https://hackerone.com/reports/587910
- **Submitted:** 2019-05-22
- **Reporter:** tester1231233
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Insufficient Input Validation, Broken Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
The 2FA disabling functionality on HackerOne fails to validate the password parameter, allowing attackers to disable two-factor authentication by providing any arbitrary password alongside a valid backup code or OTP. This bypasses a critical security confirmation step designed to prevent unauthorized account modifications.

## Attack scenario
1. Attacker gains temporary access to a user's account or session (phishing, session hijacking, XSS)
2. Attacker navigates to /settings/auth and initiates the disable 2FA process
3. The disable 2FA dialog prompts for either backup code or OTP, and a password
4. Attacker enters a valid backup code (if previously obtained) or brute-forces/guesses OTP
5. Attacker enters any random password value in the password field
6. Server processes the GraphQL mutation without validating the password, successfully disabling 2FA

## Root cause
The backend GraphQL mutation `destroyTwoFactorAuthenticationCredentials` accepts the password parameter but does not validate it against the user's actual password hash before processing the request. The validation logic likely only checks the OTP/backup code validity while skipping password verification.

## Attacker mindset
An attacker with partial account compromise (valid session or backup codes) could permanently disable 2FA protection to maintain persistent access without triggering re-authentication alerts. This converts a temporary access into a more stable foothold.

## Defensive takeaways
- Always validate password re-confirmation on sensitive account modifications (2FA, email change, logout-all-sessions)
- Implement server-side password hashing comparison for confirmation steps, not just presence checks
- Use rate limiting and anomaly detection on sensitive endpoint mutations
- Require stronger authentication (passwordless authentication, hardware keys) for 2FA modifications
- Log all 2FA toggle attempts with IP/session context for user review
- Consider requiring a recent authentication event (timestamp-based) before allowing 2FA changes
- Test GraphQL mutations with invalid/missing security parameters as part of security review

## Variant hunting
Check email change/update endpoints for similar password bypass patterns
Test session logout-all functionality for password validation bypass
Review password change/reset flows for missing confirmation steps
Test API endpoints handling sensitive user data modifications (phone, recovery email, trusted devices)
Check if backup code regeneration requires password validation
Verify other MFA-related mutations (enable MFA, change MFA method) for validation bypass
Test authenticated API endpoints generally for missing re-confirmation on destructive operations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process
- T1621 - Multi-Factor Authentication Interception
- T1199 - Trusted Relationship

## Notes
The vulnerability is particularly severe in the context of HackerOne's bug bounty platform where 2FA is mandatory for programs requesting it. An attacker could disable 2FA on researcher/hunter accounts to maintain access and submit malicious reports. The GraphQL mutation structure shows the backend explicitly receives the password parameter but fails to enforce its validation, suggesting this is an implementation oversight rather than a design choice.

## Full report
<details><summary>Expand</summary>

Hi,

when I was submitted a report to a program that request `2FA` ON, I notice that if you try to disable this option will ask for `backup code - password` and if you enter a random password in the request filed and a correct `backup code` it will be successfully disabled the `2FA` without check if the password was correct or not.

#PoC
1. go to your account and activate the `2FA` from `/settings/auth`
2. after active this option click on `Disabled` icon beside `Two-factor authentication`.
3. a new window will open asking for `Authentication or backup code - Password` to confirm the disabled.
{F494646}
4. in the first box enter a valid `Authentication or backup code` and in the password filed enter any random/wrong password and click save.
5. the option will be disabled successful without check the validation of the password.
 
#graphql Request
```json

{"query":"mutation Destroy_two_factor_authentication_credentials_mutation($input_0:DestroyTwoFactorAuthenticationCredentialsInput!,$first_1:Int!,$throttle_time_2:Int!,$first_4:Int!,$size_3:ProfilePictureSizes!) {destroyTwoFactorAuthenticationCredentials(input:$input_0) {clientMutationId,...F1,...F2}} fragment F0 on User {id,totp_supported,totp_enabled,remaining_otp_backup_code_count,account_recovery_phone_number,username,name,_profile_picturePkPpF:profile_picture(size:$size_3)} fragment F1 on DestroyTwoFactorAuthenticationCredentialsPayload {me {id,user_type,_program_health_acknowledgements2aGZgn:program_health_acknowledgements(first:$first_1,throttle_time:$throttle_time_2) {edges {node {id,reason,team_member {user {id},id,team {handle,name,sla_failed_count,id}}},cursor},pageInfo {hasNextPage,hasPreviousPage}},new_feature_notification {name,description,url,id},...F0}} fragment F2 on DestroyTwoFactorAuthenticationCredentialsPayload {me {totp_enabled,remaining_otp_backup_code_count,id},was_successful,_errors3exXYb:errors(first:$first_4) {edges {node {type,field,message,id},cursor},pageInfo {hasNextPage,hasPreviousPage}}}",
"variables":{"input_0":{"password":"██████████","otp_code":"███","clientMutationId":"9"},"first_1":1,"throttle_time_2":3600,"first_4":100,"size_3":"small"}}
```

## Impact

user can disable `Two-factor authentication` without entering a valid password

</details>

---
*Analysed by Claude on 2026-05-24*
