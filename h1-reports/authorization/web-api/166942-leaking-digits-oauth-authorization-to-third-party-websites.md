# Digits OAuth Authorization Token Leakage via Unvalidated Callback URL

## Metadata
- **Source:** HackerOne
- **Report:** 166942 | https://hackerone.com/reports/166942
- **Submitted:** 2016-09-08
- **Reporter:** akhil-reni
- **Program:** Digits (Twitter/Fabric)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Broken Authentication, Open Redirect, OAuth 2.0 Misconfiguration, Insufficient Callback URL Validation
- **CVEs:** None
- **Category:** web-api

## Summary
Digits OAuth implementation accepts arbitrary callback URLs with any subdomain or path under fabric.io domain, allowing attackers to redirect authorization tokens to third-party websites. The vulnerability can be chained with stored XSS or social engineering to leak OAuth tokens to attacker-controlled domains.

## Attack scenario
1. Attacker crafts malicious Digits OAuth login link with callback_url pointing to attacker-controlled page on fabric.io (e.g., https://fabric.io/kits/ios/stripe)
2. Victim clicks the link and authenticates with Digits, granting authorization
3. OAuth token is sent to attacker's controlled fabric.io path during redirect
4. Attacker embeds link from step 1 in victim's browser context (e.g., within fabric.io issue notes)
5. When victim clicks embedded external link (e.g., stripe.com), token can be leaked via Referer header or URL parameter manipulation
6. Attacker can now impersonate the victim and access their Digits-connected services

## Root cause
Callback URL validation only checks the host (fabric.io) but does not validate the path or subdomain against a whitelist of legitimate callback endpoints. This allows attackers to craft valid-looking callback URLs pointing to arbitrary fabric.io paths including user-generated content areas.

## Attacker mindset
An attacker recognizes that permissive callback URL validation combined with a large platform (fabric.io) creates attack surface. By leveraging user-generated content (issue notes) and relying on social engineering (clicking links), they can execute a sophisticated attack that appears to originate from trusted infrastructure while exfiltrating sensitive OAuth tokens.

## Defensive takeaways
- Implement strict whitelist validation for OAuth callback URLs - validate exact path, not just domain
- Use cryptographic state parameters and PKCE for OAuth flows to prevent token leakage
- Never accept user-controlled paths in callback URL validation logic
- Implement proper URL sanitization and encoding when displaying user-generated content
- Monitor and log all OAuth authorization events with callback URL details
- Educate users about not clicking suspicious links within authenticated sessions
- Implement Content-Security-Policy headers to prevent open redirects within trusted domains

## Variant hunting
Test other OAuth providers integrating with Fabric for similar callback URL bypass patterns
Check if consumer_secret can be leaked through similar subdomain/path manipulation
Investigate whether other Fabric services (Crashlytics, etc.) have similar OAuth implementations
Test for stored XSS in issue notes/comments that could be chained with this vulnerability
Search for similar validation flaws in other platforms accepting organization-wide callback URLs
Test parameter pollution or encoding tricks (../ traversal, URL encoding) to bypass callback validation

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1606.002 - Forge Web Credentials: Browser Cookies
- T1539 - Steal Web Session Cookie
- T1621 - Multi-Factor Authentication Interception
- T1187 - Forced Authentication

## Notes
This vulnerability demonstrates the danger of validating only the domain component of security-sensitive URLs. The attacker's second scenario is particularly sophisticated as it chains stored XSS (ability to inject notes in issue tracker) with OAuth token leakage, creating a complete attack chain requiring only initial access to the organization. The fact that any fabric.io path is accepted suggests callback URL validation was likely implemented as a simple string prefix check rather than a proper URI parsing and whitelist comparison.

## Full report
<details><summary>Expand</summary>

**Hi,**

While authenticating digits to my Fabric account i have noticed that the callback_url is not solid i.e. any sub domain or any path is accepted as callback_url with host as fabric.io.
This issue can be exploited by leaking the authorization token to third party websites (websites mentioned on kit's page)

**Steps to reproduce:**
- Go to https://www.digits.com/login?consumer_key=YlNgs6zwm4QLmrzJBwRK3FcR5&callback_url=https://fabric.io/kits/ios/stripe&host=https://fabric.io
- Give access to Digits
- Now you will be redirected to https://fabric.io/kits/ios/stripe
- While on stripe kits page click on the stripe website URL (https://stripe.com)
- The authorization token will be leaked to stripe.com 
{F118436}

This issue can also be exploited on our organization member by actually leaking the consumer secret to our domain. 

**Steps to reproduce**
- Add the victim to your organization
- Create an crash issue under fabric
- add a note to that issue for ex: https://wesecureapp.com
- Note down the issue URL
{F118437}
Ex: https://fabric.io/img-srcx-onerrorprompt15/android/apps/app.myapplication/issues/56207e21f5d3a7f76bd5c20c
- Change the call back URL to issue url
https://www.digits.com/login?consumer_key=YlNgs6zwm4QLmrzJBwRK3FcR5&callback_url=https://fabric.io/img-srcx-onerrorprompt15/android/apps/app.myapplication/issues/56207e21f5d3a7f76bd5c20c&host=https://fabric.io
- Give digits permission
- You will be redirected to issue
- Now click the link in the notes and the OAuth token will be leaked to the attacker controlled domain.
{F118438}

**Regards,
Akhil**

</details>

---
*Analysed by Claude on 2026-05-24*
