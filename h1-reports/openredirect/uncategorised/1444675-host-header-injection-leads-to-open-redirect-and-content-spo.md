# Host Header Injection leads to Open Redirect and Content Spoofing

## Metadata
- **Source:** HackerOne
- **Report:** 1444675 | https://hackerone.com/reports/1444675
- **Submitted:** 2022-01-09
- **Reporter:** oblivionlight
- **Program:** Omise
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Host Header Injection, Open Redirect, Content Spoofing, Text Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Omise dashboard is vulnerable to Host Header Injection through the X-Forwarded-Host header, enabling attackers to perform Open Redirects and Content Spoofing attacks. An authenticated attacker can manipulate the host header to redirect users to arbitrary domains or display spoofed content under the trusted domain context.

## Attack scenario
1. Attacker crafts a request to https://dashboard.omise.co/signin or /settings with a malicious X-Forwarded-Host header (e.g., X-Forwarded-Host: bing.com)
2. Attacker authenticates to the dashboard with valid credentials and ensures email is unverified to trigger the verification email flow
3. Server processes the request and uses the attacker-controlled X-Forwarded-Host header when generating URLs for email verification or settings pages
4. Application generates redirect URLs or content using the injected host header, pointing to attacker's malicious domain
5. User receives email with link or visits settings page, which now contains URLs/content pointing to attacker-controlled infrastructure
6. User clicks the malicious link or interacts with spoofed content, believing it originates from the trusted Omise domain

## Root cause
The application fails to properly validate and sanitize the X-Forwarded-Host header and uses it to construct redirect URLs and generate dynamic content without verifying it matches the expected application domain. The server trusts the X-Forwarded-Host header without implementing whitelist validation or canonicalization.

## Attacker mindset
An attacker would recognize that applications behind reverse proxies or load balancers commonly use X-Forwarded-Host for URL generation, making this a high-probability attack vector. The ability to achieve both open redirects and content spoofing with a single header injection demonstrates the critical nature of proper host validation, with potential for phishing campaigns and credential harvesting.

## Defensive takeaways
- Implement strict whitelist validation of the Host and X-Forwarded-Host headers against expected application domains
- Never use user-supplied or proxy headers directly in redirect URLs or content generation without validation
- Configure reverse proxies to only accept X-Forwarded-Host from trusted internal sources and strip it from client requests
- Use absolute URLs with hardcoded application domain for email verification links and sensitive redirects
- Implement Content Security Policy (CSP) headers to restrict redirect destinations
- Log and alert on mismatches between Host header and X-Forwarded-Host header values
- Conduct security review of all URL generation logic, particularly in authentication and email verification flows

## Variant hunting
Test X-Forwarded-Proto header injection for protocol switching attacks
Check for X-Forwarded-For header injection affecting security logging or rate limiting
Test other proxy headers: X-Original-Host, X-Host, Forwarded header (RFC 7239)
Examine OAuth/SAML redirect_uri parameters for similar host validation weaknesses
Review password reset flows for equivalent host header injection vulnerabilities
Test API endpoints for host header injection affecting CORS or CSRF token validation
Check if host header injection affects API response headers or HSTS policies

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1187

## Notes
This is a chain of related vulnerabilities stemming from improper host header handling. The impact is particularly severe because it affects authenticated users during email verification flows. The vulnerability requires authentication, slightly reducing severity, but the attack is trivial to exploit once authenticated. Video proof-of-concept was provided but not included in this analysis.

## Full report
<details><summary>Expand</summary>

## Summary:

1.) Open Redirection
The https://dashboard.omise.co/test/dashboard website is vulnerable to an Open Redirection flaw if the server receives a crafted X-Forwarded-Host header.

Description:
Open Redirect is a vulnerability in which the attacker manipulates a web page to redirect the users to unknown destinations (malicious/phishing destinations in most cases).

Steps To Reproduce:

1. Visit https://dashboard.omise.co/signin and sign in with your credentials and make sure you have not verified your email.
2. Once you log in, you will be on this page --  https://dashboard.omise.co/test/dashboard , send the request to Repeater and add X-Forwarded-Host: bing.com below Host: dashboard.omise.co
3. Open the request in the browser and click on "here" inside --> Please check your mailbox (***********@gmail.com) to confirm your email address.
If you did not get an email from us, please click here to request another email.
4. It will redirect to a malicious page.

POC:
Attached Video.

  2.)  Content Spoofing or Text Injection.
The https://dashboard.omise.co/test/settings website is vulnerable to a Content Spoofing or Text Injection flaw if the server receives a crafted X-Forwarded-Host header.
Description:
Content spoofing, also referred to as content injection, "arbitrary text injection" or virtual defacement, is an attack targeting a user made possible by an injection vulnerability in a web application. When an application does not properly handle user-supplied data, an attacker can supply content to a web application, typically via a parameter value, that is reflected back to the user. This presents the user with a modified page under the context of the trusted domain.

Steps To Reproduce:

1. Visit https://dashboard.omise.co/signin and sign in with your credentials and make sure you have not verified your email.
2. Once you log in, go to Settings  https://dashboard.omise.co/test/settings , send the request to Repeater and add X-Forwarded-Host: bing.com below Host: dashboard.omise.co
3. Open the request in the browser and in the Settings option under Chains mark Enable account chaining CheckBox.
4. Once you mark the check box it will show the URL, copy that URL and paste it in the browser.
5. It will redirect.

POC:
Attached Video.

## Impact

Open Redirection Impact - 
An attacker can redirect users to malicious websites, which can lead to phishing attacks.

Content Spoofing or Text Injection Impact - 
An attacker can create a valid webpage with malicious recommendations and the user believes the recommendation as it was from the stock website.

</details>

---
*Analysed by Claude on 2026-05-24*
