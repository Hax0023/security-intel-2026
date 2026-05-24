# Direct Access to Admin Dashboard via File Extension Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1421804 | https://hackerone.com/reports/1421804
- **Submitted:** 2021-12-09
- **Reporter:** mester_x
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Authorization Bypass, Path Traversal/Extension Manipulation, Information Disclosure, CSRF Token Exposure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Admin dashboard authentication protection can be bypassed by appending a file extension (.php) to the admin path, allowing unauthenticated users to view sensitive administrative information and CSRF tokens. While full administrative actions are blocked, the exposure of the admin interface and CSRF tokens presents significant security risks.

## Attack scenario
1. Attacker discovers that accessing /admin redirects to Okta authentication
2. Attacker appends .php extension to bypass authentication: /admin.php
3. Unauthenticated attacker gains direct access to admin dashboard without Okta login
4. Attacker views sensitive administrative data and information normally restricted
5. Attacker inspects page source (Ctrl+U) and extracts authenticity_token (CSRF token)
6. Attacker leverages exposed CSRF token to perform unauthorized administrative actions via cross-site request forgery

## Root cause
Insufficient authentication validation based on URL path. The application's authentication/authorization middleware likely checks for exact path matching (/admin) but fails to account for alternate representations of the same resource (/admin.php). The web server may be treating /admin and /admin.php as different paths, bypassing centralized authentication checks.

## Attacker mindset
Opportunistic attacker testing common bypass techniques (file extensions, URL encoding variations) against protected resources. Once discovering the bypass works, attacker prioritizes information gathering (CSRF tokens, admin data) for follow-up attacks like CSRF.

## Defensive takeaways
- Implement authentication/authorization at the application layer, not just URL routing level
- Normalize URL paths before authentication checks to prevent extension-based bypasses
- Use consistent authentication enforcement across all path variants and extensions
- Implement strict URL rewriting rules to prevent access to admin paths with alternative extensions
- Validate and enforce authentication before rendering any admin content or sensitive data
- Rotate CSRF tokens frequently and prevent exposure to unauthenticated users
- Implement defense-in-depth: layered authentication (web server level, application level, API level)
- Use security headers to prevent unauthorized access and information disclosure
- Test authentication bypasses as part of security testing (path traversal, extensions, null bytes)

## Variant hunting
Test other file extensions: /admin.html, /admin.asp, /admin.aspx, /admin.jsp, /admin.jspx
Test case variations: /Admin.php, /ADMIN.php, /aDmIn.php
Test double extensions: /admin.php.bak, /admin.php~
Test null byte injection: /admin.php%00, /admin%00.php (legacy systems)
Test trailing characters: /admin.php/, /admin.php;.html
Test special encoding: /admin%2ephp, /admin%252ephp
Check other protected endpoints: /admin-panel.php, /dashboard.php, /settings.php
Test on other subdomains listed in scope

## MITRE ATT&CK
- T1190
- T1566
- T1539
- T1078
- T1110

## Notes
The reporter identified CSRF token exposure as the most critical finding. The vulnerability chain is: (1) Authentication bypass via extension manipulation, (2) Unauthorized access to admin interface, (3) Information disclosure of CSRF tokens, (4) Potential for CSRF attacks using exposed tokens. The report mentions this affects multiple subdomains. The inability to perform state-changing actions (discard, edit, create) while unauthenticated may be due to server-side CSRF validation, but token exposure still enables attacks. The vulnerability demonstrates the importance of comprehensive input validation and path normalization in security-sensitive operations.

## Full report
<details><summary>Expand</summary>

* This issue affect two Subdomains, https://data-stories-website.shopifycloud.com/admin.php  `and`  https://datastories.shopify.com/admin.php

## Summary:
Hi Team,
When Link to https://datastories.shopify.com/admin   or  https://data-stories-website.shopifycloud.com/admin the subdomain redirect you to https://shopify.okta.com/login/login.htm?fromURI=/oauth2/v1/authorize/redirect?okta_key=PJl7eQUE9mYSKrtADqQAMe6v3y_SA3iqFtstkVPavAA for OKTA authentication to perform non admins from the Admin dashboard at https://datastories.shopify.com/admin.
But non authentications users still can access the admin dashboard  just by add any extintion to the admin word => https://datastories.shopify.com/admin.php .
When link to https://datastories.shopify.com/admin.php You can see the admin dashboard for the subdomain and the information replaced in.
* You can't discard, edit  or create Globals while you are not authenticated, But you can still see administrative information.
* When You press Ctrl+U you can see parameter called `authenticity_token` which admin csrf_token, This token can used to perform CSRF attack on the site admin **I can't perform for u the CSRF attack now for manu reasons, but accessing this token is critical issue**.

## Steps To Reproduce:

  1. Link to https://datastories.shopify.com/admin.php , and  https://data-stories-website.shopifycloud.com/admin.php

## Impact

Direct access to admin dashboard

</details>

---
*Analysed by Claude on 2026-05-24*
