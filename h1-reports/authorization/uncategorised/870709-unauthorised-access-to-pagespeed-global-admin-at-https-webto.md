# Unauthorized Access to PageSpeed Global Admin Panel at webtools.paloalto.com

## Metadata
- **Source:** HackerOne
- **Report:** 870709 | https://hackerone.com/reports/870709
- **Submitted:** 2020-05-11
- **Reporter:** lordjerry0x01
- **Program:** Palo Alto Networks
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Authentication, Missing Access Controls, Insufficient Authorization
- **CVEs:** None
- **Category:** uncategorised

## Summary
A publicly accessible subdomain (webtools.paloalto.com) contains an administrative endpoint for PageSpeed Global Admin that lacks any authentication mechanism. An unauthenticated attacker can directly access the admin panel at /pagespeed-global-admin/ without credentials, potentially gaining full administrative control over the PageSpeed service.

## Attack scenario
1. Attacker discovers the webtools.paloalto.com subdomain through subdomain enumeration or reconnaissance
2. Attacker navigates to https://webtools.paloalto.com/pagespeed-global-admin/ without providing any credentials
3. The endpoint responds with the admin panel interface without requiring authentication
4. Attacker gains unauthorized access to PageSpeed Global Admin dashboard and its functionality
5. Attacker can view sensitive configuration, modify settings, or perform administrative actions
6. Attacker potentially modifies PageSpeed configurations affecting all downstream users and services

## Root cause
The PageSpeed Global Admin endpoint was deployed on a public-facing subdomain without implementing authentication or authorization checks. The application likely relies on implicit trust or expects authentication at a different layer that was bypassed or misconfigured.

## Attacker mindset
Opportunistic reconnaissance - attacker conducted subdomain enumeration, discovered an interesting webtools domain, and proactively tested for common admin paths or endpoints. The discovery suggests the attacker is performing thorough reconnaissance on Palo Alto's external attack surface to identify exposed administrative interfaces.

## Defensive takeaways
- Implement mandatory authentication (OAuth 2.0, SAML, or similar) on all administrative endpoints
- Apply authorization checks to verify user roles and permissions before granting access to admin panels
- Use Web Application Firewalls (WAF) to restrict access to admin endpoints by IP whitelist or require VPN
- Implement rate limiting and anomaly detection on authentication endpoints
- Conduct regular security audits of all public-facing subdomains and their exposed endpoints
- Use secure by default principles: deny access and explicitly grant permissions rather than the reverse
- Implement session management and token validation for all authenticated endpoints
- Monitor access logs for unauthorized attempts to admin endpoints

## Variant hunting
Search for other admin panels on webtools.paloalto.com or related subdomains (admin, console, dashboard, management)
Test other Palo Alto subdomains for similar authentication bypass patterns
Check for hardcoded credentials or default accounts on the PageSpeed service
Look for API endpoints related to PageSpeed that may also lack authentication
Test for horizontal privilege escalation - accessing other users' administrative functions
Investigate if PageSpeed Global Admin interacts with other Palo Alto services without proper trust boundaries

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (use of unauthenticated access)
- T1526 - Reconnaissance via subdomain enumeration
- T1592 - Gather Victim Identity Information
- T1133 - External Remote Services

## Notes
This is a straightforward but critical finding - direct access to an administrative panel without authentication. The vague 'You better know what can be done here' impact statement suggests the admin panel provides significant capabilities (configuration changes, data access, etc.). The report demonstrates solid reconnaissance methodology by discovering the subdomain and testing for common admin paths.

## Full report
<details><summary>Expand</summary>

## Summary:
I came across this subdomain `https://webtools.paloalto.com/` which took my attention, after a bit enumeration I found an endpoint which allows anyone to access `PageSpeed Global Admin` without any type of authentication. 

## Vulnerable URL:
`https://webtools.paloalto.com/pagespeed-global-admin/`

## Impact

You better know what can be done here.

</details>

---
*Analysed by Claude on 2026-05-24*
