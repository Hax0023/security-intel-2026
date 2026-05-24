# Shop Admin Privilege Escalation via Login Services Configuration

## Metadata
- **Source:** HackerOne
- **Report:** 56626 | https://hackerone.com/reports/56626
- **Submitted:** 2015-04-16
- **Reporter:** satishb3
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Privilege Escalation, Insufficient Authorization Checks, Horizontal Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Shop administrators with full access could escalate privileges to modify login service configurations (Google Apps login) despite the UI restricting this to account owners only. An attacker could modify external login services by directly sending POST requests to the API endpoint with proper authentication tokens, effectively bypassing the intended authorization model.

## Attack scenario
1. Attacker gains shop admin credentials (social engineering, credential stuffing, or insider threat)
2. Attacker logs into Shopify admin panel and confirms Login Services section is hidden from their role
3. Attacker intercepts or crafts a direct POST request to /admin/login_services/google_apps/update endpoint
4. Attacker includes valid authenticity_token and session cookies to bypass CSRF protection
5. Attacker modifies shop[google_apps_login_enabled] parameter to enable Google Apps login and sets malicious google_apps_domain
6. Attacker successfully modifies login services; account owner later discovers unauthorized external IdP configured, potentially enabling account takeover

## Root cause
Backend authorization checks on the login_services controller only validated role-based access at the UI/view layer rather than enforcing it at the API/controller level. The API endpoint /admin/login_services/google_apps/update lacked proper authorization middleware to verify whether the request originated from an account owner, allowing shop admins to bypass the intended restriction through direct API calls.

## Attacker mindset
An opportunistic insider or compromised admin account holder recognizes that UI-level restrictions are often incomplete. By directly accessing the API endpoint with valid session tokens, they can escalate privileges without being detected through normal UI workflows. The attacker aims to either lock out legitimate owners via unauthorized IdP configuration or establish persistent backdoor access through external login services.

## Defensive takeaways
- Implement authorization checks at the controller/API level, not just the view/UI layer
- Use principle of least privilege: verify role/permission on every backend request, not once per session
- Audit all sensitive endpoints (especially those handling authentication/authorization settings) for missing access control checks
- Separate role-based permissions clearly: account owner vs shop admin vs other roles should be enforced server-side
- Implement request validation to ensure parameters match the requesting user's permission level
- Regularly audit API endpoints against UI restrictions to identify discrepancies
- Log all modifications to critical settings (login services, authentication) with user context for forensic analysis

## Variant hunting
Check other admin API endpoints for similar authorization bypasses (payment methods, shipping settings, staff management)
Test if shop admins can modify other account-owner-only settings through direct API calls (2FA settings, recovery codes, account deletion)
Verify whether other roles (staff members with limited permissions) can escalate privileges via API endpoints
Examine if authenticity_token validation can be bypassed or if CSRF protection is incomplete
Test if modifying other external login services (SAML, OAuth providers) has the same vulnerability
Check for parameter tampering: whether changing other fields in the request could escalate impact

## MITRE ATT&CK
- T1190
- T1078
- T1556
- T1556.003
- T1136

## Notes
This is a classic authorization bypass vulnerability where UI-level controls are bypassed through direct API access. The vulnerability demonstrates the importance of securing APIs independently from UI controls. The use of authenticity_token and proper cookies indicates the attacker was already authenticated, making this a privilege escalation rather than authentication bypass. The severity is amplified because login service configuration could lead to account takeover of the entire shop. Shopify's multi-tenant architecture means this could affect multiple businesses if automated.

## Full report
<details><summary>Expand</summary>

 'Login services' section in the Settings->Account is accessible only to the Account owners. However, shop admins (full access users) can escalate privileges and modify the login services.

To verify,
1. Log into https://seclearn.myshopify.com as admin.
2. Navigate to settings->Account, notice that it does not show Login Services section to this user. However, he can modify the Login Services by sending the below request (use proper authenticity_token and cookies before sending the request).

	POST /admin/login_services/google_apps/update HTTP/1.1
	Host: seclearn.myshopify.com
	User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0
	Cookie: ...
	Content-Type: application/x-www-form-urlencoded
	
	utf8=%E2%9C%93&_method=patch&authenticity_token=xxxxxPaAQQFSKgdwaJr6XWqFbBkQ%3D&shop%5Bgoogle_apps_login_enabled%5D=0&shop%5Bgoogle_apps_login_enabled%5D=1&shop%5Bgoogle_apps_domain%5D=securitylearn.net&commit=Save


3. To confirm, log in as Account owner and look at the Login Services section. Notice that, Google apps are enabled and securitylearn.net is added to the google app domain.

</details>

---
*Analysed by Claude on 2026-05-24*
