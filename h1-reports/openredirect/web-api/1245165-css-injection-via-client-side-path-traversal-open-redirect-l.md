# CSS Injection via Client Side Path Traversal + Open Redirect leads to personal data exfiltration on Acronis Cloud

## Metadata
- **Source:** HackerOne
- **Report:** 1245165 | https://hackerone.com/reports/1245165
- **Submitted:** 2021-06-26
- **Reporter:** mr-medi
- **Program:** Acronis
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** CSS Injection, Path Traversal, Open Redirect, Client-Side Request Forgery, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A chained vulnerability combining CSS injection via unsanitized color_scheme parameter, relative path traversal, and an open redirect in the OAuth authorize endpoint allows attackers to load malicious CSS from external domains and exfiltrate sensitive user data (customer and partner identifiers). The attack leverages the browser's automatic redirect following for CSS resource loading to bypass same-origin protections.

## Attack scenario
1. Attacker identifies that the color_scheme GET parameter is unsanitized and concatenated into a CSS file path without filtering '.' and '/' characters
2. Attacker discovers the /api/2/idp/authorize/ endpoint accepts a controllable 'state' parameter that enables open redirect functionality
3. Attacker crafts a color_scheme payload using path traversal (%2F..%2F..%2F..%2F) to reach the vulnerable OAuth endpoint instead of the CSS file
4. Attacker includes the open redirect parameters in the traversal payload, redirecting to their attacker-controlled domain hosting malicious CSS
5. Victim clicks malicious link or visits attacker's page with crafted color_scheme parameter; browser loads the traversed path which redirects to attacker's CSS
6. Malicious CSS uses attribute selectors and pseudo-elements (e.g., content: attr()) to exfiltrate sensitive data like customer/partner hashes via background-image URLs to attacker's server

## Root cause
Multiple security deficiencies: (1) Frontend fails to validate/sanitize path traversal characters in color_scheme parameter before concatenating into CSS file path, (2) OAuth authorize endpoint does not validate redirect_uri/state parameters for same-origin enforcement, (3) No Content Security Policy (CSP) preventing external CSS loading, (4) CSS parser allows attribute extraction and exfiltration via background-image/content properties

## Attacker mindset
Chain multiple lower-severity vulnerabilities (path traversal + open redirect) to bypass same-origin restrictions and load untrusted CSS, then abuse CSS attribute selectors to extract DOM data invisible to traditional XSS filters. Target high-value data like customer/partner identifiers stored in page context.

## Defensive takeaways
- Implement strict whitelist validation for color_scheme parameter—only allow expected values (e.g., 'light', 'dark'), reject special characters
- Sanitize all user inputs before path concatenation; use path joining libraries that prevent traversal sequences
- Enforce redirect_uri whitelist validation in OAuth endpoints; validate against hardcoded allowed redirect domains
- Implement Content Security Policy (CSP) with style-src directive to restrict CSS sources to same-origin or specific trusted CDNs
- Never allow open redirects in sensitive endpoints; validate state/redirect parameters against a whitelist
- Apply defense-in-depth: avoid storing sensitive identifiers in easily-accessible DOM or page context; use data attributes sparingly
- Implement Subresource Integrity (SRI) for any external resource loading
- Regular security code review for parameter concatenation patterns in URL construction

## Variant hunting
Test all GET parameters used in resource path concatenation (JavaScript, CSS, image loading) for path traversal patterns
Audit all redirect-enabled endpoints (OAuth, password reset flows, social login) for open redirect via state, return_url, redirect_uri parameters
Search for CSS file loading patterns that don't validate file extensions or paths
Look for other endpoints that concatenate user input into HTTP Location header redirects
Test for similar path traversal in other cloud console features (branding, theming, localization)
Check if other sensitive data fields are accessible via CSS attribute selectors (account IDs, tokens, API keys)

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1601 Modify System Image
- T1187 Forced Authentication
- T1566 Phishing
- T1592 Gather Victim Identity Information
- T1040 Traffic Sniffing
- T1557 Man-in-the-Middle

## Notes
This is a sophisticated multi-stage attack requiring victim interaction (clicking malicious link). The writeup was truncated mid-sentence but clearly demonstrates impact on customer/partner data. The vulnerability chain is elegant but each component (path traversal, open redirect, CSS injection) would individually be lower severity—the chaining elevates to High/Critical due to authentication bypass potential and PII exfiltration. The OAuth endpoint accepting arbitrary state values without validation is a critical flaw in redirect handling.

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
*Analysed by Claude on 2026-05-24*
