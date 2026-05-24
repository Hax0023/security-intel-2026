# Open Redirect On Login Panel

## Metadata
- **Source:** HackerOne
- **Report:** 473064 | https://hackerone.com/reports/473064
- **Submitted:** 2018-12-29
- **Reporter:** chiraggupta8769-
- **Program:** Zomato
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirects and Forwards
- **CVEs:** None
- **Category:** uncategorised

## Summary
The login panel at zomato.com contains an unvalidated open redirect vulnerability via the redirect_url parameter. After successful authentication, users are redirected to any attacker-controlled URL without validation, enabling phishing and credential theft attacks.

## Attack scenario
1. Attacker crafts a malicious URL: https://www.zomato.com/login?redirect_url=https://phishing-site.com/fake-zomato-login
2. Attacker sends the link to Zomato users via email, SMS, or social media as a legitimate login prompt
3. Victim clicks the link and sees the legitimate Zomato login page, building trust
4. Victim enters their credentials and submits the login form
5. After authentication succeeds, the user is redirected to the attacker's phishing site
6. Attacker captures additional sensitive information or installs malware on victim's device

## Root cause
The application fails to validate or whitelist the redirect_url parameter, directly using user-supplied input for post-login redirection without checking if the target is an allowed domain

## Attacker mindset
An attacker would leverage this vulnerability to conduct sophisticated phishing campaigns by making malicious redirects appear to come from a trusted domain. The post-authentication redirect increases victim trust since they've already successfully logged in, making credential harvesting more effective.

## Defensive takeaways
- Implement whitelist-based validation for all redirect parameters, only allowing predefined trusted domains
- Use relative URLs instead of absolute URLs when possible to prevent cross-domain redirects
- Validate redirect destinations against a whitelist of allowed paths within the application
- Implement Content Security Policy (CSP) headers to restrict redirect destinations
- Add user confirmation dialogs when redirecting to external URLs
- Log all redirect attempts for security monitoring and anomaly detection
- Regularly audit all endpoints that accept redirect parameters during code review

## Variant hunting
Search for other redirect parameters: redirect, return_url, return_to, continue_url, next, target, goto, url, forward
Test redirect vulnerabilities on password reset, logout, OAuth callback endpoints
Check for double-encoding or alternative encoding schemes (URL encoding variations) to bypass simple filters
Test with protocol-relative URLs (//attacker.com) and data URIs
Examine API endpoints that might accept redirect parameters in JSON or form bodies
Look for chained redirects where multiple parameters could bypass single-layer validation

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1187

## Notes
This is a classic unvalidated redirect vulnerability that directly enables phishing attacks. The reporter demonstrated the vulnerability on mobile browsers (Chrome Android, Firefox Android), indicating it affects mobile users. The simplicity of the exploit (single parameter manipulation) suggests the application has minimal input validation on this endpoint. Post-authentication redirects are particularly dangerous as they bypass user skepticism - victims believe they've successfully authenticated before being redirected.

## Full report
<details><summary>Expand</summary>

**Summery**
Hey There are a open Redirect on your login panel

**Platform(s) Affected:** Website

## Browsers Verified In [If Applicable]:

  * Chrome For Android
  * Firefox For Android

## Steps To Reproduce:

  1. Go To This Url :- https://www.zomato.com/login?redirect_url=https://askdcodes.org
  2. Then login there
  3. boom you got Redirected to askdcodes.org

## Supporting Materials ##
Attaching A Video Poc

## Impact

Any Attacker can Redirect your users to malicious website

</details>

---
*Analysed by Claude on 2026-05-24*
