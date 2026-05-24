# Open Redirect via CDN Asset Parameter - Shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 905737 | https://hackerone.com/reports/905737
- **Submitted:** 2020-06-22
- **Reporter:** zonduu
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, URL Redirection to Untrusted Site
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability was discovered in the /plus/get-cdn-asset endpoint of www.shopify.com through the 'asset' parameter. An attacker can craft a malicious URL to redirect users to arbitrary external domains, enabling phishing attacks and credential theft.

## Attack scenario
1. Attacker crafts a malicious URL: https://www.shopify.com/plus/get-cdn-asset?asset=http://evil.com/?
2. Attacker sends the link to victims via email, social media, or embeds it in phishing pages
3. Victim clicks the link, trusting the shopify.com domain
4. Application redirects victim to attacker-controlled domain (evil.com)
5. Victim, believing they are on a legitimate Shopify page, enters credentials or sensitive data
6. Attacker captures victim credentials and gains unauthorized access

## Root cause
Insufficient input validation and sanitization of the 'asset' parameter. The application does not verify that redirect destinations are within an allowlist of trusted domains, allowing arbitrary URL schemes (http://, https://) to be passed through and processed.

## Attacker mindset
Attackers seek open redirects on trusted domains to bypass user suspicion and security filters. Shopify is a high-value target due to merchant and customer trust; redirecting users to fake login pages would yield credentials for account takeovers, payment fraud, and data theft.

## Defensive takeaways
- Implement strict URL validation using allowlist/whitelist approach for redirect destinations
- Validate that redirect URLs belong to the same origin or pre-approved domains only
- Use URL parsing libraries to prevent bypass techniques (e.g., protocol confusion, double-encoding)
- Implement Content Security Policy (CSP) headers to restrict redirects
- Avoid user-controlled input in redirect logic; use indirect references instead
- Add security warnings before redirecting to external domains
- Conduct regular security audits of all URL-handling endpoints

## Variant hunting
Test other CDN/asset endpoints with similar parameter names: url, redirect, target, link, destination
Check for bypasses using protocol handlers: javascript:, data:, vbscript:
Test URL encoding variations: %68ttp://, //evil.com, ///evil.com
Attempt case variations: HTTP://, HtTp://
Try relative path traversal: //evil.com, \\evil.com
Investigate other Shopify subdomains and endpoints for similar patterns
Test parameter pollution: asset=http://good.com&asset=http://evil.com

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1598.004
- T1192

## Notes
This is a straightforward open redirect vulnerability with clear exploitation path. The minimal report suggests early-stage discovery. Shopify likely patched this quickly given their mature security program. The /plus path suggests targeting Shopify Plus merchants, a higher-value attack vector.

## Full report
<details><summary>Expand</summary>

Hello Shopify team,

I found an open redirect in www.shopify.com

Link:

- `https://www.shopify.com/plus/get-cdn-asset?asset=http://evil.com/?`

**Vulnerable parameter:** `asset`

## Impact

- Open redirect that can lead to phishing and other type of attacks.

Have a good day, zonduu.

</details>

---
*Analysed by Claude on 2026-05-24*
