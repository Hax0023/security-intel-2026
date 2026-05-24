# Open Redirect in Bulk Edit

## Metadata
- **Source:** HackerOne
- **Report:** 169759 | https://hackerone.com/reports/169759
- **Submitted:** 2016-09-16
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in Shopify's bulk edit functionality where the return_to parameter is not properly validated, allowing attackers to redirect users to arbitrary external domains. By crafting a malicious URL with a manipulated return_to parameter, clicking the Close button redirects to attacker-controlled sites.

## Attack scenario
1. Attacker identifies the bulk edit endpoint at /admin/bulk with an unvalidated return_to parameter
2. Attacker crafts a malicious URL: https://<shop>.myshopify.com/admin/bulk?resource_name=Product&return_to=/..//evil.com
3. Attacker shares the URL via phishing email, social engineering, or trojanized links to Shopify merchants
4. Victim clicks the link and lands on the Shopify bulk edit page (appears legitimate)
5. Victim clicks the Close button, expecting to return to their admin panel
6. User is redirected to attacker's domain (evil.com), where credential harvesting or malware distribution occurs

## Root cause
The return_to parameter in the bulk edit endpoint lacks proper validation and sanitization. The application fails to whitelist allowed redirect destinations or validate that the target URL is within the same origin, allowing path traversal and protocol-relative URLs to bypass security checks.

## Attacker mindset
An attacker would leverage this vulnerability for credential harvesting by creating convincing phishing pages that mimic Shopify's login or admin interface. The attack is particularly effective because users trust the initial Shopify domain and expect legitimate redirects after administrative actions.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters, allowing only internal URLs
- Use URL parsing libraries to prevent path traversal attacks (/..// bypass)
- Reject protocol-relative URLs and ensure redirects use absolute paths starting with /
- Implement redirect validation on both client and server side
- Consider eliminating return_to parameters entirely where possible, defaulting to known safe locations
- Add security warnings before redirecting users outside the application domain
- Implement CSP headers to prevent XSS-assisted redirects

## Variant hunting
Search for other parameters named return_to, redirect, next, goto, url, redirect_uri across all endpoints
Test bulk operations endpoints (bulk delete, bulk assign, bulk update) for similar issues
Check if similar patterns exist in other admin workflows (checkout, settings, dashboard)
Test with encoded bypass techniques: %2e%2e%2f, double encoding, case variations
Verify if the vulnerability affects different resource types beyond Product

## MITRE ATT&CK
- T1598 - Phishing: Spearphishing Link (crafted malicious URLs sent to victims)
- T1187 - Forced Phishing (leveraging trusted domain to appear legitimate)

## Notes
This is a classic open redirect vulnerability with moderate severity. The /..// bypass technique suggests inadequate URL validation logic. The use of path traversal to reach a protocol-relative URL (//evil.com) is a common bypass pattern. The vulnerability's impact is amplified by user trust in the Shopify domain, making it effective for credential harvesting campaigns targeting merchants.

## Full report
<details><summary>Expand</summary>

Hi , 
I have found an open redirection issue when bulk editing resources.
#PoC:
Go to `https://<shop>.myshopify.com/admin/bulk?resource_name=Product&return_to=/..//evil.com` then click the **Close** button and you'll go to *evil.com* 

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
