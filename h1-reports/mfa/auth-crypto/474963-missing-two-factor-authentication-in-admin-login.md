# Missing Two Factor Authentication in /admin/login

## Metadata
- **Source:** HackerOne
- **Report:** 474963 | https://hackerone.com/reports/474963
- **Submitted:** 2019-01-05
- **Reporter:** notexist
- **Program:** cfptime.org
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Missing Multi-Factor Authentication, Weak Authentication, Brute Force Vulnerability
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The administrative login endpoint at /admin/login lacks Two Factor Authentication (2FA), leaving the sensitive admin panel vulnerable to brute force and password guessing attacks. The Django-based application exposes a critical entry point without secondary authentication controls that should protect administrative access.

## Attack scenario
1. Attacker identifies the admin login endpoint at https://www.cfptime.org/admin/login
2. Attacker performs automated brute force attack against known/leaked admin usernames
3. Without 2FA, attacker gains unauthorized access with correct password credentials
4. Attacker obtains full administrative control of the web application
5. Attacker modifies application content, exfiltrates user data, or deploys malicious code
6. Legitimate website owner has no notification of compromised account until damage is detected

## Root cause
Administrative authentication mechanism relies solely on username/password credentials without implementing additional verification factors (email confirmation, TOTP tokens, hardware keys, or SMS codes)

## Attacker mindset
Attackers prioritize admin panels as high-value targets due to elevated privileges. 2FA absence makes credential-based attacks significantly more attractive than sites with 2FA enabled. Opportunistic actors perform password spray and dictionary attacks against admin endpoints.

## Defensive takeaways
- Implement mandatory 2FA for all administrative accounts using TOTP (Time-based One-Time Password) or similar mechanisms
- Use established Django packages like django-otp with qrcode for seamless 2FA integration
- Enforce 2FA before granting any admin panel access, regardless of password strength
- Implement rate limiting and account lockout mechanisms on admin login endpoints
- Monitor and alert on failed login attempts exceeding baseline thresholds
- Segregate admin access to VPN/IP whitelist when possible
- Require strong password policies in conjunction with 2FA
- Enable audit logging for all authentication events on administrative functions

## Variant hunting
Check other admin endpoints (/administrator, /management, /dashboard) for 2FA absence
Verify if API authentication endpoints lack 2FA protections
Test if 2FA can be bypassed via session hijacking or token prediction
Identify if backup authentication methods (password reset) circumvent 2FA
Audit if 2FA is optional rather than mandatory for admin accounts
Check Django admin panel (/admin/) directly for 2FA configuration
Test for 2FA recovery code vulnerabilities if implemented

## MITRE ATT&CK
- T1110 - Brute Force
- T1110.001 - Brute Force: Password Guessing
- T1110.004 - Brute Force: Credential Stuffing
- T1078.001 - Valid Accounts: Default Accounts
- T1556 - Modify Authentication Process

## Notes
This report is framed as a 'suggested security improvement' rather than a critical vulnerability, indicating responsible disclosure approach. The researcher provides constructive recommendations with specific Python packages (django-otp, qrcode). However, the lack of demonstrated exploitation and bounty amount not being specified suggests this may have been a low-severity report or policy-based finding. The root cause is architectural rather than implementation-level, requiring refactoring of authentication flow.

## Full report
<details><summary>Expand</summary>

Hello Team,
>First of all this report is just mainly concern for `Suggested security improvements` based on your policy page.
>If and only if not mean possible, please do let me know. Thanks!

#### INTRODUCTION
Administrative panel is one of the main entry point for the website owner to manage their web apps from outside, making it expose not only to website owner but to public as well.

#### DESCRIPTION
It have found out that `https://www.cfptime.org/` has an endpoint of `admin/login`  which was a written django web application python framework (i should say based on the login page UI). 

Though the web application looks okay, i do suggests that you'll need to setup an additional Two Factor Authentication on the login page to ensure that only the website owner can access the site internally and nothing else.

#### RECOMMENDATIONS

>###Things To Look For
> - Suggested security improvements

I highly recommend to install 2FA from the following modules in python `django-otp`,`qrcode` which uses otp token for verification since csrf token are mean to use only on public, while otp can only be received by the website owner itself only.

#### REFERENCES
Finally the references i used for this report, you might consider checking this also for even more ways to fortify your web application.
https://hackernoon.com/5-ways-to-make-django-admin-safer-eb7753698ac8

## Impact

Prone to password guessing attacks/brute force attacks.

</details>

---
*Analysed by Claude on 2026-05-24*
