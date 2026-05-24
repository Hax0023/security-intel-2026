# Unauthorized Access to PII and Mass Account Takeover via Sequential ID Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 1061736 | https://hackerone.com/reports/1061736
- **Submitted:** 2020-12-18
- **Reporter:** takester
- **Program:** Unknown (Redacted)
- **Bounty:** Unknown (Report number: 1061736)
- **Severity:** Critical
- **Vuln:** Broken Object Level Authorization (BOLA), Insecure Direct Object Reference (IDOR), Information Disclosure, Weak Password Reset Mechanism, Account Takeover, Insufficient Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical IDOR vulnerability exposed an endpoint that disclosed Personally Identifiable Information (PII) including names, mobile numbers, and email addresses without proper authorization checks. The vulnerability could be exploited by enumerating sequential IDs to obtain credentials for password reset flows, allowing attackers to perform mass account takeovers using a static PIN combined with leaked email addresses.

## Attack scenario
1. Attacker discovers endpoint pattern at /api/user/[ID] or similar sequential identifier
2. Attacker enumerates IDs by incrementing/decrementing numbers to harvest PII (first name, last name, email, phone) for multiple users
3. Attacker navigates to forgot password functionality and enters harvested email address
4. Attacker is prompted for email and PIN verification; PIN is discoverable as static/hardcoded value exposed at same endpoint
5. Attacker enters correct PIN (leaked via endpoint) and gains access to password reset form
6. Attacker resets target account password and gains full account access; process repeats for all enumerated users

## Root cause
Multiple security failures: (1) Missing authorization checks on user detail endpoint allowing IDOR via sequential ID manipulation, (2) PII exposed without authentication/authorization, (3) Password reset mechanism accepts static/hardcoded PIN without proper validation, (4) No rate limiting on password reset attempts, (5) Insufficient randomization of reset tokens/PINs

## Attacker mindset
Opportunistic credential harvester leveraging low-effort, high-impact vulnerability chain. Attacker recognizes that sequential IDs combined with static PIN creates trivial automation path for mass account compromise. Focus is on scale and bulk account takeover rather than targeted attacks.

## Defensive takeaways
- Implement proper authorization checks on all endpoints; verify user owns requested resource before returning PII
- Replace sequential IDs with cryptographically random, non-guessable identifiers (UUIDs, GUIDs)
- Never expose PII in unauthenticated endpoints; segregate sensitive data access
- Generate cryptographically random PINs/tokens for password reset flows; avoid hardcoded or static values
- Implement rate limiting and throttling on password reset endpoints
- Add CAPTCHA or multi-factor challenges to password reset flows
- Use one-time-use, time-limited tokens for password reset (typically 15-30 minutes)
- Log and monitor password reset attempts for anomalous patterns
- Implement email verification and secondary confirmation steps
- Add step-up authentication or additional proof-of-identity requirements for sensitive operations

## Variant hunting
Test all endpoints accepting numeric/sequential parameters for IDOR vulnerabilities
Enumerate user IDs across authentication, profile, settings, payment, and preference endpoints
Check password reset, account recovery, and forgot username flows for weak token generation
Search for other endpoints exposing PII without authorization (profile, directory, search, export)
Test for bypassable PIN/OTP mechanisms using static values, low entropy, or predictable patterns
Verify authorization on export, download, and bulk data retrieval functions
Check social features (followers, friends, groups) for IDOR via user ID enumeration
Test API endpoints for information disclosure; mobile apps often expose unauthenticated APIs
Fuzz endpoints for alternative parameter names (userID, user_id, uid, id, email_id, account_id)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate system for finding exposed resources
- T1526.001 - Automated Exfiltration via enumeration
- T1040 - Traffic Capture/Sniffing (if credentials sent unencrypted)
- T1556 - Modify Authentication Process
- T1555 - Credentials from password manager/stored data
- T1589.002 - Gather Victim Identity Information - Email Addresses
- T1589.001 - Gather Victim Identity Information - Credentials
- T1136.003 - Create Account (via compromised reset)

## Notes
Report demonstrates classic IDOR chain leading to account takeover. Redacted nature of report suggests responsible disclosure. Key weakness is combining multiple authorization failures: (1) leaking PII, (2) static/discoverable reset PIN, (3) sequential ID enumeration. This is foundational vulnerability class affecting numerous platforms. Severity amplified by mass account takeover capability and ease of exploitation (no advanced techniques required).

## Full report
<details><summary>Expand</summary>

Hi, I hope you doing well
I found a critical endpoint which disclosed the personal information which can use to takeover any account present on https://██████████
#Steps:
1. Visit the link https://www.████████/███████    you will get my details,  including first name and last name, mobile number and email_address related to the account.
2. Go to the forgot password link present at https://www.███████/ click on it.
3. Enter the mail address later you will be taken to another page which will ask you to enter mail address and pin
4. After entering mail address enter the pin as "████" as █████████ is at the endpoint.
5. It will validate and will ask you to change the password of that account.

###Note:  To get email list and pin list just decrease the number at the endpoint 
for example https://www.████████/███will give you another mail_address and pin will be ██████████

## Impact

An attacker can able to takeover any account that is present on that side.

</details>

---
*Analysed by Claude on 2026-05-24*
