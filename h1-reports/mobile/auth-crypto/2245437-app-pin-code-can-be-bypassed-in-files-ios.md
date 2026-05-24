# App PIN Code Brute Force Vulnerability in Files iOS

## Metadata
- **Source:** HackerOne
- **Report:** 2245437 | https://hackerone.com/reports/2245437
- **Submitted:** 2023-11-09
- **Reporter:** spell1
- **Program:** Files iOS
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authentication Bypass, Insufficient Rate Limiting, Weak Brute Force Protection
- **CVEs:** CVE-2023-49790
- **Category:** auth-crypto

## Summary
The Files iOS application (v4.9.1) lacks rate limiting on PIN verification attempts, allowing attackers to brute force the 4-digit PIN with unlimited tries. This authentication bypass vulnerability can lead to unauthorized access to the application and its protected data.

## Attack scenario
1. Attacker obtains or targets a device with Files iOS app installed
2. Attacker opens the application and encounters PIN prompt
3. Attacker begins systematically entering PIN combinations starting from 0000
4. Application accepts unlimited consecutive failed attempts without delay or lockout
5. Attacker programmatically automates PIN entry across all 10,000 possible combinations
6. Attacker gains application access once correct PIN (typically 4 digits) is discovered

## Root cause
The application fails to implement rate limiting, account lockout mechanisms, or progressive delays after failed PIN authentication attempts. The authentication logic validates PINs without enforcing any temporal or attempt-based restrictions.

## Attacker mindset
An attacker recognizes that 4-digit PINs offer only 10,000 possible combinations and, without rate limiting, can be exhaustively tested in minutes. The attacker assumes the app lacks standard security controls and attempts brute force as a quick bypass method.

## Defensive takeaways
- Implement exponential backoff delays after each failed PIN attempt
- Enforce account lockout after N consecutive failed attempts (e.g., 5-10 tries)
- Add progressive time delays between attempts (1s, 2s, 4s, etc.)
- Consider biometric authentication (Face ID/Touch ID) as primary mechanism with PIN as fallback
- Log failed authentication attempts for security monitoring
- Implement CAPTCHA or additional verification after threshold failures
- Consider server-side PIN validation with rate limiting if feasible
- Increase minimum PIN length or complexity requirements

## Variant hunting
Check for similar brute force vulnerabilities in other authentication mechanisms (password reset, recovery codes)
Test security questions or recovery methods for rate limiting bypasses
Verify biometric bypass mechanisms don't redirect to unprotected PIN verification
Inspect API endpoints for rate limiting on authentication requests
Test for timing attack vulnerabilities in PIN comparison logic
Check if failed attempts reset after app backgrounding/relaunch
Test keychain/stored credential access for unprotected secrets

## MITRE ATT&CK
- T1110.001 - Brute Force: Password Guessing
- T1110.004 - Brute Force: Credential Stuffing
- T1021.004 - Remote Services: SSH/Shell

## Notes
This is a straightforward but critical vulnerability in mobile application security. The 4-digit PIN entropy is inherently low (only 10,000 combinations), making rate limiting absolutely essential. The report includes a PoC attachment (F2844276) but content is not fully detailed in the excerpt. The vulnerability affects authentication integrity and confidentiality of protected data within the Files app.

## Full report
<details><summary>Expand</summary>

Hi Team,

Hope you are doing great.

Note: IoS APP Vs.: 4.9.1

I got a vulnerability in your applications via which an attacker is able to bypass the PIN.
The attacker just need to bruteforce the 4 digit PIN as unlimited tries is accepted by the application, the attacker can simply do a bruteforce and access the application.

PoC:
{F2844276}

## Impact

Authentication Bypass leading to application access

</details>

---
*Analysed by Claude on 2026-05-24*
