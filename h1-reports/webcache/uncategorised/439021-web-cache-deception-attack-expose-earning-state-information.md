# Web Cache Deception Attack - Exposure of Earning State and Authentication Information

## Metadata
- **Source:** HackerOne
- **Report:** 439021 | https://hackerone.com/reports/439021
- **Submitted:** 2018-11-11
- **Reporter:** memon
- **Program:** Berush
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Web Cache Deception, Information Disclosure, Improper Cache Control, Path Traversal/Normalization
- **CVEs:** None
- **Category:** uncategorised

## Summary
A web cache deception vulnerability allows unauthenticated attackers to access sensitive user information including earning state, tokens, and personal account data by appending static file extensions to authenticated dynamic pages. The application fails to properly distinguish between dynamic content and static assets, causing cached responses of personalized pages to be served publicly.

## Attack scenario
1. Attacker identifies authenticated endpoint (e.g., /en/register/confirmation/success) that returns personalized user data
2. Attacker appends static file extension (.css, .js, .jpg) to bypass cache controls (e.g., /en/register/confirmation/success/none.css)
3. Server processes request incorrectly, returning personalized content for the dynamic page while cache treats it as static asset
4. Response gets cached by reverse proxy/CDN with public accessibility due to static file extension
5. Attacker accesses same URL without authentication and receives cached personalized content
6. Sensitive data (earnings, tokens, session info) is exposed to unauthorized parties

## Root cause
The application fails to properly implement cache control headers for dynamic endpoints and does not validate that appended path segments are legitimate. The reverse proxy/cache layer trusts the file extension in the URL to determine cacheability rather than inspecting HTTP caching headers or validating request authenticity. Server URL parsing treats /page.php/fake.css as a request for /page.php, returning authenticated content with caching directives that allow public caching.

## Attacker mindset
An attacker would recognize that web caches often prioritize speed over security, automatically caching content with static file extensions. By exploiting the mismatch between URL structure and server processing, they can obtain valuable information like user earnings, authentication tokens, and CSRF tokens that would normally be protected. This is a low-effort, high-impact attack requiring only URL manipulation and basic understanding of web caching behavior.

## Defensive takeaways
- Implement strict cache control headers (Cache-Control: no-store, no-cache, must-revalidate) on all dynamic, authenticated endpoints
- Configure cache layers to respect HTTP caching directives rather than blindly caching based on file extensions
- Normalize and validate URL paths before serving content; reject requests with suspicious path patterns (file extension appended to dynamic pages)
- Implement authentication checks at the cache layer or use cache keys that include user identity/authentication status
- Never include sensitive tokens, CSRF tokens, or session identifiers in response bodies for HTML pages; use secure cookies with HttpOnly and SameSite flags
- Use Vary headers (e.g., Vary: Authorization, Cookie) to ensure authenticated and unauthenticated responses are cached separately
- Regularly audit cache configuration and test for cache deception vulnerabilities

## Variant hunting
Test other authenticated endpoints with static file extensions (.js, .png, .gif, .svg, .woff)
Try double extensions (.php.css, .aspx.js) on different technology stacks
Append null bytes or special characters (;.css, ?.css) to bypass cache rules
Test subdirectory traversal patterns (/page.php/../something.css)
Check if sensitive API endpoints are vulnerable (/api/user/profile.json.css)
Verify if cached responses include sensitive headers (Authorization, Set-Cookie) that leak authentication
Test different cache layers (CDN, reverse proxy, browser cache) for varying behaviors

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1200
- T1020

## Notes
This is a real-world vulnerability class first documented in the context of PayPal. The attack exploits a fundamental disconnect between how web servers parse URLs and how caching infrastructure categorizes requests. The vulnerability is particularly dangerous because it affects cached content that remains publicly accessible indefinitely. Organizations using reverse proxies or CDNs must ensure cache control policies are authentication-aware and that dynamic endpoints cannot be inadvertently cached through URL manipulation techniques.

## Full report
<details><summary>Expand</summary>

Hello,

I have found new Vulnerability in your website which called Web cache deception attack.
It's found first time in Paypal.

###Web Cache Deception Attack

Websites often tend to use web cache functionality to store files that are often retrieved, to reduce latency from the web server.

#### Let's see an example of web cache.

Website http://www.example.com is configured to go through a reverse proxy. A dynamic page that is stored on the server and returns personal content of users, such as http://www.example.com/home.php, will have to create it dynamically per user, since the data is different for each user. This kind of data, or at least its personalized parts, isn't cached. What's more reasonable and common to cache are static, public files: style sheets (css), scripts (js), text files (txt), images (png, bmp, gif), etc. This makes sense because these files usually don't contain any sensitive information. In addition, as can be found in various best practices articles about web cache configuration, it's recommended to cache all static files that are meant to be public, and disregard their HTTP caching headers.
What happens when accessing a URL like http://www.example.com/home.php/non-existent.css
A GET request to that URL will be produced by the browser. The interesting thing is the server's reaction – how does it interpret the request URL? Depending on its technology and configuration (the URL structure might need to be built slightly different for different servers), the server returns the content of http://www.example.com/home.php. And yes, the URL remains http://www.example.com/home.php/non-existent.css. The HTTP headers will be the same as for accessing http://www.example.com/home.php directly: same caching headers and same content type (text/html, in this case).

### Steps To Reproduce:

1. Login to your account.
2. Go to `https://www.berush.com/en/register/confirmation/success`.
3. Then after go to `https://www.berush.com/en/register/confirmation/success/none.css`.
4. Open private mode (Incognito window) or Any other browser and paste `https://www.berush.com/en/register/confirmation/success/none.css` url in address bar. Now you can see then without authanticated i can all earning state of authanticated user account.

#### Attached video PoC for more information.

###Reference:
[397508](https://hackerone.com/reports/397508)

I hope you understand.

Regards,
Memon

## Impact

An attacker who lures a logged-on user to access `https://www.berush.com/en/register/confirmation/success/none.css` will caue this page – containing the user's personal content and Token information – to be cached and thus publicly-accessible. It could get even worse, if the body of the response contains (for some reason) the session identifier, security answers or CSRF tokens. All the attacker has to do now is to access this page on his own and expose this data.

</details>

---
*Analysed by Claude on 2026-05-24*
