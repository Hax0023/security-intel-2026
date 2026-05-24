# Unauthorized Account Access via Leaked Credentials in URL Format (Account Takeover)

## Metadata
- **Source:** HackerOne
- **Report:** 3080597 | https://hackerone.com/reports/3080597
- **Submitted:** 2025-04-07
- **Reporter:** firec4t
- **Program:** Khan Academy
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Credential Exposure, Account Takeover, Broken Authentication, Insufficient Authentication Controls
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Attackers can perform complete account takeover on Khan Academy by using credentials (email and password) exposed in cleartext on VirusTotal and other public sources. The platform lacks secondary verification mechanisms or alerts when compromised credentials are used to authenticate. This allows unauthorized access to user accounts, personal learning data, messages, and linked services.

## Attack scenario
1. Attacker discovers Khan Academy user credentials exposed on VirusTotal or similar credential leak databases
2. Attacker navigates to Khan Academy login page and enters the leaked email address
3. Attacker enters the corresponding password from the leaked credential set
4. System authenticates the attacker without requiring multi-factor authentication
5. Attacker gains full account access without any notification to the legitimate user
6. Attacker exfiltrates personal data, learning progress, messages, or pivots to linked external accounts

## Root cause
Khan Academy relies solely on password-based authentication without mandatory multi-factor authentication (MFA/2FA), allowing attackers with leaked credentials to bypass all security controls. No detection mechanisms alert users when accounts are accessed from unusual locations or devices.

## Attacker mindset
Opportunistic threat actor leveraging publicly available leaked credentials from breach databases to perform mass account takeovers with minimal technical effort. The attacker seeks to gain access to personal data, learning accounts, and potentially linked services for financial gain, identity theft, or malicious activity.

## Defensive takeaways
- Implement mandatory two-factor authentication (2FA) for all users or at minimum high-risk accounts
- Deploy credential exposure monitoring to detect when user credentials appear in public breach databases and force password resets
- Implement behavioral analysis to detect anomalous login attempts (unusual geographic locations, device fingerprints, time-of-day patterns)
- Send security alerts to users whenever account access occurs from new devices or locations
- Enforce strong password policies and require regular password changes for exposed credentials
- Monitor VirusTotal and similar services for exposed credentials belonging to your platform
- Implement account lockout mechanisms after multiple failed authentication attempts
- Use CAPTCHA or rate limiting on login endpoints to prevent credential stuffing attacks

## Variant hunting
Check for similar credential exposure in alternative leak databases (Have I Been Pwned, Dehashed, etc.)
Test whether other authentication endpoints (API login, OAuth endpoints) have the same vulnerability
Verify if compromised credentials work across linked Khan Academy services or partner integrations
Search for credentials in GitHub, Pastebin, and other code-sharing platforms that might expose Khan Academy user data
Test if account recovery mechanisms (password reset, email verification) have similar bypasses
Investigate whether leaked credentials are being actively exploited in the wild or sold on dark web markets

## MITRE ATT&CK
- T1110 - Brute Force
- T1110.004 - Credential Stuffing
- T1187 - Forced Phishing
- T1556 - Modify Authentication Process
- T1078 - Valid Accounts
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information

## Notes
This is a resubmission of a previously reported similar issue (Report #2981324). The reporter explicitly identifies that credentials are archived in cleartext in URL format and accessible via public sources. The vulnerability represents a complete authentication bypass for any account with exposed credentials. The presence of prior reports on the same vulnerability suggests potential remediation delay or inadequate response from the vendor. Critical priority should be given to implementing MFA and credential exposure monitoring immediately.

## Full report
<details><summary>Expand</summary>

I discovered a critical vulnerability that allows attackers to access user accounts on khanAcademy.com using credentials publicly available on VirusTotal., an attacker can directly authenticate into a user’s account without any secondary verification or alert to the user.
i have reported a similar issue , here's the report ( 2981324 ) 

this time the email and password of the victim is archived in clear text ( https://en.khanacademy.org/login,██████,,█████████,,,█████████,██████████,Personal )

by entering the mail ( ██████████ ) and password ( ███████ ) in the login , the attacker can easily perform account takeover

Please Enforce 2FA: Make two-factor authentication mandatory, especially for accounts with detected exposure.

## Impact

Full account takeover: Unauthorized access to user accounts with no user awareness.

Exposure of personal data: Private information such as learning progress, messages, and linked accounts may be compromised.

Potential financial or reputational damage: If linked to other services, this access may lead to wider exploitation.

</details>

---
*Analysed by Claude on 2026-05-24*
