# Open Redirect and XSS in supporthiring.shopify.com via Double Slash Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 158434 | https://hackerone.com/reports/158434
- **Submitted:** 2016-08-11
- **Reporter:** jamesclyde
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Open Redirect, Unvalidated Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
The supporthiring.shopify.com application contains an open redirect vulnerability in the 'path' parameter that can be bypassed using URL-encoded double slashes (%2F%2F). Attackers can craft malicious links to redirect victims to arbitrary external domains, enabling phishing and credential theft attacks.

## Attack scenario
1. Attacker identifies the vulnerable 'path' parameter in supporthiring.shopify.com/apps/locksmith/resource/pages/gauntlet-challenge
2. Attacker discovers that standard open redirect protections are in place but can be bypassed with double slash encoding (%2F%2F)
3. Attacker crafts malicious URL: http://supporthiring.shopify.com/apps/locksmith/resource/pages/gauntlet-challenge?path=%2F%2Fevil.com
4. Attacker distributes link via phishing email or social engineering targeting Shopify users
5. Victim clicks link and sees legitimate 404 error page from trusted Shopify domain for 2 seconds
6. Browser automatically redirects victim to attacker-controlled evil.com where credentials or sensitive data can be harvested

## Root cause
The application implements blacklist-based URL validation that checks for suspicious path patterns but fails to account for URL-encoded bypass techniques. The parser likely normalizes single slashes but processes double slashes before normalization, allowing the bypass of redirect destination validation.

## Attacker mindset
An attacker recognizes that input validation relying on character matching can be evaded through encoding. The delayed redirect (2 second 404 page) creates false legitimacy, making the redirect appear part of normal site behavior rather than suspicious. This is ideal for credential harvesting or malware distribution campaigns targeting Shopify merchants.

## Defensive takeaways
- Implement whitelist-based URL validation instead of blacklist approaches; only allow redirects to known safe destinations
- Decode and normalize all URL input before validation to prevent encoding-based bypasses
- Apply URL parsing using language-native URI parsing libraries that handle encoding consistently
- Implement strict protocol validation (http/https only) and reject uncommon schemes
- Avoid showing delay before redirects as it obscures the redirect action from users
- Use Content-Security-Policy headers to restrict redirect destinations at browser level
- Validate redirect URLs against a strict pattern: only same-origin or explicitly whitelisted external domains
- Consider warning users with interstitial pages for external redirects rather than automatic navigation

## Variant hunting
Search for similar bypass patterns: encoded slashes (%2F), backslashes (%5C), unicode encodings (\u002F), protocol-relative URLs (//), data: URIs, javascript: URIs, newline injection (%0a%0d), and combinations like %252F (double encoding). Test other Shopify subdomains for identical vulnerable parameters. Look for similar redirect parameters: redirect=, return=, next=, goto=, url=, continue=.

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Email
- T1598.002 - Phishing: Adversary-in-the-middle
- T1036.005 - Masquerading: Match Legitimate Name or Location
- T1190 - Exploit Public-Facing Application

## Notes
The vulnerability affects all browsers, indicating a server-side validation bypass rather than browser-specific issue. The 2-second delay before redirect is a UX choice that inadvertently aids attackers by providing time for page render before redirect. The report demonstrates proof-of-concept but severity assessment was limited by lack of XSS payload details mentioned in title but not demonstrated in writeup. Double slash encoding bypassing validation suggests the security implementation was incomplete - likely checking for specific string patterns without proper URL parsing.

## Full report
<details><summary>Expand</summary>

Hello,

The users can be redirected to some other site which is in control of the attacker from 

Vulnerable parameter: path=

You have a protection here at path= but it bypass the parameter if you add a double slash, like %2F%2F.

Let's say user is attacker asked victim to came to this page: :
http://supporthiring.shopify.com/apps/locksmith/resource/pages/gauntlet-challenge?&path=%2F%2Fevil.com

Victim will be see a 404 error page and after 2 seconds he will be redirected to: https://evil.com

These can be controlled by the attacker and used in other attacks

Works in all browsers!!




</details>

---
*Analysed by Claude on 2026-05-12*
