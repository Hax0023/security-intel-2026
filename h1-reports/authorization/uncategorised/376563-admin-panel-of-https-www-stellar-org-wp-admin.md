# Unauthenticated Access to WordPress Admin Panel

## Metadata
- **Source:** HackerOne
- **Report:** 376563 | https://hackerone.com/reports/376563
- **Submitted:** 2018-07-04
- **Reporter:** hach3ro
- **Program:** Stellar Development Foundation
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Improper Access Control, Information Disclosure, Insufficient Authentication
- **CVEs:** None
- **Category:** uncategorised

## Summary
The WordPress admin panel at /wp-admin/ is accessible to unauthenticated users, exposing administrative functionality and enabling enumeration of usernames and server details. This allows attackers to conduct targeted brute force attacks against admin credentials and gather reconnaissance information for further exploitation.

## Attack scenario
1. Attacker discovers /wp-admin/ is publicly accessible without authentication
2. Attacker accesses login page and enumerates valid usernames through error messages or timing attacks
3. Attacker gathers server information including WordPress version and OS details from HTTP headers or page content
4. Attacker performs targeted brute force attacks against known admin usernames
5. Upon successful credential compromise, attacker gains full administrative access
6. Attacker can modify site content, install malicious plugins, or pivot to backend infrastructure

## Root cause
WordPress admin panel not properly restricted at the web server or application level. Missing authentication checks before allowing access to /wp-admin/ directory and missing proper access control mechanisms to prevent unauthenticated users from viewing administrative interfaces.

## Attacker mindset
Reconnaissance and initial access. The attacker sees the exposed admin panel as low-hanging fruit for information gathering and credential attack planning, treating it as a starting point for privilege escalation and site compromise.

## Defensive takeaways
- Implement strict authentication checks before allowing any access to /wp-admin/ directory
- Restrict /wp-admin/ access by IP whitelist or require VPN access for administrative functions
- Disable directory listing and hide sensitive information from HTTP headers and error messages
- Implement rate limiting and CAPTCHA on login attempts to prevent brute force attacks
- Use WAF rules to block access to /wp-admin/ from non-whitelisted sources
- Hide WordPress version information and server details from responses
- Consider renaming or obfuscating the admin panel URL
- Implement multi-factor authentication for all administrative accounts
- Monitor and alert on failed login attempts and unusual admin panel access patterns

## Variant hunting
Check for other exposed admin interfaces (/administrator/, /admin/, /backend/, /management/), verify access controls on API endpoints that perform administrative operations, test for authentication bypass via HTTP method overloading or header manipulation, examine if sensitive functionality is exposed through REST APIs

## MITRE ATT&CK
- T1190
- T1592
- T1595
- T1110
- T1087

## Notes
This is a critical access control vulnerability that essentially grants reconnaissance capabilities to unauthenticated attackers. The exposure of server/version information combined with admin panel accessibility significantly increases the attack surface. The vulnerability demonstrates lack of basic security hardening on a high-profile target.

## Full report
<details><summary>Expand</summary>

https://www.stellar.org/wp-admin/ link has various operations which should not be accessible to an anonymous user.

As admin panel is accessible an attacker can use this information in targeted attack and he can bruteforce the username and password.

on the other side server information is easily available with version and operating system details.

## Impact

https://www.stellar.org/wp-admin/

</details>

---
*Analysed by Claude on 2026-05-24*
