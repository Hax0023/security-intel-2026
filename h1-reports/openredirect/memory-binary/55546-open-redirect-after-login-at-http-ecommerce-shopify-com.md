# Open Redirect after login at http://ecommerce.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 55546 | https://hackerone.com/reports/55546
- **Submitted:** 2015-04-09
- **Reporter:** dhaval
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Open Redirect, Post-Authentication Redirect
- **CVEs:** None
- **Category:** memory-binary

## Summary
An open redirect vulnerability exists on the Shopify ecommerce login page where the 'return_to' parameter is not properly validated. Attackers can craft a URL with a malicious 'return_to' parameter containing a domain suffix (e.g., '.mx', '.es', '.tw') that redirects authenticated users to attacker-controlled domains after successful login.

## Attack scenario
1. Attacker crafts a malicious URL with return_to=.mx%2F parameter pointing to attacker-controlled domain (e.g., ecommerce.shopify.com.mx)
2. Attacker sends phishing email/message to victim with the crafted login URL (http://ecommerce.shopify.com/accounts?found_email=true&return_to=.mx%2F)
3. Victim clicks the link and is taken to legitimate Shopify login page, appears trustworthy
4. Victim enters their email and password on the legitimate-looking form
5. Upon successful authentication, the application redirects victim to attacker-controlled domain (ecommerce.shopify.com.mx)
6. Attacker can harvest session cookies, credentials, or perform credential harvesting on the attacker-controlled lookalike domain

## Root cause
Insufficient input validation on the 'return_to' parameter. The application fails to verify that the redirect destination is a whitelist of trusted domains. The parameter accepts relative paths and domain suffix manipulation without proper URL parsing and validation.

## Attacker mindset
An attacker recognizes that post-login redirects are trusted by users and leverage this for credential theft or session hijacking. By using domain suffix manipulation (.mx, .es, .tw), the attacker creates convincing lookalike domains that bypass simple URL validation. The attack leverages user trust in the initial legitimate login page to deliver them to attacker infrastructure after authentication.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters
- Use URL parsing libraries to properly parse and validate redirect destinations
- Only allow redirects to paths on the same domain (same-origin policy)
- Validate that redirect_to/return_to parameters contain only absolute URLs matching a whitelist of safe domains
- Implement POST-Redirect-GET pattern with server-side session storage for return URLs instead of URL parameters
- Use DNS validation or domain ownership verification for any external redirect
- Log and monitor redirect parameters for suspicious patterns
- Implement Content Security Policy (CSP) with frame-ancestors and redirect restrictions

## Variant hunting
Test other authentication endpoints (register, password reset, oauth callbacks) for open redirect via return_to, redirect_uri, next, redirect_url parameters
Try variations: return_to=//evil.com, return_to=///evil.com, return_to=\\evil.com, return_to=javascript:alert(1)
Check if other URL parameters like 'found_email', 'user[email]' have injection points
Test double-encoding: %252e%252emx to bypass filters
Try domain confusion: return_to=@evil.com, return_to=evil.com@shopify.com
Investigate if data exfiltration occurs during redirect (leaking tokens in Referer header)
Check other Shopify subdomains for similar patterns

## MITRE ATT&CK
- T1598.003
- T1598.000
- T1187
- T1598

## Notes
This is a classic post-authentication open redirect enabling credential phishing campaigns. The vulnerability is particularly dangerous because it abuses user trust in legitimate authentication flows. The ability to manipulate domain suffixes (.mx, .es, .tw) suggests inadequate URL validation logic. The vulnerability likely scored high on CVSS due to ease of exploitation and potential for credential theft, though the report doesn't specify the bounty amount awarded.

## Full report
<details><summary>Expand</summary>

Hi,

The users can be redirected to some other site which is in control of the attacker from http://ecommerce.shopify.com/accounts

Let's say user is attacker asked victim to login from the here :
http://ecommerce.shopify.com/accounts?found_email=true&return_to=.mx%2F&user[email]=email@email.com

When victim enters the password he is redirected to http://ecommerce.shopify.com.mx/
This com.mx can be changed to multiple like .es .tw etc

These can be controlled by the attacker and used in other attacks



</details>

---
*Analysed by Claude on 2026-05-24*
