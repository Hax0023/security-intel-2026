# Open Redirect at *.myshopify.com/account/login via checkout_url Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 103772 | https://hackerone.com/reports/103772
- **Submitted:** 2015-12-06
- **Reporter:** boredengineer21
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the Shopify login flow where the checkout_url parameter fails to properly validate redirect destinations. Attackers can craft malicious URLs that redirect authenticated users to attacker-controlled domains after login completion.

## Attack scenario
1. Attacker crafts a malicious URL with a specially crafted checkout_url parameter (e.g., ?checkout_url=.np) pointing to an external domain
2. Attacker distributes the link via phishing email, social engineering, or other means to target Shopify shop users
3. Victim receives the link and clicks it, arriving at the legitimate login page (*.myshopify.com)
4. Victim authenticates with their credentials on the legitimate login page
5. Upon successful authentication, the server processes the checkout_url redirect parameter without proper validation
6. Victim is redirected to attacker's domain (e.g., sehyoginfoshop.myshopify.com.np) where credential harvesting or malware distribution can occur

## Root cause
Insufficient URL validation in the checkout_url parameter processing. The redirect logic concatenates the shop domain with the user-supplied checkout_url parameter without enforcing that the resulting URL remains within Shopify's domain boundaries. The missing forward slash allows domain suffix manipulation (e.g., .np TLD attachment).

## Attacker mindset
An attacker would recognize that post-authentication redirect parameters are commonly overlooked in security reviews. By exploiting the lack of URL validation, they can leverage the trust users have in legitimate Shopify domains to deliver them to malicious sites. The technique is effective because it combines legitimate authentication with illegitimate redirects, making detection harder for users.

## Defensive takeaways
- Implement strict whitelist-based URL validation for all redirect parameters - only allow redirects to known safe domains/paths
- Use URL parsing libraries (not string concatenation) to construct and validate redirect destinations
- Enforce leading forward slashes in redirect URLs to prevent domain suffix manipulation attacks
- Validate that the host portion of redirect URLs matches expected domains using proper URL parsing
- Implement Content Security Policy (CSP) headers to limit redirect capabilities
- Log and monitor redirect parameters for suspicious patterns
- Perform post-authentication security checks before executing redirects

## Variant hunting
Search for other redirect parameters in authentication flows (return_url, next, redirect_to, callback_url, success_url)
Test redirect parameters at different Shopify endpoints (checkout, admin, customer portal)
Check if other URL manipulation techniques work: protocol manipulation (javascript:, data:), double encoding, case manipulation
Test in different Shopify shop contexts and subdomains
Look for similar patterns in Shopify's API endpoints that accept URL parameters

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1021.007 - Remote Services: Cloud Services

## Notes
This is a classic open redirect vulnerability exacerbated by improper string concatenation rather than proper URL handling. The vulnerability is particularly dangerous in authentication contexts because users trust the legitimate domain portion and may not notice the domain suffix manipulation. The suggested fix (adding a forward slash) is a band-aid; a proper solution requires URL parsing and strict validation. The report demonstrates good researcher practice by providing clear reproduction steps and a suggested fix.

## Full report
<details><summary>Expand</summary>

Hi,

Any user after logging into an any myshopify shop can be redirected to other domain.

To reproduce:
Send this to victim: 
http://sehyoginfoshop.myshopify.com/account/login?checkout_url=.np

Now when our victim logs in,
He will be redirected to
https://sehyoginfoshop.myshopify.com.np/

Which is not a shopify domain.

Fix: While redirecting Use <shop-name>"/"$checkout_url instead of <shop-name>$checkout_url

</details>

---
*Analysed by Claude on 2026-05-24*
