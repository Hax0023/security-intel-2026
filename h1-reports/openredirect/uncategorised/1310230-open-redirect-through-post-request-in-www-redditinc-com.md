# Open Redirect through POST Request in www.redditinc.com

## Metadata
- **Source:** HackerOne
- **Report:** 1310230 | https://hackerone.com/reports/1310230
- **Submitted:** 2021-08-18
- **Reporter:** kratul
- **Program:** Reddit Inc
- **Bounty:** Not specified in writeup
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirects and Forwards
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the /ama endpoint of www.redditinc.com where user-supplied data in the 'failed' POST parameter is used unsafely to construct HTTP redirect responses. An attacker can craft a malicious URL that redirects authenticated users to arbitrary external domains, enabling phishing attacks and credential theft.

## Attack scenario
1. Attacker identifies the /ama POST endpoint accepts a 'failed' parameter that controls redirect behavior
2. Attacker crafts a POST request with 'failed=http://attacker-phishing-domain.com' parameter
3. Attacker embeds this request in a phishing email or shares the URL to legitimate users
4. When user submits the form, the application responds with HTTP 302 redirect to attacker's domain
5. User's browser follows redirect to phishing site which mimics Reddit login or credential collection
6. Attacker captures user credentials, session tokens, or other sensitive information

## Root cause
The application fails to validate or sanitize the 'failed' POST parameter before using it in the HTTP Location header for redirects. The backend directly reflects user input into the redirect response without checking against a whitelist of allowed domains or ensuring the URL is relative/same-origin.

## Attacker mindset
Attacker recognizes that leveraging legitimate domain credibility (valid SSL certificate, authentic URL structure) significantly increases phishing success rates. By discovering that form submission parameters control redirects, attacker can trick users into visiting malicious domains while believing they're still on Reddit's trusted infrastructure.

## Defensive takeaways
- Implement strict whitelist validation for all redirect destinations - only allow relative URLs or explicitly whitelisted domains
- Use allowlist patterns like /^\/(thank-you|success|error)\/.*$/ rather than blacklisting
- Avoid reflecting user input directly into Location headers; validate against application-controlled redirect mappings
- Implement Content Security Policy (CSP) with appropriate directives to limit redirect capabilities
- Log all redirect requests for security monitoring and anomaly detection
- Use security testing frameworks to identify open redirect patterns across all POST/GET endpoints
- Apply framework-level protections if available (e.g., Craft CMS security modules)

## Variant hunting
Test all form endpoints for redirect parameters: 'redirect', 'return', 'returnUrl', 'next', 'url', 'target', 'goto'
Check both GET and POST methods for redirect vulnerabilities on /ama and similar endpoints
Test parameter encoding variants: base64-encoded URLs, URL-encoded special characters, protocol-relative URLs (//evil.com)
Investigate other Zendesk integration endpoints that may have similar form processing logic
Check for partial URL validation bypasses: 'http://redditinc.com.evil.com', 'http://redditinc.com@evil.com'
Test chained redirects and parameter pollution across different form endpoints

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1598.004

## Notes
The vulnerability is relatively straightforward but effective for phishing campaigns. The 'failed' parameter name suggests it's designed to redirect users after form validation failures, but lacks proper validation. The reference to report 242243 indicates this may be a recurring issue across Reddit's infrastructure. The use of Zendesk form handling suggests the vulnerability may affect other Zendesk-integrated applications. Notably, the 'redirect' parameter contains a hash prefix, suggesting potential protection attempts that may be bypassable via the 'failed' parameter.

## Full report
<details><summary>Expand</summary>

## Summary:
Open redirection vulnerabilities arise when an application incorporates user-controllable data into the target of a redirection in an unsafe way. An attacker can construct a URL within the application that causes a redirection to an arbitrary external domain. This behavior can be leveraged to facilitate phishing attacks against users of the application. The ability to use an authentic application URL, targeting the correct domain and with a valid SSL certificate (if SSL is used), lends credibility to the phishing attack because many users, even if they verify these features, will not notice the subsequent redirection to a different domain.

## Steps To Reproduce:
Requests are sent from Burp Suite Community Edition

  1. Intercept Request of www.redditinc.com
  2. Send it to Repeater.
  3. Paste the HTTP Request given.
  4. Send.
  5. Copy link from the Show Response in Browser option.
  6. Paste it in Burp Browser and Run.

##Reference/Supporting Material:
[https://hackerone.com/reports/242243](https://hackerone.com/reports/242243)

## POC Video is attached



## HTTP Request:
```
POST /ama HTTP/2
Host: www.redditinc.com
Content-Type: multipart/form-data; boundary=----------YWJkMTQzNDcw
Cookie: OptanonAlertBoxClosed=2021-08-18T14:18:57.720Z;OptanonConsent=isIABGlobal=false&datestamp=Wed+Aug+18+2021+19%3A48%3A59+GMT%2B0530+(India+Standard+Time)&version=6.13.0&hosts=&consentId=bca87c2e-056e-4636-b582-be4622de55db&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip,deflate
Content-Length: 1509
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4298.0 Safari/537.36

------------YWJkMTQzNDcw
Content-Disposition: form-data; name="action"

zendesk/default/submit
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="agreement"

yes
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="description"

555
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="email"

sample@email.tst
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="email_confirm"

sample@email.tst
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="failed"

http://google.com
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="name"

ghovjnjv
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="organization"

PENTESTING
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="participants"

ghovjnjv
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="redirect"

74bcbfb4f9c047fb4e467dd203ca3b30f2b31216551ab9db2bf44911c029d506thank-you/ama-form-step-1
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="subject"

AMA Request
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="success"

thank-you/ama-form-step-1
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="ticket_form_id"

360000307211
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="timeframe"

next-week
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="timezone"

(GMT-05:00) Eastern Time (US & Canada)
------------YWJkMTQzNDcw--

```



## HTTP Response:
```
HTTP/2 302 Found
Server: nginx
Content-Type: text/html; charset=UTF-8
Permissions-Policy: interest-cohort=()
X-Robots-Tag: none
X-Powered-By: Craft CMS
Location: http://google.com
Cache-Control: private
Accept-Ranges: bytes
Date: Wed, 18 Aug 2021 15:30:48 GMT
Via: 1.1 varnish
Strict-Transport-Security: max-age=31536000; includeSubdomains
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-Xss-Protection: 1; mode=block
Content-Length: 0
```

## Impact

A remote attacker can redirect users from your website to a specified URL. This problem may assist an attacker to conduct phishing attacks, trojan distribution, spammers.

</details>

---
*Analysed by Claude on 2026-05-24*
