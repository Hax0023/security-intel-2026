# Open Redirect in Shopify App Callback Handler

## Metadata
- **Source:** HackerOne
- **Report:** 226408 | https://hackerone.com/reports/226408
- **Submitted:** 2017-05-05
- **Reporter:** pappan
- **Program:** Shopify
- **Bounty:** Unknown
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Shopify app callback endpoint at assistant-client.meteorapp.com/shopify/callback accepts an untrusted 'shop' parameter that is reflected in redirects without proper validation. An attacker can craft malicious URLs to redirect users to arbitrary domains during the OAuth flow, enabling phishing and social engineering attacks.

## Attack scenario
1. Attacker crafts malicious URL with shop parameter pointing to attacker-controlled domain: https://assistant-client.meteorapp.com/shopify/callback?code=xxx&hmac=yyy&shop=attacker.com&timestamp=zzz
2. Attacker sends link to victim via email, messaging, or social engineering
3. Victim clicks link, believing they are completing legitimate Shopify OAuth flow
4. Application processes callback and redirects to attacker.com (fake Shopify login page)
5. Victim enters credentials thinking they're authenticating with Shopify
6. Attacker captures credentials or plants malware for follow-on attacks

## Root cause
The 'shop' parameter is used in a redirect operation without validating that the domain is a legitimate Shopify shop domain (*.myshopify.com). The application trusts user-supplied input for redirect destinations.

## Attacker mindset
An attacker would recognize that OAuth callback flows are trust-sensitive operations. By injecting arbitrary domains into the shop parameter, they can break out of the intended Shopify ecosystem and redirect victims to credential harvesting pages. This is particularly effective because victims expect to be redirected during OAuth flows.

## Defensive takeaways
- Implement whitelist-based validation: only allow redirects to domains matching *.myshopify.com pattern
- Validate the 'shop' parameter against a known list of legitimate Shopify shops before using it in redirects
- Use a redirect allowlist rather than relying on blacklists or pattern matching alone
- Implement strict URL validation that rejects any non-Shopify domains
- Consider not using user-supplied input in redirect decisions; instead, look up the shop from your backend based on authenticated session
- Add security headers like X-Frame-Options and Content-Security-Policy to prevent framing and script injection
- Log and alert on redirect attempts to non-whitelisted domains for detection of exploitation attempts

## Variant hunting
Check other callback endpoints (not just /shopify/callback) for similar issues
Test other parameters (code, hmac, timestamp) for injection/validation flaws
Look for similar patterns in other Shopify app integrations on meteorapp.com
Check if the HMAC validation can be bypassed with arbitrary shop values
Test if relative redirects (../ or //) are accepted
Check for data exfiltration via query parameters in redirects

## MITRE ATT&CK
- T1598.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing: Spearphishing Link (via trusted service)
- T1566 - Phishing

## Notes
The reporter mentions uncertainty about meteorapp.com ownership and explicitly requests not to be marked as NA. This is a valid open redirect that could be chained with social engineering. The 'shop' parameter appears to be attacker-controllable despite being part of an OAuth callback, indicating insufficient input validation. The HMAC parameter suggests some security measures were attempted, but the shop parameter was overlooked in the validation logic.

## Full report
<details><summary>Expand</summary>

Hi,

The Amazon Alexa app when installing calls a URL https://assistant-client.meteorapp.com/shopify/callback?code=6aae881ab9c4f12d5b264e6c871a108a&hmac=6109806a12b0439d6a2dce2d547344eb1c2c53e9691259f39eefbb93b9c9c97b&shop=pappuza-2.myshopify.com&timestamp=1494008598

The **shop** parameter will accept any domain and redirects. 
Don't know whether meteorapp.com is controlled by you but reporting this as this found as made by shopify in the app store.

If not going to resolve this, please do not mark as NA. I will do the needful.

</details>

---
*Analysed by Claude on 2026-05-24*
