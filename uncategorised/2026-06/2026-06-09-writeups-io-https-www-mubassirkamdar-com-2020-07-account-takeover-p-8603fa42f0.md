# Account Takeover via Open Redirect in Password Reset Flow

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Private Bug Bounty Program (Undisclosed)
- **Bounty:** Unknown - Pending at time of writing
- **Severity:** Critical
- **Vuln types:** Open Redirect, Account Takeover, Insufficient URL Validation, Password Reset Token Exposure
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered a critical account takeover vulnerability in a password reset endpoint that failed to properly validate the resetPasswordUrl parameter. By injecting a malicious domain, the researcher received password reset tokens on their attacker-controlled server, enabling full account takeover of any user account.

## Attack scenario (step by step)
1. Attacker initiates password reset on target application via legitimate account or victim email
2. Intercepts password reset request containing resetPasswordUrl=http://target.com parameter
3. Modifies resetPasswordUrl parameter to attacker-controlled domain (http://attacker.com)
4. Application generates password reset token and sends email with token URL pointing to attacker domain
5. Attacker receives reset email with valid password reset token in URL
6. Attacker uses token to reset victim account password and gain full account access

## Root cause
The application implements an open redirect vulnerability in the password reset functionality by accepting and processing user-controlled URLs in the resetPasswordUrl parameter without proper validation or whitelisting. The endpoint fails to verify that the reset URL belongs to the legitimate application domain before embedding it in the password reset token email.

## Attacker mindset
Methodical reconnaissance-driven approach: researcher thoroughly enumerated application functionality before focusing on high-value features like account recovery. Persistence despite initial failures with CSRF/IDOR, pivot to suspicious parameters. Recognition that reset tokens in URLs are valuable targets, understanding that email-based attacks circumvent many browser-based protections.

## Defensive takeaways
- Implement strict whitelist validation for all URL parameters - reject any domain not matching the application's authorized domains
- Never allow user-controlled URLs in password reset flows; generate reset tokens independently without URL parameters from user input
- Use server-side URL generation only - construct the complete reset URL on the backend and verify it before sending in emails
- Implement additional safeguards: short token expiration times, one-time use tokens, rate limiting on password reset endpoints
- Apply defense-in-depth: CSRF tokens on password reset forms, challenge emails for account recovery, and email verification before processing reset
- Regular security audits of authentication-related endpoints given their critical nature
- Log and monitor password reset activity for anomalies

## Variant hunting
['Check all password reset variants: email-based, SMS-based, security questions - do they share similar URL validation flaws?', 'Test other account recovery functions: account unlock, email change, phone number change flows for open redirects', 'Investigate if similar resetPasswordUrl or callback parameters exist in other endpoints (OAuth flows, webhooks, notifications)', 'Check for parameter pollution attacks combining resetPasswordUrl with other parameters', 'Test if Host header injection or X-Forwarded-Host can bypass URL validation as fallback', 'Examine if application uses relative URLs that could be exploited with path traversal']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link (attacker receives legitimate reset token)
- T1056 - Input Capture (token interception)
- T1078 - Valid Accounts (account takeover post-exploitation)
- T1021 - Remote Services (lateral movement after account takeover)

## Notes
This is a classic and devastating vulnerability pattern in authentication flows. The researcher's methodology of thoroughly mapping application functionality before vulnerability hunting increased effectiveness. The writeup lacks specific technical details about email content validation and whether the application verified URL ownership. The pending bounty status at publication suggests potential acceptance given criticality. Similar patterns appear in many OAuth implementations and third-party authentication flows.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
