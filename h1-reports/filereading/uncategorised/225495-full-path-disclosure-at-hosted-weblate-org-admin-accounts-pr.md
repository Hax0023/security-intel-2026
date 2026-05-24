# Full Path Disclosure and Missing Rate Limiting on Admin Authentication

## Metadata
- **Source:** HackerOne
- **Report:** 225495 | https://hackerone.com/reports/225495
- **Submitted:** 2017-05-02
- **Reporter:** geekdad
- **Program:** Weblate
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Missing Rate Limiting, Brute Force Attack
- **CVEs:** None
- **Category:** uncategorised

## Summary
The admin authentication endpoint at hosted.weblate.org/admin/accounts/profile/ discloses full path information through authentication prompts, revealing the directory structure of protected areas. Additionally, the admin login form lacks rate limiting, allowing attackers to conduct brute force attacks against staff accounts without restriction.

## Attack scenario
1. Attacker browses hosted.weblate.org/admin/accounts/profile/ without authentication
2. Server responds with authentication prompt that reveals the full path structure of the admin directory
3. Attacker obtains information about protected admin areas and their location
4. Attacker navigates to hosted.weblate.org/admin/login/?next=/admin/ endpoint
5. Attacker launches automated brute force attack using credential lists against the login form
6. Due to absence of rate limiting, attacker can attempt unlimited login combinations to compromise staff accounts

## Root cause
The application fails to implement two security controls: (1) proper error message handling that masks sensitive path information in authentication responses, and (2) rate limiting mechanisms on authentication endpoints to prevent brute force attacks

## Attacker mindset
An attacker would use path disclosure to understand the administrative structure and identify high-value targets, then exploit the missing rate limiting to systematically compromise staff accounts through credential stuffing or dictionary attacks

## Defensive takeaways
- Implement generic authentication error messages that do not reveal path structure or confirm existence of protected resources
- Add rate limiting to all authentication endpoints with progressive delays or temporary lockouts after failed attempts
- Log and monitor authentication attempts for anomalies indicating brute force campaigns
- Implement CAPTCHA or multi-factor authentication on admin login forms
- Use constant-time comparison functions to prevent timing-based information leakage in authentication
- Configure Web Application Firewall (WAF) rules to detect and block brute force patterns

## Variant hunting
Check other admin subpaths (/admin/users/, /admin/settings/) for similar path disclosure
Test API endpoints for missing rate limiting on authentication
Verify if path information is disclosed in HTTP headers, response times, or error pages across the application
Examine if password reset or account recovery endpoints also lack rate limiting
Test other authenticated areas for information leakage through 403/401 responses

## MITRE ATT&CK
- T1110
- T1592
- T1589
- T1598

## Notes
This is a compound vulnerability combining information disclosure with brute force capability. The severity is elevated because path disclosure enables targeted attacks. The report lacks specifics on actual successful exploitation, bounty amount, and timeline. The researcher should have included proof-of-concept brute force attempts demonstrating the absence of rate limiting controls.

## Full report
<details><summary>Expand</summary>

Browsing this link https://hosted.weblate.org/admin/accounts/profile/  will ask for admin username and password as asked  when browsing https://hosted.weblate.org/admin/accounts/ or https://hosted.weblate.org/admin/ hence disclosing the directory path of forbidden area.
screenshot : path.png

also it is found that there is no rate limiting enforced at https://hosted.weblate.org/admin/login/?next=/admin/  hence attacker can break into staffs account by brute forcing. 
screenshot : login.png

</details>

---
*Analysed by Claude on 2026-05-24*
