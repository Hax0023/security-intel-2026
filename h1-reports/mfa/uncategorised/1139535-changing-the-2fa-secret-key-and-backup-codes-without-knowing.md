# Changing 2FA Secret Key and Backup Codes Without Knowing Current OTP

## Metadata
- **Source:** HackerOne
- **Report:** 1139535 | https://hackerone.com/reports/1139535
- **Submitted:** 2021-03-29
- **Reporter:** whhackersbr
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Authentication Bypass, Broken Access Control, Insufficient Authentication, Credential Management Weakness
- **CVEs:** None
- **Category:** uncategorised

## Summary
The HackerOne account settings allowed users to change their 2FA secret key and backup codes without verifying knowledge of the current OTP, despite the UI requiring it. An attacker with access to a victim's account could bypass this check by sending a crafted GraphQL mutation that accepted the new 2FA credentials with only password verification.

## Attack scenario
1. Attacker gains access to victim's HackerOne account credentials (through phishing, credential stuffing, or other means)
2. Attacker logs in to victim's account and navigates to 2FA settings
3. Attacker captures the GraphQL endpoint and mutation structure used for updating 2FA credentials
4. Attacker crafts a malicious GraphQL request with new TOTP secret and backup codes, including victim's password and any valid OTP code
5. Attacker sends the request which bypasses OTP validation checks, updating the 2FA configuration
6. Attacker can now sign in using the new 2FA credentials they created, locking out the legitimate user

## Root cause
The backend GraphQL mutation for updating 2FA credentials did not properly validate that the user providing the current OTP actually knew the current 2FA secret. The backend accepted the mutation request with password verification alone, while the frontend UI enforced stricter validation. This is a classic case of security controls implemented only on the client-side without corresponding server-side enforcement.

## Attacker mindset
An account takeover attacker would recognize that 2FA bypass enables permanent account compromise. By replacing the victim's 2FA credentials with their own, the attacker can maintain persistent access even if the victim discovers the compromise and tries to reset credentials. This is a high-value target for attackers seeking to maintain access to bug bounty platforms or critical user accounts.

## Defensive takeaways
- Always enforce security-critical validations on the server-side; never rely solely on client-side checks
- Require verification of the current 2FA OTP before allowing ANY changes to 2FA configuration, including setting new secret keys or backup codes
- Implement rate limiting and alerting on 2FA configuration changes to detect suspicious activity
- Log all 2FA modifications with detailed audit trails for forensic investigation
- Use separate verification methods: password alone is insufficient for 2FA changes when 2FA is already enabled
- Consider requiring additional verification factors (email confirmation, backup authentication method) for sensitive account changes
- Implement server-side validation that strictly mirrors and enforces all client-side security constraints
- Add monitoring for sessions attempting to modify 2FA credentials to detect account compromise attempts

## Variant hunting
Check for similar bypass patterns in other mutation endpoints that handle sensitive account modifications (password changes, email changes, recovery options)
Test whether the signature parameter validation is properly enforced server-side or if it can be forged
Investigate if other GraphQL mutations have similar client-side/server-side validation mismatches
Examine whether expired or replayed OTP codes are accepted in the mutation
Test if authentication tokens with limited scope could still modify 2FA settings
Check if password-only authentication is insufficient for other security-sensitive operations

## MITRE ATT&CK
- T1110 - Brute Force (credential access leading to account compromise)
- T1098 - Account Manipulation (modifying 2FA settings)
- T1556 - Modify Authentication Process (bypassing 2FA verification)
- T1199 - Trusted Relationship (leveraging authenticated session)
- T1078 - Valid Accounts (using legitimate but compromised credentials)

## Notes
The report demonstrates a critical authentication bypass in a security-focused platform. The presence of a signature field in the mutation suggests the developers were aware of the need for verification but failed to properly implement it server-side. The fact that the attack requires an existing authenticated session with the victim's credentials makes it a post-authentication account takeover vulnerability, which is still critical as it prevents account recovery even after password reset. The redacted nature of some fields (TOTP secret, backup codes) in the reproduction steps suggests HackerOne properly handled sensitive disclosure.

## Full report
<details><summary>Expand</summary>

## Summary:

 After the setup of 2FA, disabling or editing it should require the 2FA OTP.
But it can be bypassed.

## Steps To Reproduce:

1) Sign in to a new HackerOne account.
2) Setup 2FA; and
3) Try to disable it without knowing the OTP.

You can't, you need to know the `Authentication Code` or `Backup Code`.

{F1246364}

Let's bypass it:

1) Open Google Authenticator and create a new account using `██████` as the setup key;
2) Sign in to your HackerOne account;
3) Replay the HTTP Request below (update `X-Auth-Token`, `password`, and `otp_code` using the OTP generated on Google Authenticator):

```
POST /graphql HTTP/1.1
Host: hackerone.com
content-type: application/json
X-Auth-Token: ******************************
Content-Length: 1221

{"operationName":"UpdateTwoFactorAuthenticationCredentials","variables":{"password":"******************************","otp_code":"******************************","signature":"f3a55d33972b3ac5433dc1ea3f36bed8b6813bf9","backup_codes":["b144ab9f9bc17195","09cc146d7a382931","95bd3133a5bab481","b54d2a14acc7ff0b","46f36d0d72096963"],"totp_secret":"███████","backup_code":"b144ab9f9bc17195"},"query":"mutation UpdateTwoFactorAuthenticationCredentials($password: String!, $otp_code: String!, $backup_code: String!, $totp_secret: String!, $backup_codes: [String]!, $signature: String!) {\n  updateTwoFactorAuthenticationCredentials(input: {password: $password, otp_code: $otp_code, backup_code: $backup_code, totp_secret: $totp_secret, backup_codes: $backup_codes, signature: $signature}) {\n    was_successful\n    errors(first: 100) {\n      edges {\n        node {\n          id\n          type\n          field\n          message\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    me {\n      id\n      remaining_otp_backup_code_count\n      totp_supported\n      totp_enabled\n      remaining_otp_backup_code_count\n      account_recovery_phone_number\n      __typename\n    }\n    __typename\n  }\n}\n"}
```

The 2FA secret key and backup codes will be changed.
You didn't need to know the old 2FA OTP to make the changes.

{F1246361}

4) Sign out and try to sign in again.
Now you need to use the new 2FA OTP, the old one doesn't work anymore.

## Recommendation:

Don't allow changes on 2FA configuration without confirming that the user knows the 2FA OTP.

## Impact

An attacker can change the 2FA secret key and backup codes without knowing the 2FA OTP of the victim.

</details>

---
*Analysed by Claude on 2026-05-24*
