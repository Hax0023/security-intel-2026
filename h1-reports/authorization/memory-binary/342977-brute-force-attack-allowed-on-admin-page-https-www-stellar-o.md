# Brute Force Attack on WordPress Admin Login Page

## Metadata
- **Source:** HackerOne
- **Report:** 342977 | https://hackerone.com/reports/342977
- **Submitted:** 2018-04-25
- **Reporter:** abo-jehad
- **Program:** Stellar.org
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Brute Force Attack, Insufficient Rate Limiting, Missing Account Lockout Mechanism, Weak Authentication Controls
- **CVEs:** None
- **Category:** memory-binary

## Summary
The WordPress admin login page (wp-admin/) at stellar.org lacks rate limiting and account lockout protections, allowing attackers to perform automated brute force attacks to enumerate and compromise administrator credentials. An attacker can use tools like Burp Suite Intruder to systematically test password combinations without server-side restrictions, leading to unauthorized administrative access.

## Attack scenario
1. Attacker identifies the WordPress admin login endpoint at /wp-admin/
2. Attacker intercepts login request using Burp Suite or similar proxy tool
3. Attacker configures automated brute force attack using Intruder with common password lists
4. Server fails to rate-limit or block repeated failed authentication attempts
5. Attacker achieves valid credentials after multiple iterations
6. Attacker gains unauthorized administrative access to WordPress dashboard

## Root cause
The WordPress installation does not implement server-side protections against brute force attacks, including: lack of rate limiting on login attempts, no progressive delays between failed attempts, missing account lockout after threshold of failed attempts, and absence of CAPTCHA or multi-factor authentication (MFA) on the admin login page.

## Attacker mindset
An attacker would target this vulnerability as a low-effort entry point to compromise the entire website. WordPress admin access provides complete control over content, users, plugins, and themes. The attacker exploits the predictable nature of human-generated passwords and the absence of defensive controls, automating the attack for rapid credential discovery.

## Defensive takeaways
- Implement rate limiting and throttling on login endpoints to restrict attempt frequency (e.g., max 5 attempts per 15 minutes)
- Deploy progressive delays/exponential backoff that increases wait time after each failed attempt
- Implement account lockout mechanism after configurable threshold of failed attempts (e.g., 5 failures = 30 min lockout)
- Enable CAPTCHA or reCAPTCHA on login form to prevent automated attacks
- Implement and enforce strong password policies (minimum length 12+ characters, complexity requirements)
- Deploy multi-factor authentication (MFA/2FA) on admin accounts as mandatory security control
- Monitor and log all failed authentication attempts for security alerting
- Use WordPress security plugins (e.g., Wordfence, iThemes Security) with brute force protection
- Restrict admin login access by IP whitelist if feasible
- Rename or hide wp-admin location using security plugins

## Variant hunting
Test other authentication endpoints for similar brute force vulnerabilities (password reset, user registration)
Check for timing-based user enumeration attacks that reveal valid usernames
Verify if default/weak administrator usernames (admin, administrator) exist and are guessable
Test for credential stuffing attacks using leaked password databases
Assess if API authentication endpoints lack similar protections
Check for authentication bypass vulnerabilities in related functionality
Test for session management weaknesses allowing account takeover
Verify if backup/alternative login methods exist without proper protections

## MITRE ATT&CK
- T1110.001
- T1110.003
- T1586.003
- T1078.001

## Notes
This is a common and high-impact WordPress vulnerability. The proof-of-concept demonstrates successful attack execution with only 9 attempts. Real-world exploitation would use larger password lists (rockyou.txt, etc.) against common admin usernames. The lack of any defensive mechanism suggests the target site did not implement standard WordPress hardening practices. This vulnerability is easily exploitable and should be remediated immediately as it provides direct pathway to full website compromise.

## Full report
<details><summary>Expand</summary>

hi security team
-due to your bug bounty program , i found basic authentication method
-by doing many trials the server will response and will not block the logging process
- the attack can be automated by burp intruder till getting access to admin page
- in second screen the request is intercepted by burp proxy
F290121:

-in third anf forth screen i used burp intruder to automate  bruit force attack (i tried only 9 times to make POC)
F290122:
F290123:

## Impact

if the attack coleted , admin page is accessed

</details>

---
*Analysed by Claude on 2026-05-24*
