# Cross-site scripting (XSS) on api.collabs.shopify.com via creator_redirect parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1672459 | https://hackerone.com/reports/1672459
- **Submitted:** 2022-08-17
- **Reporter:** kun_19
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected XSS, Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on api.collabs.shopify.com in the authentication flow via an unsanitized creator_redirect parameter. An attacker can craft a malicious URL with JavaScript payload that executes in the victim's browser context, allowing arbitrary code execution and potential credential theft or data exfiltration.

## Attack scenario
1. Attacker discovers the vulnerable creator_redirect parameter in the login endpoint accepts JavaScript URIs
2. Attacker crafts a malicious URL: https://api.collabs.shopify.com/creator/auth/login?creator_redirect=javascript:alert(document.domain) or more sophisticated payloads for credential harvesting
3. Attacker distributes the malicious link via phishing email, social media, or embedded in a trusted website to target content creators on the Shopify Collabs platform
4. Victim clicks the link while authenticated or logs in when prompted, and the JavaScript payload executes in the context of api.collabs.shopify.com
5. Attacker's payload exfiltrates authentication tokens, session cookies, or captures credentials for account takeover
6. Attacker gains ability to perform actions as the victim, access affiliate earnings, modify profile, or redirect to phishing pages

## Root cause
The creator_redirect parameter in the authentication endpoint is not properly validated or sanitized. The application fails to whitelist safe redirect URLs and does not prevent JavaScript protocol handlers (javascript:, data:, etc.) from being processed as valid redirect targets.

## Attacker mindset
The attacker recognizes that early-access creator platforms handle sensitive financial and social data. By targeting authenticated users during or after login, they can harvest session tokens or credentials to compromise influencer accounts, potentially for account takeover, financial fraud, or lateral movement into creator communities.

## Defensive takeaways
- Implement strict URL validation for all redirect parameters using a whitelist of safe domains
- Use URL parsing libraries to validate redirect targets before processing
- Reject non-HTTP(S) protocol schemes (javascript:, data:, vbscript:, etc.)
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Use the OWASP recommended approach: validate that redirects only go to same-origin or explicitly whitelisted domains
- Implement output encoding/escaping for any user-controlled data reflected in responses
- Conduct security review of all authentication and redirect flows across subdomains

## Variant hunting
Search for similar redirect parameters (redirect, return_to, next, back, callback, continue, destination) across collabs.shopify.com and related Shopify subdomains; test OAuth callback endpoints; check for POST-based redirects; examine API endpoints that handle URL fragments or query parameters after authentication

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability is particularly critical because it targets content creators with financial incentives, likely resulting in higher click-through rates on phishing attempts. The api subdomain distinction suggests potential for token exfiltration and API abuse. The report demonstrates basic PoC but real-world exploitation would likely involve credential harvesting or session hijacking payloads.

## Full report
<details><summary>Expand</summary>

## Summary:
Shopify collabs (collabs.shopify.com) is a new platform for content creators / influencers to discover and advertise the millions of brands of Shopify. The content creators can apply for different brands on this platform and get paid (affiliate marketing).
I discovered a cross-site scripting vulnerability on this quite new domain. 

## Steps To Reproduce:

  1. Visit https://www.shopify.com/collabs/find-brands and click on "Apply for early access"
  2. Create a new Shopify ID / account
  3. You get redirected to https://collabs.shopify.com/onboarding:  
{F1871170}
  4. Connect your social media account to your profile (e.g. Instagram), edit your content, etc.
  5. You should now be successfully registered  (early bird access - waiting list):  
{F1871169}
  6. As you are logged in, open the URL `https://api.collabs.shopify.com/creator/auth/login?creator_redirect=javascript:alert(document.domain)` and you will see that the JavaScript has triggered:  
{F1871171}



## Supporting Material:
[list any additional material (e.g. screenshots, video, etc)]

  * [attachment / reference]

## Impact

* Execution of JavaScript code in the victim's browser => Execution of any future API functions of api.collabs.shopify.com in the name of the victim
* Exfiltration of confidential data
* etc.

</details>

---
*Analysed by Claude on 2026-05-12*
