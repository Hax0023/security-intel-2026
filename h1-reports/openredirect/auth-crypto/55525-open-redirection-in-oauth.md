# Open Redirection in OAuth Authorization Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 55525 | https://hackerone.com/reports/55525
- **Submitted:** 2015-04-09
- **Reporter:** coolboss
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirection, OAuth Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The OAuth authorization endpoint in Shopify's admin panel performs an open redirect to the attacker-controlled redirect_uri even when an invalid scope is provided, allowing attackers to redirect users to arbitrary external sites. This can be exploited for phishing attacks by combining social engineering with credential harvesting on lookalike domains.

## Attack scenario
1. Attacker registers a legitimate Shopify application and obtains a client_id
2. Attacker crafts a malicious OAuth authorization URL with an intentionally invalid scope parameter and a redirect_uri pointing to a phishing domain
3. Attacker distributes this URL via social engineering, email, or messaging to target victims
4. Victim clicks the link and is presented with a legitimate-looking Shopify authorization consent screen
5. When the victim authorizes (or upon error handling), the system redirects them to the attacker's phishing domain with sensitive parameters in the URL
6. Attacker captures credentials or sensitive data from the victim on the fake site

## Root cause
The OAuth authorization endpoint lacks proper validation of error conditions and unconditionally redirects to the registered redirect_uri parameter even when scope validation fails. The application should validate the request before performing any redirection, or display errors on the platform's own domain rather than redirecting to untrusted origins.

## Attacker mindset
An attacker recognizes that OAuth flows inherently redirect users and that error conditions are often overlooked in security testing. By combining an invalid scope with a controlled redirect_uri, the attacker bypasses normal OAuth flow restrictions to create an open redirector, effectively turning the legitimate OAuth endpoint into a phishing vector.

## Defensive takeaways
- Validate all OAuth request parameters (client_id, redirect_uri, scope) BEFORE performing any redirect
- Display error messages on the authorization server's own domain, not the client's redirect_uri
- Implement whitelist validation for redirect_uri values registered with each application
- Add rate limiting and anomaly detection on authorization endpoints to detect phishing attempts
- Log and monitor invalid scope requests combined with suspicious redirect_uri patterns
- Consider implementing additional user confirmation when error redirects contain external URLs

## Variant hunting
Check other OAuth endpoints (token, revoke) for similar open redirect vulnerabilities
Test with various invalid parameters (invalid client_id, expired client_id, mismatched scope combinations)
Attempt to use localhost, 127.0.0.1, or internal IP addresses as redirect_uri values
Test with data: URIs, javascript: protocols in redirect_uri parameter
Check if error responses include user-controlled input that could lead to XSS when displayed
Investigate whether the hmac/signature parameters can be manipulated to bypass validation
Test redirect_uri with URL encoding bypasses (double encoding, unicode encoding)

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1021.005

## Notes
This is a classic open redirection vulnerability in an OAuth context. The key insight is that error handling paths are often overlooked, and attackers can chain this with social engineering for effective phishing. The presence of HMAC and signature parameters in the error response indicates the platform was attempting some form of validation, but it was bypassed or not applied consistently to error cases. The vulnerability is particularly dangerous because it leverages trust in the legitimate OAuth provider to enhance phishing credibility.

## Full report
<details><summary>Expand</summary>

Hello,

When we specify an `invalid` scope then the authorize url redirects to the site mentioned in `redirect_uri`. So, attacker can create an app and use it as open redirector to redirect victims to fake sites.
eg. Attacker can host same phishing page and hack the victims.

Proof Of Concept :
===============
1. I created an app 

<https://prans.myshopify.com/admin/oauth/authorize?client_id=616ce3efcd495007438000ad958a6629&scope=read_customers&redirect_uri=http://www.facebook.com/abc/>

2. Now, visit this ...

This will redirect ...

<https://prans.myshopify.com/admin/oauth/authorize?client_id=616ce3efcd495007438000ad958a6629&scope=a&redirect_uri=https://www.facebook.com/abc>

3. This will redirect with an error to ...
<https://www.facebook.com/abc?error=invalid_scope&hmac=07657fedf1815f84248dfc6c372ba002e3ea5041df849080269786ae732aed99&shop=prans.myshopify.com&signature=6ecc20da3eb66500d9245635ead45315&timestamp=1428607537>


Simple patch :
===========
Only a error should be shown and no redirection should take place so as to protect users.

Thanks,
Pranav



</details>

---
*Analysed by Claude on 2026-05-24*
