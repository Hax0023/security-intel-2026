# Open Redirect in OIDC Logout Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1369806 | https://hackerone.com/reports/1369806
- **Submitted:** 2021-10-13
- **Reporter:** kauenavarro
- **Program:** Nutanix
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the OIDC logout endpoint where the `post_logout_redirect_uri` parameter is not properly validated, allowing attackers to redirect authenticated users to arbitrary external domains. By crafting a malicious logout URL, an attacker can perform phishing attacks or credential theft by redirecting users to attacker-controlled sites.

## Attack scenario
1. Attacker identifies the vulnerable logout endpoint at /api/iam/authn/v1/oidc/logout
2. Attacker crafts a malicious URL with post_logout_redirect_uri parameter pointing to evil.com
3. Attacker sends phishing email to Nutanix users with the crafted logout URL disguised as legitimate
4. Victim clicks the link believing they are logging out from legitimate Nutanix service
5. Application issues HTTP 302 redirect to attacker's malicious domain without validation
6. Victim lands on phishing page mimicking Nutanix login, entering credentials which are captured by attacker

## Root cause
The logout endpoint fails to validate that the `post_logout_redirect_uri` parameter matches an allowlist of approved redirect destinations. The parameter value is directly used in the HTTP Location header without sanitization or domain validation, enabling arbitrary external redirects.

## Attacker mindset
Attacker seeks to leverage the trust users have in legitimate Nutanix logout flows to redirect them to credential harvesting pages. The vulnerability is particularly effective because users explicitly expect to be redirected during logout, making the attack less suspicious than a random redirect.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters, rejecting any URLs not on approved domain list
- Validate redirect URIs against configured allowlist before processing HTTP 302 responses
- Use URL parsing libraries to properly validate scheme and domain, preventing bypass techniques like protocol-relative URLs or data URIs
- Implement Content-Security-Policy headers to restrict redirect destinations at browser level
- Log and monitor redirect parameters for suspicious patterns and external domain redirects
- Follow OpenID Connect specifications for post_logout_redirect_uri validation requirements
- Conduct security review of all authentication/authorization endpoints for similar redirect vulnerabilities

## Variant hunting
Check other OIDC/OAuth endpoints for similar unvalidated redirect parameters (callback_url, return_url, redirect_to, etc.)
Test authorization endpoints (/oauth/authorize, /oidc/authorize) for open redirects
Examine error pages and success pages that may accept redirect parameters
Review application for other post-authentication redirect flows lacking validation
Test with protocol-relative URLs (//evil.com), data URIs, and JavaScript URLs to bypass naive filters

## MITRE ATT&CK
- T1598.003
- T1598.004
- T1566.002
- T1080

## Notes
This is a staging environment endpoint (stage.test.dev-iam.xi.nutanix.com), suggesting the vulnerability may exist in production as well. The OIDC logout endpoint is particularly sensitive because users expect redirection as part of normal logout flow, making this an effective phishing vector. The vulnerability references indicate this is a known attack pattern in OIDC implementations.

## Full report
<details><summary>Expand</summary>

Open Redirect Vulnerability
Hello , found open redirect in https://stage.test.dev-iam.xi.nutanix.com/api/iam/authn/v1/oidc/logout?post_logout_redirect_uri=.

Go to

https://stage.test.dev-iam.xi.nutanix.com/api/iam/authn/v1/oidc/logout?post_logout_redirect_uri=http://evil.com&id_token_hint=test

curl -I "https://stage.test.dev-iam.xi.nutanix.com/api/iam/authn/v1/oidc/logout?post_logout_redirect_uri=http://evil.com&id_token_hint=test"

HTTP/2 302 
content-type: text/html; charset=utf-8
location: http://evil.com
date: Wed, 13 Oct 2021 20:55:57 GMT
x-envoy-upstream-service-time: 2
server: envoy


##Reference

https://hackerone.com/reports/504751
https://portswigger.net/kb/issues/00500100_open-redirection-reflected

## Impact

An attacker can use this vulnerability to redirect users to other malicious websites, which can be used for phishing and similar attacks

</details>

---
*Analysed by Claude on 2026-05-24*
