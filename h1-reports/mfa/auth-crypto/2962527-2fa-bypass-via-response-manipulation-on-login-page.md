# 2FA Bypass via Response Manipulation on Login Page

## Metadata
- **Source:** HackerOne
- **Report:** 2962527 | https://hackerone.com/reports/2962527
- **Submitted:** 2025-01-28
- **Reporter:** mikelly
- **Program:** HackerOne (Private Program)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Insecure Direct Object References (IDOR), Client-Side Authentication Bypass, Broken Authentication, Insufficient Server-Side Verification, Response Manipulation
- **CVEs:** CVE-2021-30120
- **Category:** auth-crypto

## Summary
A critical vulnerability in the 2FA mechanism allows attackers to bypass OTP verification by intercepting and manipulating the server response. By modifying the status field from 3 (incorrect code) to 1 (correct code), an attacker with valid credentials can gain unauthorized account access without entering the correct 2FA code. This flaw completely nullifies the security benefit of two-factor authentication.

## Attack scenario
1. Attacker obtains valid user credentials through phishing, credential stuffing, or data breaches
2. Attacker logs in to the target account with the compromised email and password
3. Server sends 6-digit OTP code to user's email address and prompts for verification
4. Attacker intentionally submits an incorrect 2FA code and intercepts the HTTP response using a proxy tool (Burp Suite, etc.)
5. Attacker modifies the response body, changing the status field from '3' (incorrect OTP) to '1' (correct OTP)
6. Attacker forwards the manipulated response, and the application grants full account access without verifying the actual OTP

## Root cause
The application performs 2FA validation logic on the client-side or fails to enforce proper server-side verification. The authentication decision is derived from response values that can be manipulated by the attacker rather than from a server-side authoritative check. The server accepts the client's assertion of successful OTP verification without re-validating the actual OTP code.

## Attacker mindset
An attacker with modest technical skills can exploit this vulnerability using common proxy tools. The attack requires only valid credentials and the ability to intercept/modify HTTP responses. The low technical barrier combined with high impact (complete account takeover) makes this highly attractive for account compromise campaigns.

## Defensive takeaways
- Never rely on client-controlled response values for authentication decisions; always validate security-critical operations server-side
- Implement strict server-side OTP verification that must be passed before granting session tokens or access
- Use HTTP-only, Secure cookies for session management to prevent client-side manipulation of authentication state
- Implement rate limiting and account lockout mechanisms after multiple failed OTP attempts
- Add server-side logging and anomaly detection for repeated failed 2FA attempts
- Conduct security reviews of all authentication flows to identify client-side trust dependencies
- Implement proper separation of concerns: cryptographic verification must happen server-side with no client override capability
- Use signed/encrypted tokens or server-side session stores to prevent tampering with authentication state

## Variant hunting
Look for similar vulnerabilities in: password reset flows accepting client-supplied verification status, email confirmation mechanisms, identity verification processes, step-up authentication for sensitive operations, and any multi-step authentication where intermediate responses indicate success/failure. Check for other status codes or fields that may influence access control decisions.

## MITRE ATT&CK
- T1110.001
- T1190
- T1552.007
- T1621
- T1199

## Notes
This is a design-level flaw rather than a minor implementation bug. The vulnerability suggests fundamental misunderstanding of security boundaries between client and server. The reference to CVE-2021-30120 and similar HackerOne report #1943252 suggests this may be a recurring pattern in the target's codebase. Immediate remediation required as this completely negates 2FA protection.

## Full report
<details><summary>Expand</summary>

**Description:**
I discovered a vulnerability in the Two-Factor Authentication (2FA) mechanism of your website, stemming from an insecure design flaw. The issue arises from the way the system handles 2FA verification. Specifically, the verification process can be bypassed by intercepting and manipulating the server's response. As a result, an attacker can gain unauthorized access to an account after providing the correct login credentials, without the need to submit the correct 2FA code. This flaw highlights a weakness in the design of the 2FA flow, where the server fails to enforce proper security checks after the initial login phase.

## References
https://hackerone.com/reports/1943252

## Impact

This vulnerability allows an attacker with valid credentials (email and password) to completely bypass the 2FA mechanism. As a result:

1. The security benefit of 2FA is nullified.
2. Accounts are susceptible to unauthorized access if credentials are compromised through phishing, leaks, or other means.

## System Host(s)
██████████

## Affected Product(s) and Version(s)
Custom website hosted at ████████

## CVE Numbers
CVE-2021-30120

## Steps to Reproduce
1. Create an account at ████████
2. Log in using valid credentials (email and password) at ███████
3. A 6 digit 2FA code will be sent to your email, and you will be prompted to enter this 6 digit 2FA code
4. Enter a wrong 2FA code and make sure to intercept the response to this request
5. Observe that the intercepted response body will have a status of 3 that is status: 3 indicating an incorrect OTP code
6. Modify the status value from 3 (incorrect code) to 1 (indicating a correct code).
7. Forward the modified response and observe that you are now logged into the account, bypassing the 2FA process entirely.

## Suggested Mitigation/Remediation Actions
1. Ensure that 2FA verification is fully performed server-side without relying solely on client-side or response manipulation for authentication state changes.
2. Validate the OTP server-side before granting access and ensure no client-side response or manipulation can override the server's verification logic.



</details>

---
*Analysed by Claude on 2026-05-24*
