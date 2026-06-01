# Username Enumeration Leading to Admin Account Brute Force

## Metadata
- **Source:** HackerOne
- **Report:** 188205 | https://hackerone.com/reports/188205
- **Submitted:** 2016-12-04
- **Reporter:** hackerwahab
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Username Enumeration, Weak Brute Force Protection, Insufficient Rate Limiting
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Nextcloud WordPress admin panel at /wp-admin was vulnerable to username enumeration, allowing attackers to discover valid usernames (such as 'frank'). Once enumerated, attackers could perform brute force attacks against discovered admin accounts without adequate rate limiting or account lockout mechanisms, potentially leading to full server compromise.

## Attack scenario
1. Attacker uses WPScan or similar tools to enumerate valid usernames from the /wp-admin endpoint
2. Tool identifies 'frank' as a valid admin username through response time differences or error messages
3. Attacker performs dictionary/brute force attack against the 'frank' account using WPScan or custom scripts
4. Weak or absent rate limiting allows rapid password attempts without throttling
5. Attacker gains admin credentials and accesses the WordPress administration panel
6. Attacker uploads malicious shell/plugin to compromise the server and pivot to subdomains

## Root cause
WordPress /wp-admin endpoint exposed user enumeration through response variations; absence of rate limiting, account lockout policies, or CAPTCHA on login attempts; no progressive delays between failed login attempts

## Attacker mindset
Low-skill attacker seeking quick compromise of WordPress installations using automated tools; motivation is opportunistic server takeover for malware distribution or lateral movement to hosting infrastructure

## Defensive takeaways
- Implement aggressive rate limiting on /wp-admin login endpoints (e.g., max 5 attempts per 15 minutes per IP)
- Deploy account lockout mechanisms after configurable failed attempts (e.g., 5-10 failures lock account for 30 minutes)
- Use CAPTCHA/reCAPTCHA after 2-3 failed login attempts
- Disable user enumeration by standardizing error messages ('Invalid username or password')
- Hide or restrict access to /wp-admin to known IPs via WAF/reverse proxy
- Monitor and alert on brute force patterns in real-time
- Enforce strong password policies and multi-factor authentication for admin accounts
- Consider security headers (X-Frame-Options, CSP) to prevent admin panel framing
- Use fail2ban or similar intrusion prevention systems

## Variant hunting
Check for similar enumeration in /wp-login.php endpoint
Test password reset functionality for username disclosure
Examine REST API endpoints for user enumeration (e.g., /wp-json/wp/v2/users)
Test XML-RPC (/xmlrpc.php) for user enumeration via system.multicall
Verify enumeration across different user roles (subscriber, editor, author)
Check for timing-based enumeration attacks
Test authentication bypass on /wp-admin with HTTP parameter pollution

## MITRE ATT&CK
- T1087
- T1110.001
- T1110.003
- T1012
- T1190

## Notes
Report quality is poor with informal language and limited technical detail; researcher provided generic mitigation advice ('WordPress Login Attemptizer') rather than specific implementation guidance. The vulnerability chain (enumeration → brute force → RCE) represents a critical authentication bypass leading to complete system compromise. Severity should be Critical given the clear path to admin access and server takeover.

## Full report
<details><summary>Expand</summary>

Hello,

My self Abdulwahab,
 I want to Alert You that Your website is Facing a serious Problem Called : Username Enumeration
This Problem is on
nextcloud.com/wp-admin

We Use wpscan to get username 

and the username is 
"frank"
After getting username a user can Bruteforce it Using Wpscan and get access to admin panel and upload shell and also get all sub_domain Means Full Server is Hacked!

FIX
===
To Fix this use Wordpress Login Attemptizer

Thanks,
ABDULWAHAB,
Independent Cyber Security Researcher,



</details>

---
*Analysed by Claude on 2026-05-31*
