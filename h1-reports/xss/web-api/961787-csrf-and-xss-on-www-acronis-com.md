# CSRF and Reflected XSS on Acronis Forgot Registration Email Form

## Metadata
- **Source:** HackerOne
- **Report:** 961787 | https://hackerone.com/reports/961787
- **Submitted:** 2020-08-18
- **Reporter:** cabelo
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Request Forgery (CSRF), Reflected Cross-Site Scripting (XSS)
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on the Acronis password reminder form at /en-us/my/remind/index.html where user input is not properly sanitized before being reflected in the response. The vulnerability can be exploited via CSRF to execute arbitrary JavaScript in the victim's browser context, potentially stealing session cookies and sensitive data.

## Attack scenario
1. Attacker crafts a malicious HTML page containing a hidden form that targets the vulnerable Acronis remind endpoint
2. Attacker sends the link to a target user (social engineering or phishing)
3. When the victim visits the attacker's page, the hidden form auto-submits a POST request to Acronis with XSS payload in the parameter
4. The Acronis application reflects the unescaped payload back in the HTML response without sanitization
5. The victim's browser executes the injected SVG/JavaScript code (e.g., confirm(document.cookie))
6. Attacker gains access to victim's session cookies, session tokens, or can perform actions on behalf of the victim

## Root cause
Insufficient input validation and output encoding on the POST parameter. The application fails to properly sanitize or HTML-encode user-supplied input before reflecting it in the HTTP response. Additionally, CSRF protection tokens appear to be either missing or not properly validated.

## Attacker mindset
An opportunistic attacker exploiting a common web vulnerability to target Acronis users. The combination of CSRF + XSS suggests reconnaissance of the application's form structure and testing for both defense mechanisms. The attacker likely seeks to harvest session credentials, perform unauthorized actions, or redirect users to phishing pages.

## Defensive takeaways
- Implement strict input validation on all POST parameters; whitelist acceptable characters and reject suspicious input early
- Apply context-aware output encoding (HTML entity encoding) to all user-controlled data before rendering in HTML context
- Implement robust CSRF protection with SameSite cookie flags (SameSite=Strict/Lax) and unpredictable, user-specific tokens validated on each request
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Implement automated security testing (SAST/DAST) in the CI/CD pipeline to catch XSS vulnerabilities early
- Apply a Web Application Firewall (WAF) with rules to detect and block common XSS attack patterns
- Conduct security code review focusing on all input/output handling in form processing logic

## Variant hunting
Test other form endpoints on Acronis for similar XSS vulnerabilities (registration, login, password reset)
Attempt polyglot payloads and encoding bypasses (hex, unicode, double encoding) on the same parameter
Check if CSRF tokens are session-bound and properly validated; test token reuse across sessions
Test for DOM-based XSS in client-side JavaScript processing of form data
Probe for Stored XSS if user input is cached or persisted in backend systems
Verify if other parameters (token, SN, OrderId) are also vulnerable to XSS
Test for bypassing via alternative HTTP methods (GET, PUT, PATCH) on the same endpoint

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1528
- T1563

## Notes
The POC demonstrates a chained attack using CSRF to bypass same-origin restrictions and XSS to execute arbitrary code. The payload encoding (HTML entity escaping: &quot;, &lt;, &gt;) and SVG OnLoad handler bypass suggests the application may have basic but insufficient XSS protections. The use of comment syntax (<!--) indicates an attempt to break out of HTML context. Acronis should prioritize patching this as it directly impacts user account security on a platform dealing with backup and system recovery services.

## Full report
<details><summary>Expand</summary>

Hi team,

I've discovered a XSS Reflected vulnerability on Forgot Registration E-mail form. I performed a POC using CSRF  to inject and execute a javascript code in the POST request.

Target Page: https://www.acronis.com/en-us/my/remind/index.html

POST Data: token=a016902ceaeb6ae91c21302631fbbcfc&SN=818198181891891981981981516518198198&OrderId=&Submit=Send+E-mail%0D%0A

Payload: 1&quot;&lt;!--&gt;&lt;Svg OnLoad=(confirm)(document.cookie)&lt;!--

Steps to reproduce/POC:

CSRF html page:
{F954073}

CORS html  code:
{F954074}

code:
```
<form action=https://www.acronis.com/en-us/my/remind/index.html method=POST><input type=hidden name="token" value="a016902ceaeb6ae91c21302631fbbcfc"><input type=hidden name="SN" value="818198181891891981981981516518198198"><input type=hidden name="OrderId" value=""><input type=hidden name="Submit" value="Send+E-mail%0D%0A"><input type=hidden name="c" value="1&quot;&lt;!--&gt;&lt;Svg OnLoad=(confirm)(document.cookie)&lt;!--"><input type=submit value=XSS-Acronis></form>
```

XSS:
{F954075}

Best Regards.

## Impact

An attacker execute arbitrary JavaScript code in the context of the users website.

</details>

---
*Analysed by Claude on 2026-05-12*
