# Web Cache Poisoning Attack Leads to User Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 631589 | https://hackerone.com/reports/631589
- **Submitted:** 2019-06-28
- **Reporter:** deksterh11
- **Program:** Lyst
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Web Cache Poisoning, Information Disclosure, Authentication Bypass, Sensitive Data Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
The web server is vulnerable to cache poisoning attacks where authenticated user data becomes cached and served to unauthenticated users. An attacker can craft URLs that cause the server to cache personalized content (containing email, member ID, etc.) and serve it to other users regardless of authentication status.

## Attack scenario
1. Attacker identifies a URL pattern that serves static-like content but contains user-specific data (e.g., /shop/trends/mens-dress-shoes/blahblah.css)
2. Attacker logs in with their account and visits the crafted URL to populate cache with authenticated content
3. The web server caches the response with user information (email, member ID) embedded in the cached content
4. An unauthenticated user (or attacker in private browsing mode) requests the same URL
5. The server serves the cached content to the unauthenticated user, revealing authentication-specific information
6. Attacker extracts sensitive data (email, member ID) from the source code of the cached response

## Root cause
The web server fails to properly differentiate cached responses based on authentication state. The cache key does not include user authentication context, causing authenticated user data to be cached and indiscriminately served to all subsequent requesters regardless of their authentication status.

## Attacker mindset
The attacker exploits the assumption that static resources (CSS files) don't contain sensitive data. By deliberately poisoning the cache with authenticated requests, they demonstrate how dynamic content can be weaponized when cache mechanisms ignore authentication context. This is a reconnaissance and information gathering attack targeting user account identifiers.

## Defensive takeaways
- Implement cache keys that include authentication state/user context to prevent serving authenticated content to unauthenticated users
- Use Cache-Control headers (private, no-cache, no-store) for any response containing user-specific data
- Validate that static resource endpoints do not expose dynamic or user-specific information
- Implement proper cache isolation between authenticated and unauthenticated sessions
- Monitor cache behavior and test cache poisoning scenarios as part of security testing
- Consider using Set-Vary headers to include authentication status in cache differentiation
- Implement content security policies to prevent sensitive information leakage in static resources

## Variant hunting
Look for other URL patterns that mix static file extensions with dynamic content, particularly in: product pages with user-specific pricing/recommendations, personalized list endpoints served as static files, user-generated content cached without authentication context, API endpoints using static file extensions, and any resource served with user data but generic cache headers.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1592

## Notes
This is a classic Web Cache Deception attack variant leveraging cache poisoning. The reporter references the BlackHat 2017 presentation by Gil which formalized this attack vector. The vulnerability is particularly serious because it enables account enumeration and credential theft preparation. The report demonstrates exploitation through direct technical reproduction with screenshots. The simplicity of the attack (just visiting a URL with proper authentication) makes it highly practical and reproducible at scale.

## Full report
<details><summary>Expand</summary>

Hello

Your Web-Server is vulnerable to web cache poisoning attacks.
This means, that the attacker are able to get another user Information.

If you are logged in and visit this website (For example):
https://www.lyst.com/shop/trends/mens-dress-shoes/blahblah.css

Then the server will store the information in the cache, BUT with the logged in user information.
A non-logged-in user can then visit this website and see the information contained therein.

In that case, this url: https://www.lyst.com/shop/trends/mens-dress-shoes/blahblah.css can be visited in Private Mode and still you will be shown as "LOGGED IN" and then check the Source code you will get your email, member id ,etc..


Some informations about the attack:
https://www.blackhat.com/docs/us-17/wednesday/us-17-Gil-Web-Cache-Deception-Attack.pdf

The screenshots with the steps are in the attachments.

## Impact

Web cache poisoning attack can be used to steal user informations like email, name and member id which is important for the login security feature.

</details>

---
*Analysed by Claude on 2026-05-24*
