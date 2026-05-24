# 2FA Bypass via Brute Force on Password Reset Page

## Metadata
- **Source:** HackerOne
- **Report:** 121696 | https://hackerone.com/reports/121696
- **Submitted:** 2016-03-09
- **Reporter:** kamikaze
- **Program:** Slack
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Broken Authentication, Insufficient Rate Limiting, Weak Brute Force Protection
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The password reset functionality in Slack did not implement rate limiting or account lockout mechanisms on 2FA code verification attempts. An attacker who gains access to a victim's email could brute force the 2FA code during password reset to completely compromise accounts with 2FA enabled, completely bypassing the second authentication factor.

## Attack scenario
1. Attacker compromises victim's email account through phishing, credential stuffing, or other means
2. Attacker initiates password reset on victim's Slack account using compromised email
3. Victim receives password reset link in email; attacker accesses email and clicks link
4. On password reset page, attacker sets a new password and is prompted for 2FA code
5. Attacker systematically submits 2FA codes (likely 6-digit TOTP, max 1,000,000 combinations) without rate limiting
6. After multiple failed attempts (researcher tested 20+ attempts), attacker successfully resets password and gains full account access

## Root cause
The application failed to implement rate limiting, exponential backoff, or temporary account lockout mechanisms on the 2FA verification endpoint during password reset flows. The 2FA protection was effectively optional rather than enforced as a mandatory security control.

## Attacker mindset
An attacker who has compromised a user's email would recognize that 2FA during password reset is the final barrier to account takeover. They would attempt to bypass it through brute force, knowing that successful exploitation grants complete account access without triggering additional alerts (since the victim's email is already compromised).

## Defensive takeaways
- Implement strict rate limiting on 2FA verification attempts (max 3-5 attempts per time window)
- Enforce progressive delays or exponential backoff after failed attempts (e.g., 30s, 5min, 24h lockout)
- Temporarily lock accounts or require alternative verification after repeated failed 2FA attempts
- Log and alert on suspicious 2FA verification patterns during password reset
- Consider requiring email verification or out-of-band confirmation before allowing password reset
- Implement CAPTCHA or similar bot detection after a few failed attempts
- Send notification to registered email/phone about password reset and 2FA attempts

## Variant hunting
Check if other authentication flows (login, account recovery, sensitive actions) lack 2FA brute force protections
Test if backup codes have similar brute force protection gaps
Verify if device registration/trust flows are also vulnerable
Examine if SMS/email one-time codes (as 2FA alternatives) have rate limiting
Test concurrent brute force attempts from multiple IPs/sessions
Check if 2FA bypass exists in other password reset scenarios (e.g., admin-initiated resets)

## MITRE ATT&CK
- T1110.001
- T1078.001
- T1621
- T1556

## Notes
This is a critical authentication bypass with high real-world impact. The researcher responsibly noted the automated testing exclusion in Slack's policy and performed manual testing instead. The vulnerability becomes critical when combined with email compromise, as the second factor (2FA) becomes worthless. The fix is straightforward but crucial for account security posture.

## Full report
<details><summary>Expand</summary>

If a user set 2FA, a user has to enter verification code when a user tries to reset password. 

Under the "Password Reset" page, a user can enter wrong two-factor authentication code many times. I said "many times" because your bug bounty policy stated...

Exclusions

Issues found through automated testing

So, I may not be allowed to brute force in order to check how many times a user can enter wrong 2FA codes. I didn't use any automated tools and didn't brute force for my testing.

I tested that I could still reset my password after I entered wrong 2FA codes 20 times manually. It seems that a user can brute force 2FA codes.

-----step to reproduce-----

1. A user sends a password reset message to user's registered email.

2. Go to "Password Reset" page from #1's message.

3. Set a new password and Brute force two-factor auth code

----------------------------------

After a user reset password, a user will go to slack's home page. From that page a user can do anything. 

Two factor authentication is another layer of protection. Even if a user leaked email address and password, a user will be protected by additional security(2FA). 

If an attacker hacked victim's email, an attacker will be able to take over slack's 2FA enabled account by brute forcing 2FA code on password reset page.

Recommendation: If a user entered wrong 2FA codes many times, a user will be blocked temporary.


</details>

---
*Analysed by Claude on 2026-05-24*
