# Open Redirect in www.shopify.dev via result_url Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 842035 | https://hackerone.com/reports/842035
- **Submitted:** 2020-04-06
- **Reporter:** beerboy_ankit
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the Shopify developer documentation search results page where the result_url parameter fails to properly validate redirect destinations. An attacker can bypass internal URL validation by prepending an @ character to redirect users to arbitrary external domains.

## Attack scenario
1. Attacker identifies the search results page at shopify.dev/search/result with the result_url parameter
2. Attacker crafts a malicious URL with result_url=@www.attacker.com to bypass validation logic
3. Attacker shares the link via phishing email, social engineering, or ad placement targeting Shopify developers
4. Victim clicks the link from a trusted shopify.dev domain, reducing suspicion
5. Browser follows the redirect and user is taken to attacker's domain (phishing, credential theft, malware)
6. Attacker harvests credentials or redirects to credential harvesting page impersonating Shopify

## Root cause
The search results redirect handler validates URLs to ensure they point to shopify.dev resources but fails to account for the @ character used in authentication URLs (user:pass@host format). The validation logic likely checks if the URL starts with '/' or contains 'shopify.dev' without proper URL parsing that accounts for special characters that alter URL interpretation.

## Attacker mindset
The attacker recognized that standard validation filters (checking for absolute URLs or external domains) can be bypassed using URL syntax tricks. The @ symbol is a valid URL component that changes how browsers parse the authority section. This demonstrates understanding of URL RFC specifications and common validation shortcomings.

## Defensive takeaways
- Use strict URL validation with proper URL parsing libraries (URL constructor in JavaScript, urllib in Python) rather than string-based checks
- Implement allowlist validation for redirect destinations - only permit relative URLs starting with / or explicitly whitelisted domains
- Use the URL constructor to parse and validate URLs: new URL(userInput, baseURL) will throw on invalid syntax
- Avoid relying on string.includes() or string.startsWith() for URL validation as these don't account for URL component precedence
- Consider implementing redirect validation server-side with explicit domain checking and rejecting any URL with authentication components (@)
- Apply URL canonicalization before validation to normalize edge cases
- Test redirect handlers with special characters: @, :, //, \, encoded variants

## Variant hunting
Check for similar patterns in: search result pages, documentation navigation, API response handlers with URL parameters, parameter names like: redirect_to, return_url, next, callback, url, destination, back, exit_url. Look for @ bypass in other Shopify subdomains (help.shopify.com, community.shopify.com, partners.shopify.com) and examine similar e-commerce platforms' search and navigation features.

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1566.001 - Phishing: Spearphishing Attachment

## Notes
The @ character is a legitimate URL component used for basic authentication (user:pass@host) but is often mishandled in validation. This is a well-known bypass technique. The reporter correctly noted the potential for wider scope across Shopify infrastructure. The impact is primarily for phishing and social engineering attacks, as the trust in shopify.dev domain makes users less suspicious of clicks.

## Full report
<details><summary>Expand</summary>

## Summary
Reported vulnerability allows attacker for open/unknown redirect for victim user 

## Steps to reproduce

1) Go to https://shopify.dev/concepts/shopify-introduction
2) Click on search
3) Type ``` POC ``` in search box and hit enter 
4) Right click on first result displayed as ```POS``` and click on copy  link address which will look like below.
```
https://shopify.dev/search/result?query=poc&rank=1&result_gid=ae6c33f6-62d4-4ff2-966e-96c09267ee87&result_url=%2Ftools%2Fapp-bridge%2Factions%2Fpos&search_uuid=34eeea9d-2b99-4f86-bf00-807efd4036ba&suggested=false
```
5) Modify ```result_url``` parameter in link shown above to ```result_url=@www.facebook.com```

6) Final link will look like this
```
https://shopify.dev/search/result?query=poc&rank=1&result_gid=ae6c33f6-62d4-4ff2-966e-96c09267ee87&result_url=@www.facebook.com&search_uuid=34eeea9d-2b99-4f86-bf00-807efd4036ba&suggested=false

```
7) alternatively You can also directly  access below link for your convenience
https://shopify.dev/search/result?query=poc&rank=1&result_gid=ae6c33f6-62d4-4ff2-966e-96c09267ee87&result_url=@www.facebook.com&search_uuid=34eeea9d-2b99-4f86-bf00-807efd4036ba&suggested=false


Culprit for redirect is ``` @ ``` character which will bypass the logic implemented to redirect user to access resource on www.shopify.dev itself and follow url after ``` @ ``` 


Note: I am submitting this report as this bypass technique can be use to any other domain on Shopify if same logic is implemented and could leads attacker for wider attack scope.


Thanks you!

## Impact

Invalidated Redirect

</details>

---
*Analysed by Claude on 2026-05-24*
