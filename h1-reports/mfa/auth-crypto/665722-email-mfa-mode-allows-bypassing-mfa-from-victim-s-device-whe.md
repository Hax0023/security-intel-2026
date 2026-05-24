# MFA Bypass via Mode Switching and Device Trust Manipulation in Grammarly

## Metadata
- **Source:** HackerOne
- **Report:** 665722 | https://hackerone.com/reports/665722
- **Submitted:** 2019-08-02
- **Reporter:** l1nkworld
- **Program:** Grammarly
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Multi-Factor Authentication Bypass, Insecure Direct Object References (IDOR), Client-Side Security Control Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Grammarly's MFA implementation contains a critical flaw allowing attackers to bypass multi-factor authentication by modifying request parameters during login. By changing the MFA mode from 'sms' to 'email' and disabling secure login flag, an attacker with valid credentials can authenticate without providing the required verification code.

## Attack scenario
1. Attacker obtains valid username and password through credential stuffing, phishing, or data breach
2. Attacker initiates login attempt and reaches MFA verification page
3. Attacker enters arbitrary values in MFA challenge field to trigger POST request to auth.grammarly.com/v3/api/login
4. Attacker intercepts request using Burp Suite or similar proxy tool
5. Attacker modifies JSON payload: changes mode from 'sms' to 'email' and sets secureLogin from true to false
6. Attacker forwards modified request and gains authenticated access without valid MFA proof

## Root cause
Server-side validation fails to enforce MFA completion state and does not properly verify that the authentication mode and device trust flags match the initial MFA challenge issued. Client-controlled parameters are trusted without server-side state validation, allowing attackers to downgrade security controls mid-authentication flow.

## Attacker mindset
An attacker with compromised credentials seeks to bypass additional security controls to gain account access. The low barrier to entry (simple parameter modification) combined with high impact makes this an attractive attack vector. The attacker assumes the application trusts client-supplied MFA mode parameters without proper backend verification.

## Defensive takeaways
- Implement strict server-side state machine for authentication flow - validate that mode parameter matches the originally initiated MFA challenge
- Never trust client-supplied security control parameters; maintain authoritative MFA state on server only
- Validate complete MFA proof-of-possession before allowing mode switching or security control modifications
- Implement rate limiting and anomaly detection for parameter mutations during authentication
- Ensure secureLogin and device trust flags are cryptographically signed or embedded in secure session tokens that cannot be modified by client
- Log and alert on suspicious authentication parameter changes that deviate from normal user patterns
- Conduct security review of all authentication endpoints to identify similar parameter injection vulnerabilities

## Variant hunting
Check for similar mode-switching vulnerabilities in other MFA implementations (TOTP, push notifications, hardware keys)
Test whether device trust expiration can be manipulated via client parameters
Examine if other security flags (e.g., riskLevel, requiresStepUp, deviceVerified) can be client-controlled
Test parameter fuzzing on adjacent endpoints (/v3/api/auth, /v3/api/verify, /v3/api/mfa/*)
Investigate if JWT tokens or session cookies are generated before complete MFA verification
Check if successful MFA bypass in 'email' mode is treated differently than other modes on backend

## MITRE ATT&CK
- T1110.004
- T1078.001
- T1556.006

## Notes
This is a critical authentication bypass with straightforward exploitation requiring only credential access and HTTP interception capabilities. The vulnerability indicates insufficient separation between client presentation logic and server authentication state management. The fact that mode switching is allowed mid-authentication suggests the backend may be processing requests without validating the complete authentication session state.

## Full report
<details><summary>Expand</summary>

**Summary:**
It is possible bypass MFA without the need to have the phone code.

**Description:** 
When we turn on the MFA and we have the user and password of the user, it is possible bypass the MFA only changing some values the endpoint POST `auth.grammarly.com//v3/api/login`

## Steps To Reproduce:
Note: 
- Use burp suite or another tool to intercept the requests

  1. Turn on and configure your MFA
  2. Login with your email and password
  3. The page of MFA is going to appear
  4. Enter any random number
  5. when you press the button "sign in securely" intercept the request POST `auth.grammarly.com/v3/api/login` and in the POST message change the fields:
- `"mode":"sms"` by `"mode":"email"`
-  `"secureLogin":true` by `"secureLogin":false`
 6. send the modification and check, you are in your account! It was not necessary to enter the phone code.

## Impact

The attacker can bypass the experimental MFA, If the attacker has the email and password, the attacker can login in the account without the need of the phone code.

</details>

---
*Analysed by Claude on 2026-05-24*
