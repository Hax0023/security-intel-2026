# Administrator Information Disclosure via JSON REST API on wordpress.org

## Metadata
- **Source:** HackerOne
- **Report:** 221734 | https://hackerone.com/reports/221734
- **Submitted:** 2017-04-18
- **Reporter:** 596a96cc7bf9108cd896f33c4
- **Program:** WordPress.org
- **Bounty:** Not specified in writeup
- **Severity:** medium
- **Vuln:** Information Disclosure, Improper Access Control, Sensitive Data Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
The WordPress REST API endpoint `/wp-json/wp/v2/users` on developer.wordpress.org exposes sensitive administrator user information without proper authentication or access controls. This allows unauthenticated attackers to enumerate and gather details about administrator accounts, facilitating social engineering or targeted attacks.

## Attack scenario
1. Attacker discovers the WordPress REST API is enabled on developer.wordpress.org
2. Attacker crafts HTTP request to /wp-json/wp/v2/users endpoint
3. API responds with full list of user objects including administrator accounts
4. Attacker extracts sensitive fields such as admin usernames, emails, display names, and user IDs
5. Attacker uses collected information for targeted phishing, account enumeration, or further reconnaissance
6. Information can be correlated with other data sources to identify organizational structure and key personnel

## Root cause
The WordPress REST API users endpoint was not properly restricted with appropriate capabilities checks. By default, WordPress REST API exposes user information without requiring authentication or sufficient authorization levels, even when accessing administrator accounts.

## Attacker mindset
Reconnaissance-focused attacker conducting information gathering on the WordPress.org infrastructure to identify high-value targets (administrators) for subsequent phishing, social engineering, or credential compromise attacks. Likely part of a larger campaign to compromise WordPress ecosystem resources.

## Defensive takeaways
- Implement strict capability checks on REST API endpoints to restrict user enumeration
- Disable or properly secure REST API user endpoints if not needed for public consumption
- Apply authentication requirements to sensitive endpoints before exposing user data
- Use WordPress plugins or custom code to restrict /wp-json/wp/v2/users to authenticated users only
- Monitor and audit REST API access logs for enumeration attempts
- Configure web application firewall rules to detect suspicious user enumeration patterns
- Regularly audit WordPress configuration and enabled endpoints on public-facing sites

## Variant hunting
Test other REST API endpoints for information disclosure: /wp/v2/pages, /wp/v2/posts, /wp/v2/comments
Check if other WordPress subdomains (wordpress.com, support.wordpress.org) have similar exposures
Investigate if user endpoint supports filtering parameters to bypass access controls (?per_page=999, ?context=edit)
Test GraphQL endpoints if enabled for similar user enumeration vulnerabilities
Check for information leakage through XML-RPC interface (xmlrpc.php) user listing methods
Examine author archive pages (/author/username/) for information disclosure patterns

## MITRE ATT&CK
- T1590.002 - Gather Victim Identity Information: Credentials
- T1590.003 - Gather Victim Identity Information: Employee Names
- T1087.001 - Account Discovery: Local Account
- T1526 - Exposure of Sensitive Information to an Unintended Actor
- T1589.001 - Gather Victim Identity Information: Credentials

## Notes
This is a classic REST API misconfiguration vulnerability common in WordPress installations. The vulnerability is particularly critical on high-value targets like wordpress.org infrastructure. The reporter provided minimal detail but sufficient PoC. The actual impact depends on what user fields are exposed (email addresses are particularly valuable for phishing). Response should include reviewing all REST API endpoints and implementing proper authorization frameworks.

## Full report
<details><summary>Expand</summary>



Greetings,

Hello Security Team,

Summary:

I have found a security vulnerability that can disclose some information of administrator users in this sub domain `developer.wordpress.org`

### Description (Include Impact):
Sensitive information disclosure of administrator users.

### PoC URL:
* https://developer.wordpress.org/wp-json/wp/v2/users

###PoC Screen Shot: 
* {F176692}


Let me know if you need more information.

Cheers!
j3


</details>

---
*Analysed by Claude on 2026-05-24*
