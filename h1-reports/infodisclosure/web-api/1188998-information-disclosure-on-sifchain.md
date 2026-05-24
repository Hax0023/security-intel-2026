# Information Disclosure of WordPress Users via Unauthenticated REST API

## Metadata
- **Source:** HackerOne
- **Report:** 1188998 | https://hackerone.com/reports/1188998
- **Submitted:** 2021-05-08
- **Reporter:** rohitburke
- **Program:** Sifchain
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Insecure Direct Object References, API Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
The WordPress REST API endpoint at /wp-json/wp/v2/users/ is publicly accessible without authentication, exposing sensitive user information including usernames, user IDs, and employee details. This information can be leveraged by attackers to enumerate valid user accounts and conduct targeted brute-force attacks against the authentication system.

## Attack scenario
1. Attacker discovers the publicly exposed WordPress REST API endpoint /wp-json/wp/v2/users/
2. Attacker sends unauthenticated HTTP GET request to enumerate all WordPress users and administrators
3. API returns complete user list containing usernames, IDs, display names, and profile information without requiring credentials
4. Attacker compiles list of valid usernames (particularly administrative accounts) from the response
5. Attacker uses enumerated usernames to conduct targeted brute-force password attacks against WordPress login or other systems
6. With known valid usernames, attacker significantly increases likelihood of successful account compromise

## Root cause
WordPress REST API user listing endpoint is enabled by default and accessible without authentication. The application failed to implement proper access controls or disable this endpoint, exposing the /wp-json/wp/v2/users/ endpoint to unauthenticated enumeration.

## Attacker mindset
Reconnaissance and information gathering phase of attack. Attacker is performing passive enumeration to identify valid user accounts before executing active attacks. Lower barrier to entry makes this an attractive initial reconnaissance vector for credential stuffing or brute-force campaigns.

## Defensive takeaways
- Disable or restrict WordPress REST API user endpoints (/wp-json/wp/v2/users) to authenticated users only
- Implement authentication requirements on all REST API endpoints that expose sensitive information
- Use WordPress security plugins to disable user enumeration endpoints or require authentication
- Implement rate limiting on authentication endpoints to mitigate brute-force attacks
- Monitor and log access to REST API endpoints for suspicious enumeration patterns
- Regularly audit WordPress plugin and API configurations for unintended information disclosure
- Consider implementing Web Application Firewall (WAF) rules to block API enumeration attempts

## Variant hunting
Check for similar enumeration on /wp-json/wp/v2/posts/ or /wp-json/wp/v2/pages/ endpoints
Test other REST API versions (/wp-json/wp/v1/users/) for same vulnerability
Enumerate custom REST API endpoints that may expose user or employee information
Check for exposed author archives (/author/?author=1) for username enumeration
Look for unauthenticated access to /wp-json endpoints on other WordPress installations
Test for information disclosure in search functionality or directory listings
Check XML-RPC and other WordPress APIs for similar enumeration issues

## MITRE ATT&CK
- T1592
- T1589
- T1590
- T1598
- T1110

## Notes
This is a classic WordPress misconfiguration issue where default REST API functionality is not properly secured. The vulnerability is straightforward to exploit and widely known in WordPress security community. References provided (reports 753725 and 138244) indicate this is a recurring issue across multiple organizations. The impact assessment notes connection to brute-force attacks, making this a multi-stage exploitation scenario rather than direct compromise. Severity is Medium rather than High because it requires chaining with other vulnerabilities (weak passwords, lack of rate limiting) for complete exploitation.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello Team,
I have found user/admin usernames disclosed.
Using REST API, we can see all the WordPress users/authors with some of their information. (such as id, name, login name, etc.) and employees of Sifchain without authentication on https://sifchain.finance/

## Steps To Reproduce:
You can find the information disclosure by going to the following URL  (https://sifchain.finance/wp-json/wp/v2/users/)

 
## Supporting Material/References:
    1) https://hackerone.com/reports/753725
    2) https://hackerone.com/reports/138244

## Impact

1) Malicious users  could collect the usernames disclosed and be focused throughout BF (bruteforce) attack (as the usernames are now known), making it less harder to penetrate the systems.
2) Therefore this information can be used to do bruteforce login.

</details>

---
*Analysed by Claude on 2026-05-24*
