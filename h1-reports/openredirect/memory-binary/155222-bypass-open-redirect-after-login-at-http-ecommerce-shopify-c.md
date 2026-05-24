# Open Redirect after Login at ecommerce.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 155222 | https://hackerone.com/reports/155222
- **Submitted:** 2016-07-30
- **Reporter:** jamesclyde
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** memory-binary

## Summary
An open redirect vulnerability exists in the login functionality of ecommerce.shopify.com where the 'return_to' parameter is not properly validated. Attackers can craft malicious login URLs that redirect authenticated users to arbitrary external domains, enabling phishing and credential theft attacks.

## Attack scenario
1. Attacker crafts a malicious URL: https://ecommerce.shopify.com/accounts?return_to=%40evil.com/
2. Attacker distributes the URL via email, social media, or other channels to targeted victims
3. Victim clicks the link and is presented with the legitimate Shopify login page
4. Victim enters their credentials and submits the login form
5. After successful authentication, the application automatically redirects victim to https://evil.com
6. Victim believes they are on a trusted Shopify domain, increasing likelihood of falling for phishing or malware on the attacker-controlled site

## Root cause
The 'return_to' parameter in the login endpoint is not validated against a whitelist of allowed redirect destinations. The application trusts user-supplied input without ensuring the redirect target is within the same domain or an explicitly approved domain.

## Attacker mindset
Opportunistic attacker leveraging the trust users place in legitimate login pages to conduct phishing campaigns, steal additional credentials, or distribute malware while maintaining plausible deniability through the trusted Shopify domain in the initial URL.

## Defensive takeaways
- Implement strict whitelist validation for redirect parameters - only allow redirects to same-domain paths or pre-approved domains
- Use URL parsing to validate the scheme (http/https) and domain components separately
- Consider using relative URLs only for redirects to eliminate external redirection
- Implement Content Security Policy (CSP) headers to restrict navigation
- Add user interaction (confirmation dialog) before redirecting to external domains
- Log and monitor unusual redirect patterns for security analysis
- Educate users to verify the domain in the address bar before and after login

## Variant hunting
Test other authentication endpoints: /login, /signin, /auth for similar 'return_to' or 'redirect', 'next', 'destination' parameters
Check POST-based login redirects for the same vulnerability
Test double URL encoding: %2540evil.com or other encoding bypasses
Test protocol bypass: //evil.com, ///evil.com, javascript: URIs
Search for similar parameters in password reset, email verification, and account recovery flows
Test with data: URLs and other non-http schemes
Check if the vulnerability exists in mobile app endpoints or API authentication flows

## MITRE ATT&CK
- T1192
- T1566
- T1598

## Notes
The vulnerability is cross-browser and works consistently, indicating systematic lack of validation. The use of %40 (@ symbol) in the example suggests potential bypass attempts. The simplicity of exploitation and high user trust in login pages makes this particularly dangerous for credential harvesting campaigns. Post-login redirect vulnerabilities are especially dangerous because users have just authenticated and are more likely to trust subsequent interactions.

## Full report
<details><summary>Expand</summary>

Hi,

The users can be redirected to some other site which is in control of the attacker from http://ecommerce.shopify.com/accounts

Let's say user is attacker asked victim to login from the here :
https://ecommerce.shopify.com/accounts?return_to=%40evil.com/

When victim enters the password he is redirected to https://evil.com

These can be controlled by the attacker and used in other attacks

Works in all browsers!!






</details>

---
*Analysed by Claude on 2026-05-24*
