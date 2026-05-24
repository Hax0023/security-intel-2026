# 2FA Bypass via Leaked Cookies

## Metadata
- **Source:** HackerOne
- **Report:** 2479622 | https://hackerone.com/reports/2479622
- **Submitted:** 2024-04-26
- **Reporter:** deepmarketer
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Broken Authentication, Session Management Flaw, Insufficient Cookie Security, Missing Device Binding
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical vulnerability allows attackers to bypass Two-Factor Authentication by stealing and reusing valid session cookies from authenticated users. An attacker who obtains session cookies (via MitM, phishing, or malware) can impersonate the user without providing the 2FA code, completely circumventing the second authentication factor.

## Attack scenario
1. Attacker performs man-in-the-middle (MitM) attack or phishing to obtain victim's session cookies after 2FA authentication
2. Attacker exports or captures the authenticated session cookies using tools like Evilginx2 or browser interception
3. Attacker imports or injects the stolen cookies into their own browser session
4. Attacker accesses the application and is granted full account access without being challenged for 2FA
5. Attacker performs unauthorized actions including data theft, account manipulation, or fraudulent transactions
6. Victim remains unaware as session activity may not trigger additional verification or device binding checks

## Root cause
The application validates 2FA only at initial login but does not maintain continuous verification tied to session cookies. Session cookies lack device fingerprinting, IP binding, or additional re-authentication checks, allowing them to be freely transferred between devices and networks without triggering security challenges.

## Attacker mindset
An attacker recognizes that while 2FA protects the login endpoint, the resulting session tokens are treated as fully trusted without additional safeguards. By targeting the post-authentication session layer rather than the authentication mechanism itself, they can achieve account compromise with lower technical difficulty than cracking 2FA codes or exploiting the authentication logic directly.

## Defensive takeaways
- Implement device fingerprinting and binding to associate session cookies with specific devices/browsers
- Require step-up authentication (re-challenge with 2FA) when unusual device, IP, location, or user-agent is detected
- Use secure cookie flags: HttpOnly, Secure, SameSite=Strict to prevent interception and cross-site misuse
- Implement session anomaly detection and automatically invalidate suspicious sessions
- Add IP address and User-Agent validation to session cookies; invalidate sessions from mismatched values
- Consider short session lifetimes combined with secure refresh token rotation
- Log and monitor session creation from new devices and alert users of new logins
- Implement rate limiting and geographic velocity checks to detect impossible travel

## Variant hunting
Test if refresh tokens are similarly unbound and can bypass 2FA re-authentication
Check if API tokens or OAuth tokens share the same vulnerability when obtained post-2FA
Verify if remember-me or persistent login features suffer from identical device-binding gaps
Test if WebAuthn/FIDO2 sessions have comparable bypass vectors
Examine whether single sign-on (SSO) tokens inherit the vulnerability across integrated applications
Check if password reset flows similarly accept pre-2FA session cookies
Test if account recovery flows are protected against cookie-based takeover

## MITRE ATT&CK
- T1190
- T1056.004
- T1040
- T1555.003
- T1539
- T1550.001
- T1111

## Notes
This vulnerability represents a fundamental design flaw where 2FA is treated as a one-time gate rather than a continuous trust model. The severity is Critical because it completely nullifies the security benefit of 2FA for any user whose cookies are compromised. The attack is practical given widespread availability of MitM tools and cookie-stealing malware. Organizations should audit whether their session management architecture properly implements device binding and continuous verification rather than relying solely on post-authentication session tokens.

## Full report
<details><summary>Expand</summary>

**Summary:**
The discovered vulnerability allows for the bypass of Two-Factor Authentication (2FA) mechanisms through the exploitation of leaked cookies. By intercepting and utilizing these cookies, an attacker can gain unauthorized access to user accounts without the need for the second authentication factor, compromising the security of the system.

**Description:**
The discovered vulnerability allows attackers to bypass Two-Factor Authentication (2FA) mechanisms by exploiting leaked cookies, compromising the security of user accounts within the hackerone. Two-Factor Authentication is a widely adopted security measure that adds an additional layer of protection beyond passwords, typically requiring users to provide a secondary authentication factor such as a code generated by an authenticator app . The vulnerability described herein enables attackers to bypass this additional security layer through the interception and utilization of session cookies, thus gaining unauthorized access to user accounts without the need for the secondary authentication factor.

## Steps To Reproduce

1. Navigate to the account settings and enable 2FA.

2. Log out and log back in using valid credentials.

3. Enter the required 2FA code to proceed.

4.Export session cookies using a cookie editor tool.

5.Paste the copied cookies into another browser

6 Access the account  without providing the 2FA code,2FA Authentication bypassed.

### Mitigation:
 Introduce device-based Two-Factor Authentication (2FA) mechanisms that require additional verification steps when signing in from new or unrecognized devices, browsers, or locations. This adds an extra layer of security by verifying the identity of the user and the device being used for authentication.

### Supporting Material/References 
POC Attached

## Impact

The vulnerability allows attackers to bypass Two-Factor Authentication (2FA) mechanisms by stealing and utilizing session cookies obtained through various means, such as man-in-the-middle (MitM) attacks using tools like Evilginx2. By exploiting this vulnerability, attackers can gain unauthorized access to user accounts without the need for the second authentication factor, compromising the security of the system and potentially leading to unauthorized data access, fraudulent transactions, or other malicious activities.

</details>

---
*Analysed by Claude on 2026-05-24*
