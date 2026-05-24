# SSO through Odnoklassniki uses HTTP instead of HTTPS, enabling credential theft and CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 703759 | https://hackerone.com/reports/703759
- **Submitted:** 2019-09-29
- **Reporter:** matthijsmelissen
- **Program:** Badoo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Transport (CWE-319), Cross-Site Request Forgery (CSRF), Man-in-the-Middle (MITM), Credential Theft
- **CVEs:** None
- **Category:** uncategorised

## Summary
Badoo's Single Sign-On integration with Odnoklassniki redirects users to an HTTP endpoint instead of HTTPS, allowing attackers to intercept credentials or perform CSRF attacks. An attacker on the same network can either steal Odnoklassniki credentials presented on the unencrypted connection or hijack the authentication flow by intercepting the state parameter and authorization code.

## Attack scenario
1. Attacker positions themselves on a shared network (e.g., rogue WiFi hotspot)
2. Victim visits https://badoo.com/nl/signin/ and clicks 'Odnoklassniki' SSO option
3. Badoo redirects victim to unencrypted http://www.odnoklassniki.ru/oauth/authorize endpoint
4. Attacker intercepts HTTP traffic and either: (a) serves a fake login page to harvest credentials, or (b) captures the state parameter and authorization code
5. Attacker either logs into victim's Badoo account with stolen Odnoklassniki credentials, or completes CSRF flow by tricking victim into visiting attacker's malicious link containing captured authorization codes
6. Attacker gains unauthorized access to victim's Badoo account

## Root cause
OAuth redirect from Badoo to Odnoklassniki authentication endpoint uses HTTP instead of HTTPS, violating the OAuth 2.0 security requirement that authentication endpoints must use TLS/SSL. The state parameter and authorization code are exposed in plaintext on an unencrypted channel.

## Attacker mindset
An attacker with network-level access (shared WiFi, ISP compromise, etc.) can easily intercept unencrypted OAuth flows. The attack requires minimal sophistication: passive MITM interception for credential theft, or active redirection/CSRF for account takeover. The attacker recognizes that most users won't notice the http:// URL in redirects.

## Defensive takeaways
- Always enforce HTTPS for all OAuth 2.0 endpoints, including third-party identity provider redirects
- Implement HSTS (HTTP Strict-Transport-Security) headers to prevent downgrade attacks
- Use HTTPS scheme for all external redirects, especially those containing sensitive parameters (state, code, tokens)
- Validate that all authentication flows use encrypted channels end-to-end
- Consider certificate pinning for critical authentication endpoints
- Implement Content Security Policy (CSP) to mitigate MITM redirect attacks
- Audit all SSO integrations to ensure consistent HTTPS enforcement across all providers

## Variant hunting
Check if other SSO providers (Google, Facebook, VK, etc.) on Badoo use HTTP redirects
Review all OAuth 2.0 integrations for mixed-content scenarios (HTTPS page loading HTTP resources)
Test whether authorization codes from HTTP flows can be replayed across different clients
Examine if state parameter validation prevents CSRF across multiple SSO flows
Check if redirect_uri validation allows attacker-controlled domains
Verify HTTPS enforcement on redirect_uri endpoints in OAuth callbacks
Audit for similar protocol downgrade vulnerabilities in password reset flows, email verification, or other authentication mechanisms

## MITRE ATT&CK
- T1557.002
- T1187
- T1192
- T1598.003
- T1111
- T1056.004

## Notes
This is a clear instance of security misconfiguration in OAuth 2.0 implementation. The vulnerability is made worse because it affects the initial authentication flow—the most critical security boundary. The HTTP redirect is particularly egregious because it undermines the entire purpose of using HTTPS on the originating Badoo login page. The state parameter's presence in the HTTP URL is a secondary CSRF vector that could allow login-time account hijacking without even knowing the victim's credentials.

## Full report
<details><summary>Expand</summary>

SUMMARY
When using single-sign on through odnoklassniki, the user is sent to an http (non-https) URL, allowing an attacker (under some conditions) to log in to the victim's Badoo account by stealing odnoklassniki credentials, as well as to execute a CSRF-attack on the log-in form.

RECOMMENDATION
Let https://badoo.com/ok/authorize.phtml?rt=060285&js_use_scheme=https redirect to https://www.odnoklassniki.ru rather than the http version.

STEPS TO REPRODUCE
1) The victim navigates to https://badoo.com/nl/signin/ and selects 'odnoklassniki'
2) The victim is forwarded to http://www.odnoklassniki.ru/oauth/authorize?response_type=code&display=popup&client_id=126351872&scope=VALUABLE_ACCESS%3BGET_EMAIL&state=<state>&redirect_uri=https%3A%2F%2Fbadoo.com%2Fexternal%2Fredirector.phtml

Impact 1:
3) The attacker intercepts the http traffic and presents the victim a fake odnoklassniki log-in page
4) The attacker intercepts the odnoklassniki credentials entered by the victim
5) The attacker uses the intercepted odnoklassniki credentials to log in to the victim's Badoo account

Impact 2:
3) The attacker intercepts the URL at http://www.odnoklassniki.ru/ to which the victim is forwarded (which notably includes the state variable, which is connected to the victim's session)
4) The attacker browses to this URL and enters its own odnoklassniki credentials
5) The attacker intercepts the URL returning to https://badoo.com/external/redirector.phtml (including its parameters) and invites the victim to visit this URL
6) The attacker is now logged in to Badoo on the victim's device

## Impact

Impact 1:
The attacker can log in to the victim's Badoo account by stealing odnoklassniki credentials, under the following conditions:

* The attacker can modify traffic between the user and badoo.com (e.g. the user is connected to a rogue access point)
* The victim is willing to enter his odnoklassniki credentials on a http version of the site

Impact 2:
The attacker can execute a CSRF attack on the log-in form (i.e. the attacker log himself in to badoo.com on the victim's browser), under the following conditions:

* The attacker can intercept traffic between the user and badoo.com (e.g. the attacker is connected to the same unprotected wifi network)
* The attacker succeeds in causing the victim to browse to a URL provided by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
