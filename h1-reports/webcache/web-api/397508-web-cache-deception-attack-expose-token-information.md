# Web Cache Deception Attack - Token Information Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 397508 | https://hackerone.com/reports/397508
- **Submitted:** 2018-08-21
- **Reporter:** memon
- **Program:** Chaturbate
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Web Cache Deception, Information Disclosure, Authentication Bypass, Cache Poisoning
- **CVEs:** None
- **Category:** web-api

## Summary
A web cache deception vulnerability allows unauthenticated attackers to access authenticated user content by appending static file extensions (e.g., .js, .css) to dynamic URLs. When a logged-in user visits a malicious link like /my_collection/min.js, the server returns personalized content with caching headers, causing the cached response containing tokens and sensitive data to be publicly accessible.

## Attack scenario
1. Attacker crafts a URL by appending a static file extension (.js, .css, etc.) to an authenticated endpoint: https://chaturbate.com/my_collection/min.js
2. Attacker tricks or socially engineers a logged-in user to visit this crafted URL
3. Server processes the request, ignores the .js extension, and returns the dynamic content of /my_collection/ with the user's personal data and authentication tokens
4. Reverse proxy/CDN caches the response because it appears to be a static file (.js) based on URL
5. Attacker accesses the same URL in an unauthenticated session and receives the cached response containing victim's sensitive data
6. Attacker extracts tokens, session identifiers, or other sensitive information from the cached response

## Root cause
Misconfiguration of caching rules in the reverse proxy/CDN that caches URLs based on file extension while the backend server ignores file extensions in the URL path. The server returns dynamic, personalized content with public caching headers for requests to /my_collection/min.js, treating it identically to /my_collection/. Additionally, there is a mismatch between cache key interpretation (URL-based) and server-side routing logic.

## Attacker mindset
An attacker recognizes that web cache systems prioritize static file extensions and exploits the disconnect between what the cache considers cacheable (static extensions) and what the server actually returns (dynamic personalized content). They understand that users trust links from legitimate sources and will click them, unaware they're poisoning the cache with authenticated content.

## Defensive takeaways
- Implement strict cache rules that differentiate between actual static files and dynamic endpoints, not relying solely on URL extensions
- Configure cache key normalization to treat /path/endpoint and /path/endpoint/fake.js identically, or exclude such patterns entirely
- Apply authentication-aware caching: never cache authenticated responses with public cache headers (use Cache-Control: private, no-cache)
- Normalize URLs server-side and reject or redirect requests with invalid path traversal patterns (e.g., /endpoint/file.ext where .ext is fake)
- Use security headers like Vary: Authorization to include authentication status in cache keys
- Implement Content Security Policy and X-Frame-Options to prevent clickjacking attacks that trick users into poisoning caches
- Monitor cache hit rates for authenticated endpoints and alert on anomalies
- Regular security audits of reverse proxy/CDN configurations

## Variant hunting
Look for similar patterns across the platform: any dynamic endpoint + static extension (other extensions like .png, .gif, .txt, .json). Test endpoints handling user data, account settings, API responses, and dashboard pages. Check if other static extensions bypass authentication on sensitive paths. Examine URL rewriting rules and path normalization logic. Test path traversal with double extensions (.php.js, .php.css) and special characters.

## MITRE ATT&CK
- T1190
- T1110
- T1040
- T1020
- T1530

## Notes
This vulnerability was famously discovered in PayPal in 2017. The bug bounty report lacks specific bounty amount but represents a critical issue combining caching misconfiguration with information disclosure. Video PoC was attached but not included in text. The vulnerability requires coordination between reverse proxy behavior and server-side routing logic. Severity is high because it exposes authentication tokens and personal information with no user interaction required after the initial cache poisoning.

## Full report
<details><summary>Expand</summary>

Hello,

I have found new Vulnerability in your website which called Web cache deception attack.
It's found first time in Paypal.

###Web Cache Deception Attack
Websites often tend to use web cache functionality to store files that are often retrieved, to reduce latency from the web server.

####Let's see an example of web cache.
Website http://www.example.com is configured to go through a reverse proxy. A dynamic page that is stored on the server and returns personal content of users, such as http://www.example.com/home.php, will have to create it dynamically per user, since the data is different for each user. This kind of data, or at least its personalized parts, isn't cached. What's more reasonable and common to cache are static, public files: style sheets (css), scripts (js), text files (txt), images (png, bmp, gif), etc. This makes sense because these files usually don't contain any sensitive information. In addition, as can be found in various best practices articles about web cache configuration, it's recommended to cache all static files that are meant to be public, and disregard their HTTP caching headers.
What happens when accessing a URL like http://www.example.com/home.php/non-existent.css
A GET request to that URL will be produced by the browser. The interesting thing is the server's reaction – how does it interpret the request URL? Depending on its technology and configuration (the URL structure might need to be built slightly different for different servers), the server returns the content of http://www.example.com/home.php. And yes, the URL remains http://www.example.com/home.php/non-existent.css. The HTTP headers will be the same as for accessing http://www.example.com/home.php directly: same caching headers and same content type (text/html, in this case).

### Steps To Reproduce:
1. Login to your account.
2. Go to `https://chaturbate.com/my_collection/`.
3. Then after go to `https://chaturbate.com/my_collection/min.js`.
4. Open private mode (Incognito window) or Any other browser  and paste `https://chaturbate.com/my_collection/min.js` url in address bar. Now you can see then without authanticated i can all the detaills of user account.

#####Attached video PoC for more information.

I hope you understand.

Regards,
Memon

## Impact

An attacker who lures a logged-on user to access `https://chaturbate.com/my_collection/min.js` will caue this page – containing the user's personal content and Token information – to be cached and thus publicly-accessible. It could get even worse, if the body of the response contains (for some reason) the session identifier, security answers or CSRF tokens. All the attacker has to do now is to access this page on his own and expose this data.

</details>

---
*Analysed by Claude on 2026-05-24*
