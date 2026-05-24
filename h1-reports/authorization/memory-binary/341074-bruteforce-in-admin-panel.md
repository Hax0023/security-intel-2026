# Bruteforce in Admin Panel - Missing Rate Limiting

## Metadata
- **Source:** HackerOne
- **Report:** 341074 | https://hackerone.com/reports/341074
- **Submitted:** 2018-04-20
- **Reporter:** shawalkhan
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Brute Force Attack, Missing Rate Limiting, Weak Authentication Controls
- **CVEs:** None
- **Category:** memory-binary

## Summary
The WordPress admin login panel at wp-login.php lacks rate limiting protections, allowing attackers to conduct unlimited brute force attacks against user credentials. An attacker can systematically attempt to guess admin passwords without any throttling or account lockout mechanisms in place.

## Attack scenario
1. Attacker identifies the WordPress login endpoint at /wp-login.php
2. Attacker uses automated tools to send rapid login attempts with common passwords or from credential stuffing lists
3. No rate limiting blocks or delays the requests, allowing hundreds of attempts per minute
4. Attacker successfully guesses weak admin credentials or reuses leaked credentials from other breaches
5. Attacker gains unauthorized access to WordPress admin dashboard
6. Attacker can modify content, install malicious plugins, create backdoors, or compromise the entire website

## Root cause
The application fails to implement rate limiting on authentication endpoints, allowing unlimited login attempts without any temporal or logical constraints.

## Attacker mindset
Opportunistic attacker looking for easy wins - targeting well-known CMS platforms with default endpoints. This vulnerability requires minimal sophistication and can be exploited with readily available tools.

## Defensive takeaways
- Implement rate limiting on all authentication endpoints (IP-based and account-based)
- Enforce account lockout after N failed login attempts within a time window
- Add progressive delays (exponential backoff) between failed attempts
- Implement CAPTCHA challenges after multiple failed attempts
- Monitor and alert on suspicious authentication patterns
- Use Web Application Firewall (WAF) rules to block brute force patterns
- Enforce strong password policies and multi-factor authentication
- Change default WordPress login URL to non-standard path

## Variant hunting
Look for missing rate limiting on: password reset endpoints, API authentication endpoints, OTP verification flows, user registration endpoints, or any endpoint accepting credentials or sensitive tokens.

## MITRE ATT&CK
- T1110 - Brute Force
- T1110.001 - Brute Force: Password Guessing
- T1078.001 - Valid Accounts: Default Accounts

## Notes
This is a straightforward vulnerability report with clear impact and solution. The report lacks technical depth (no proof of concept or specific metrics), but the core issue is valid and high-risk. WordPress installations are frequently targeted by automated brute force botnets. The fix is standard practice but often overlooked.

## Full report
<details><summary>Expand</summary>

Hello there,
Admin panel of your website (https://nextcloud.com/wp-login.php) is vulnerable to bruteforce attacks as their is no rate-limiting.

## Impact

Can gain access to admin panel.
To fix this, Just add rate limiting.

</details>

---
*Analysed by Claude on 2026-05-24*
