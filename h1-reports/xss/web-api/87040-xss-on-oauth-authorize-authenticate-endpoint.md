# XSS on OAuth authorize/authenticate endpoint via unsanitized oauth_callback parameter

## Metadata
- **Source:** HackerOne
- **Report:** 87040 | https://hackerone.com/reports/87040
- **Submitted:** 2015-09-02
- **Reporter:** filedescriptor
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, OAuth Implementation Flaw
- **CVEs:** None
- **Category:** web-api

## Summary
Twitter's OAuth authorization endpoints on twitter.com and api.twitter.com fail to properly sanitize the oauth_callback parameter in the redirection page, allowing attackers to inject arbitrary JavaScript code. An attacker can craft a malicious OAuth request token containing JavaScript payload in the callback parameter, which executes when a victim visits the authorization page.

## Attack scenario
1. Attacker crafts a malicious oauth_callback parameter containing JavaScript payload (e.g., javascript://"><script>alert(document.domain)</script>)
2. Attacker obtains an OAuth request token from Twitter's API with the malicious callback parameter
3. Attacker tricks victim into visiting the Twitter authorize/authenticate page with the malicious request token
4. Victim clicks 'Authorize app' button on the authorization page
5. Unsanitized oauth_callback parameter is reflected in the redirection page HTML
6. Victim's browser executes the injected JavaScript in the context of twitter.com domain, potentially stealing credentials or session tokens

## Root cause
The OAuth authorization endpoint constructs the redirection page without properly sanitizing or encoding the oauth_callback parameter before including it in the HTML response. The parameter is reflected directly into the page without HTML entity encoding or Content Security Policy (CSP) protection, allowing script injection.

## Attacker mindset
An attacker seeks to exploit the OAuth flow to conduct account takeovers or credential theft by injecting malicious scripts that execute in the victim's authenticated session. By leveraging the trust users place in Twitter's authorization flow, the attacker can steal authentication tokens, session cookies, or sensitive user data without requiring separate phishing or malware.

## Defensive takeaways
- Implement strict output encoding/HTML entity encoding for all user-supplied parameters reflected in HTTP responses
- Apply Content Security Policy (CSP) headers with script-src restrictions to prevent inline script execution
- Validate and whitelist the oauth_callback parameter against expected URL schemes (https only, specific domains)
- Use HTTP-only and Secure flags on session cookies to prevent JavaScript access
- Implement input validation to reject callback URLs with dangerous schemes (javascript:, data:, vbscript:)
- Conduct security code review of OAuth implementation, particularly parameter handling in redirect/authorization flows
- Perform XSS testing specifically on OAuth endpoints and callback parameter handling
- Consider using a dedicated OAuth library with built-in protections rather than custom implementation

## Variant hunting
Check other OAuth parameters (state, client_id) for similar XSS vulnerabilities
Test api.twitter.com and twitter.com for endpoint consistency in sanitization
Look for similar issues in token revocation, logout, and error pages
Test different encoding/bypass techniques (double encoding, case variation, unicode escapes, null bytes)
Check if POST-based OAuth flows have the same vulnerability
Test callback parameter on related endpoints (oauth/authorize vs oauth/authenticate)
Search for other OAuth implementations in Twitter's ecosystem for similar flaws

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The researcher noted that the vulnerability affects both twitter.com and api.twitter.com using the same endpoints. The PoC explicitly mentions the need for browsers without CSP implementation, suggesting Twitter may have implemented CSP as a defense but not properly fixed the underlying sanitization issue. The oauth_callback parameter is an inherent part of OAuth spec but implementations must sanitize it to prevent injection attacks.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report an issue where certain endpoints on twitter.com and api.twitter.com is vulnerable to XSS.

##Detail
The redirection page after authorization/authentication does not sanitize the *oauth_callback* parameter.

##PoC
1. Go to http://innerht.ml/pocs/twitter-oauth-xss (Please use IE or something that hasn't implemented CSP)
2. Click on Authorize app
3. Alert pops up

Note: it also affects api.twitter.com as they both have the same endpoints

##Repo step
1. Obtain the request token (https://api.twitter.com/oauth/request_token) where parameter *oauth_callback* contains HTML like ```javascript%3A%2F%2F"><script>alert(document.domain)</script>```
2. Redirect the victim to the authorize/authenticate page with the token

</details>

---
*Analysed by Claude on 2026-05-12*
