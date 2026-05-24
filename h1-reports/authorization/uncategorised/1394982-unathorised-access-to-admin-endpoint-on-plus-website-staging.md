# Unauthorized Access to Admin Endpoint on plus-website-staging5.shopifycloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 1394982 | https://hackerone.com/reports/1394982
- **Submitted:** 2021-11-09
- **Reporter:** j0j0
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Missing Authentication, Information Disclosure, Sensitive Data Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated endpoint at https://plus-website-staging5.shopifycloud.com/admin/ allows direct access to administrative functionality without proper authentication, exposing partner and customer contact details. The researcher successfully accessed and modified partner account data on what appears to be a staging environment containing real user information.

## Attack scenario
1. Attacker discovers the staging admin endpoint URL through subdomain enumeration or public sources
2. Attacker navigates directly to https://plus-website-staging5.shopifycloud.com/admin/ without providing credentials
3. Admin interface loads without authentication challenge, granting full access to administrative menu
4. Attacker enumerates available functions and gains ability to view, modify, and delete partner account data
5. Attacker creates unauthorized partner accounts or extracts sensitive contact information of existing partners/clients
6. Attacker assesses additional attack vectors (SQLi, RCE) for privilege escalation

## Root cause
Complete absence of authentication controls on the administrative endpoint. The staging environment lacks proper access restrictions, potentially due to misconfigured deployment, missing middleware authentication checks, or improper environment separation between staging and production.

## Attacker mindset
The researcher demonstrates responsible disclosure practices by pausing testing and seeking permission before escalation attempts. However, a malicious actor would proceed to extract all available data, modify critical configurations, create backdoor accounts, and attempt command injection for complete system compromise.

## Defensive takeaways
- Implement mandatory authentication on ALL administrative endpoints, including staging environments
- Use network-level access controls (IP whitelisting, VPN requirements) for staging admin interfaces
- Deploy Web Application Firewalls (WAF) with authentication bypass detection rules
- Implement API gateway authentication before requests reach backend services
- Separate staging and production environments with distinct credential systems
- Enforce environment-specific authentication requirements in application code
- Regular security scanning of staging/non-production endpoints for authentication bypass
- Implement centralized authentication/authorization (OAuth 2.0, SAML) across all environments
- Audit and remove test/debug endpoints before deployment
- Use RBAC (Role-Based Access Control) with default-deny principle
- Monitor access logs for suspicious admin endpoint access patterns

## Variant hunting
Other Shopify Cloud staging subdomains (staging1-10) - likely share same vulnerability pattern
Admin paths variations: /admin/, /administrator/, /admin-panel/, /backend/, /dashboard/
Parameter-based authentication bypass: ?admin=true, ?bypass=1, ?env=prod
HTTP method override: POST to GET endpoints or vice versa to bypass middleware
Header-based auth bypass: X-Admin, X-Bypass-Auth, X-Original-URL headers
API endpoint variants: /api/admin/, /graphql/admin/, /rest/admin/
Development/debug endpoints: /debug/, /dev/, /test/, /swagger/, /api-docs/
Other Shopify staging cloud services (.shopifycloud.com wildcard enumeration)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1589 - Gather Victim Identity Information
- T1590 - Gather Victim Network Information
- T1526 - Cloud Service Discovery
- T1199 - Trusted Relationship
- T1087 - Account Discovery
- T1087.004 - Cloud Account
- T1580 - Cloud Infrastructure Discovery

## Notes
Report quality degraded by redacted/censored content (█████████). Researcher exercised good judgment by halting escalation testing and requesting authorization. The presence of real partner/customer data in staging is a critical finding suggesting inadequate data classification and environment separation. DNS interaction mentioned suggests possible reconnaissance for SSRF/RCE vectors. Staging environment compromises are often gateway attacks to production systems due to shared credentials, databases, or code repositories.

## Full report
<details><summary>Expand</summary>

## Summary:
https://plus-website-staging5.shopifycloud.com/admin/ allows to access/modify and delete partners data.
While the environment seems to be staging, partner's/clients contact details look pretty real.

##Sorry:  
During the testing, I've created Test111 partner account, trying to escalate the issue, however can't find an option to delete it :| So far I  did receive some DNS interaction on my collaboration server, but I've decided to stop testing and ask first. Please let me know if I can play around and try escalating it to RCE or SQLi or something else (If it's matters to you)

## Shops Used to Test:
None

## Relevant Request IDs:
061890664b777d5f7e5cc84eefa5c8c5

## Steps To Reproduce:
Go to https://plus-website-staging5.shopifycloud.com/admin/ and check the administrative menu
█████████

Kind Regards,
j0j0

## Impact

Partners and customers data leakage, probably the issue can be escalated to something more impactful.

</details>

---
*Analysed by Claude on 2026-05-24*
