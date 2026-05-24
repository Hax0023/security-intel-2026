# Authorization Bypass via Brute Force on /wp-admin Login

## Metadata
- **Source:** HackerOne
- **Report:** 788420 | https://hackerone.com/reports/788420
- **Submitted:** 2020-02-03
- **Reporter:** brumens
- **Program:** Stripo (my.stripo.email)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Brute Force Attack, Insufficient Rate Limiting, Missing Account Lockout Mechanism, Weak Authentication Controls
- **CVEs:** None
- **Category:** memory-binary

## Summary
The /wp-admin login endpoint on my.stripo.email lacks rate limiting and account lockout protections, allowing attackers to perform rapid brute force attacks against administrator credentials. An attacker can attempt thousands of password guesses within seconds without triggering any blocking mechanisms or account locks.

## Attack scenario
1. Attacker identifies the /wp-admin login endpoint at my.stripo.email
2. Attacker uses automated tools (Wfuzz, Hydra, Burp Intruder) to send rapid authentication requests with common passwords
3. Server processes all requests without rate limiting or CAPTCHA challenges
4. Attacker successfully guesses administrative credentials within 40-60 seconds
5. Attacker gains full administrative access to the WordPress installation
6. Attacker can modify content, install malware, create backdoors, or exfiltrate data

## Root cause
The application fails to implement standard brute force protection mechanisms including: (1) Rate limiting on authentication endpoints, (2) Account lockout after failed login attempts, (3) CAPTCHA or challenge-response mechanisms, (4) Progressive delays between login attempts

## Attacker mindset
An attacker would recognize wp-admin as a standard WordPress administrative interface and assume default or common credentials are in use. The lack of rate limiting makes this an extremely low-effort attack requiring minimal resources or sophistication. Admin access represents the ultimate objective providing full system compromise.

## Defensive takeaways
- Implement rate limiting on all authentication endpoints (e.g., max 5 attempts per IP per 15 minutes)
- Deploy account lockout mechanisms after 3-5 failed login attempts for 30 minutes
- Integrate CAPTCHA or other challenge-response systems after 2-3 failed attempts
- Enforce strong password policies requiring minimum 12 characters with complexity
- Implement progressive delays (exponential backoff) between failed authentication attempts
- Monitor and alert on multiple failed login attempts from single IP addresses
- Use Web Application Firewalls (WAF) to detect and block brute force patterns
- Enforce multi-factor authentication (MFA) for all administrative accounts
- Disable or rename the /wp-admin endpoint; use /wp-login.php with additional protections
- Implement IP whitelisting for administrative access when possible
- Use security headers and implement fail2ban or similar tools

## Variant hunting
Check for similar rate limiting issues on /wp-login.php endpoint
Test other authentication endpoints (/api/auth, /login, /api/login) for brute force vulnerability
Verify if password reset functionality has similar protections
Test if other HTTP methods (POST, PUT, PATCH) bypass rate limiting on login
Check if changing User-Agent or X-Forwarded-For headers bypasses IP-based rate limiting
Test for timing attack vulnerabilities in password comparison logic
Enumerate valid usernames through response time analysis or error messages
Test API endpoints that may share authentication but lack protections

## MITRE ATT&CK
- T1110.001 - Brute Force: Password Guessing
- T1110.002 - Brute Force: Credential Stuffing
- T1110 - Brute Force
- T1621 - Multi-Factor Authentication Interception
- T1078.001 - Valid Accounts: Local Accounts

## Notes
This is a straightforward but critical vulnerability. The reporter provided clear reproduction steps using common brute force tools and demonstrated approximate attack speed (3000 passwords in 40 seconds). The vulnerability affects the most sensitive part of a WordPress installation (admin access). The fix is well-established and standardized across the industry. No complexity in exploitation but maximum impact due to administrative access compromise.

## Full report
<details><summary>Expand</summary>

The domain https://my.stripo.email in the directory /wp-admin are not blocking amount of request in the authorization form, this leads to bruteforce attack. Where the attacker are able to guess tons of passwords without getting blocked or the password field gets locked.
This attack make it possible to gain access as an admin extremely easy and quick to get a successfully login.

To test this security issue you need to visit the link https://my.stripo.email in the directory /wp-admin
Install a bruteforce tool like: Burp intruder, Wfuzz, Hydra, Ncrack
I personality use Wfuzz and Burp.

Wfuzz command in Linux terminal: wfuzz -c -w /usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt -u https://my.stripo.email/wp-admin -d "Authorization: Basic admin:FUZZ" 

Supported links and fix tips:
https://owasp.org/www-community/attacks/Brute_force_attack
https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks

This Pictures below show status from my program as you can see with Wfuzz it hitted around 3000 passwords in like 40 secounds (calculated approximately.)
My Burp suite shows more exact response from your server.

## Impact

Get access to anadmin login quickly and while logged in the attacker can do whatever an admin can.

</details>

---
*Analysed by Claude on 2026-05-24*
