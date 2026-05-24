# No Rate Limiting on Password Reset Endpoint Leading to Email Spam and Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 862681 | https://hackerone.com/reports/862681
- **Submitted:** 2020-04-29
- **Reporter:** nagli
- **Program:** Undisclosed (HackerOne Report #862681)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Missing Rate Limiting, Email Bomb/Spam, Denial of Service, Predictable Password Reset Token
- **CVEs:** None
- **Category:** uncategorised

## Summary
The password reset endpoint at /accounts/password/reset/ lacks rate limiting, allowing attackers to send unlimited password reset emails to a victim's address. Additionally, the password reset link remains static across requests, enabling email bombardment and potential spear-phishing attacks against target users.

## Attack scenario
1. Attacker identifies target user email address
2. Attacker navigates to password reset endpoint and captures the request in Burp Suite
3. Attacker sends request to Intruder with null payloads to bypass any basic controls
4. Attacker launches rapid-fire requests to generate hundreds of password reset emails
5. Victim's email inbox is flooded with reset emails, causing denial of service to legitimate communication
6. Attacker could inject malicious reset links or phishing content within legitimate-appearing reset emails

## Root cause
The application failed to implement rate limiting controls on the password reset endpoint. No throttling mechanism restricts the number of reset requests per user, IP address, or time window. Additionally, the static nature of reset tokens/links across requests eliminates the requirement for attackers to wait for token generation or track changing identifiers.

## Attacker mindset
An attacker with low technical skill can exploit this vulnerability to conduct spam campaigns, inbox denial of service attacks, or spear-phishing campaigns against known users. The ease of exploitation makes this attractive for mass harassment or targeted attacks against specific individuals.

## Defensive takeaways
- Implement strict rate limiting on password reset endpoints (e.g., 1 request per 5-15 minutes per email/IP)
- Generate unique, cryptographically random reset tokens for each request with short TTL (15-30 minutes)
- Add CAPTCHA or similar challenge-response after 2-3 failed/repeated requests
- Monitor and log password reset request patterns to detect abuse
- Implement exponential backoff or temporary account lockout after threshold of reset requests
- Consider requiring additional authentication (security questions, OTP) before sending reset email
- Add rate limiting at multiple layers (application, WAF, load balancer)

## Variant hunting
Check other authentication endpoints for rate limiting (login, registration, account recovery)
Test if rate limiting exists on SMS/2FA delivery endpoints
Verify if rate limiting applies to different user agents or spoofed IPs
Check for token randomization on other sensitive operations (email verification, account unlock)
Test rate limiting bypass via header manipulation (X-Forwarded-For, X-Client-IP)
Attempt to bypass rate limiting using distributed requests across different IPs/VPNs

## MITRE ATT&CK
- T1110 - Brute Force
- T1190 - Exploit Public-Facing Application
- T1499 - Endpoint Denial of Service
- T1598 - Phishing for Information
- T1566 - Phishing

## Notes
This is a classic missing rate limiting vulnerability on a high-value endpoint. The combination of no rate limiting plus predictable/static tokens creates a compound risk. Similar vulnerabilities were previously reported (762122, 791498, 441161), suggesting this is a common misconfiguration. The impact extends beyond DoS to include spear-phishing and email infrastructure abuse. Severity is Medium rather than High because it requires prior knowledge of target email address and causes indirect harm (email spam) rather than direct data breach.

## Full report
<details><summary>Expand</summary>

**Summary:**

No-Rate Limit on Password reset endpoint results mail-spam functionality to be abused.
Additionally, the password-reset link remain the same after each request.

**Description:**

Malicious user could Spear-target █████████ user mail and Spam it for as many requests as he would like.


Possible scenarios:
Attacker could use this vulnerability to bomb out the email inbox of the victim.
Attacker could send Spear-Phishing to the selected mail address.
Attacker might cause denial of service to the mail servers.

## Step-by-step Reproduction Instructions

1. Go to https://█████/█████/accounts/password/reset/
2.  Click on "Send Email" and Capture the request on burp.
3. Send to intruder, and start Sniping attack with NULL payloads.


## Suggested Mitigation/Remediation Actions
1. Limiting the password reset request to once every X minutes.
2. Use CAPTCHA verification after X requests.
3. Asserting random password-reset link for each request.

Similar reports:
https://hackerone.com/reports/764122
https://hackerone.com/reports/791498
https://hackerone.com/reports/441161

Best Regards,

Gal Nagli

## Impact

Attacker could use this vulnerability to bomb out the email inbox of the victim.
Attacker could send Spear-Phishing to the selected mail address.
Attacker might cause denial of service to the mail servers.

</details>

---
*Analysed by Claude on 2026-05-24*
