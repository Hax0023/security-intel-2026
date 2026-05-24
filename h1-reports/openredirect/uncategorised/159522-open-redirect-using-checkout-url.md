# Open Redirect via return_url and checkout_url Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 159522 | https://hackerone.com/reports/159522
- **Submitted:** 2016-08-15
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
Shopify's login and logout endpoints fail to properly validate redirect destinations in return_url and checkout_url parameters, allowing attackers to redirect users to attacker-controlled domains. By chaining the open redirect with URL rewrites on a attacker-controlled Shopify store, victims can be redirected to arbitrary malicious websites.

## Attack scenario
1. Attacker creates a Shopify store and configures a URL redirect rule mapping /[attacker_store_id] to a malicious domain (evil.com)
2. Attacker crafts a phishing link using the victim's store logout endpoint with return_url parameter pointing to https://checkout.shopify.com/[attacker_store_id]
3. Victim clicks the link and is redirected through Shopify's logout flow, which validates the return_url as a Shopify domain
4. The return_url passes validation because it points to legitimate checkout.shopify.com domain
5. Victim's browser follows the redirect to checkout.shopify.com/[attacker_store_id], which triggers the attacker's URL rewrite rule
6. Victim is finally redirected to evil.com, appearing as though it came from Shopify's trusted domain

## Root cause
Insufficient validation of redirect destinations. The application validates that redirect URLs point to Shopify domains (checkout.shopify.com) but fails to verify that the specific path cannot be manipulated through store URL rewrites to redirect to external domains. The validation is domain-based rather than endpoint-based.

## Attacker mindset
An attacker could leverage this to conduct phishing attacks by making malicious redirects appear to originate from trusted Shopify domains, increasing victim trust. The attack is particularly effective because it chains two separate features: open redirect in Shopify's auth endpoints and URL rewrite capabilities on stores.

## Defensive takeaways
- Implement allowlist-based redirect validation rather than domain-based validation - whitelist specific trusted endpoints
- Validate that redirect destinations resolve to expected endpoints, not just domains
- Consider disabling redirects to user-controlled paths entirely for sensitive endpoints like login/logout
- Implement additional security headers like X-Frame-Options and CSP to limit impact of redirects
- Review URL rewrite/redirect features to prevent them from being abused to bypass authentication redirect protections
- Use relative redirects or POST-redirect-GET patterns when possible to avoid open redirects

## Variant hunting
Check other authentication endpoints (password reset, email verification) for similar redirect parameter validation
Test other Shopify domains (admin.shopify.com, partners.shopify.com) for return_url/redirect_uri parameters
Look for similar patterns in other Shopify APIs that accept redirect parameters
Test variations: redirect_to, next, continue, back, goto, returnURL parameters
Check if redirect validation can be bypassed with encoded characters (%2f, %3f) or protocol-relative URLs (//evil.com)

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (sending crafted Shopify links)
- T1583.001 - Acquire Infrastructure: Domains (attacker purchases domains for redirect targets)
- T1566.002 - Phishing: Phishing - Spearphishing Link (distributing malicious redirect links)

## Notes
The vulnerability requires social engineering to be effective, as the victim must click the attacker's link. However, the fact that the redirect appears to originate from checkout.shopify.com significantly increases the likelihood of user trust. This is a good example of how combining multiple legitimate features (auth redirects + URL rewrites) can create a security issue. The report demonstrates good security research methodology by providing concrete PoC steps and explaining the attack chain clearly.

## Full report
<details><summary>Expand</summary>

Hi , I would like to report an open redirect issue in `<account>.myshopify.com/account/logout` and `<account>.myshopify.com/account/login`
#Details:
Your application allow redirecting to `https://checkout.shopify.com/` through `https://<shop>.myshopify.com/account/logout?return_url=<url>` 
The page `https://checkout.shopify.com/<Store_id>` will display the 404 page of the store. 

Here is how this can be used for open redirection: 
1. Attacker creates a store then adds a new URL redirect with `/[Store_id]` in the **Old path** field and the malicious website(e.g:evil.com) in the **Redirect to** field.
{F112369}
2. Attacker sends the victim a link like this: 
`https://<victim>.myshopify.com/account/logout?return_url=https://checkout.shopify.com/[Attacker's_store_id] `
3. The victim will be redirected to the malicious website. 

#PoC:
`https://<account>.myshopify.com/account/logout?return_url=https://checkout.shopify.com/14372648`
This will redirect you to evil.com

`https://<account>.myshopify.com/account/login?checkout_url=https://checkout.shopify.com/14372648`
This will redirect you to evil.com after you login. 

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
