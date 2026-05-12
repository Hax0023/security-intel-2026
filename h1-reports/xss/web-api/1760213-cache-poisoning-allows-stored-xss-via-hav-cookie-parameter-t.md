# Cache Poisoning Enables Stored XSS via WAF Bypass in hav Cookie Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1760213 | https://hackerone.com/reports/1760213
- **Submitted:** 2022-11-02
- **Reporter:** bombon
- **Program:** Abritel (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cache Poisoning, Stored Cross-Site Scripting (XSS), WAF Bypass, Authentication Token Theft
- **CVEs:** None
- **Category:** web-api

## Summary
A cache poisoning vulnerability combined with a WAF bypass allows attackers to inject stored XSS payloads via the 'hav' cookie parameter. By embedding double quotes in XSS payloads, the WAF filtering is bypassed, and the malicious script is cached and executed for all subsequent users visiting the poisoned URL, enabling session token theft and account takeover.

## Attack scenario
1. Attacker crafts a malicious request with XSS payload embedded in the 'hav' cookie parameter, using strategic double quote placement to evade WAF detection (e.g., '</sc"ript>' bypasses '</script>' filter)
2. Attacker requests a cacheable resource (PHP.js or PHP.jpeg file) with the poisoned cookie, causing the server to reflect the XSS payload into the response
3. The response containing the XSS payload is cached by CDN/proxy servers using the URL as the cache key, without properly isolating cookie-based variations
4. Subsequent users request the same URL without the malicious cookie, but receive the cached response containing the stored XSS payload
5. The XSS payload executes in victims' browsers, typically extracting the HASESSIONV3 authentication token from window.INITIAL_STATE.system.cookie
6. Attacker uses stolen session tokens to hijack victim accounts and gain unauthorized access

## Root cause
Multiple layered failures: (1) WAF uses insufficient pattern matching (blocks '</script>' but not '</sc"ript>'), (2) Server reflects unsanitized cookie values into responses, (3) Cache key does not properly account for cookie variations, treating different cookie values as the same cached resource

## Attacker mindset
Methodical WAF evasion researcher who discovered quote-based obfuscation technique. Recognized cache poisoning potential to amplify impact from single injection to mass compromise. Targeted high-value cookie containing session credentials for account takeover exploitation.

## Defensive takeaways
- Implement context-aware output encoding rather than blocklist-based WAF rules; encode all cookie values before rendering in HTML/JavaScript contexts
- Use cache keys that include cookie values or implement Set-Cookie/Vary headers to prevent cookie-based cache poisoning
- Apply HTML entity encoding and JavaScript string escaping to all reflected/stored user input regardless of perceived safety
- Implement Content Security Policy (CSP) with script-src restrictions to mitigate XSS execution impact
- Use HTTPOnly and Secure flags on session cookies to prevent JavaScript access and transmission over non-HTTPS
- Validate and sanitize input at the point of storage, not just at output
- Conduct security testing specifically targeting WAF bypass techniques (quote insertion, encoding variations, case manipulation)
- Implement proper cache invalidation and segmentation based on security context

## Variant hunting
Test other quote-based WAF bypasses in different parameters: referer, user-agent, accept-language headers
Look for similar cache poisoning via other HTTP headers (X-Forwarded-For, Origin, custom headers)
Test single-quote, backtick, and HTML entity-encoded variations of filtered patterns
Check if other cookie parameters exhibit similar reflection/caching behavior
Investigate whether the PHP.js and PHP.jpeg endpoints have different caching policies or cache key logic
Test polyglot payloads that work across multiple content types (JS, JPEG, HTML) to poison multiple endpoints
Search for other file extensions with similar reflection patterns (.json, .xml, .svg)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1005 - Data from Local System
- T1040 - Network Sniffing
- T1539 - Steal Web Session Cookie
- T1056 - Input Capture

## Notes
Report references a previous duplicate (Report #1698316) that was supposedly closed as resolved, suggesting this is a variant or incomplete remediation of a known issue. The use of file extensions (.php.js, .php.jpeg) indicates unconventional routing that may bypass standard security assumptions. The attack requires victim interaction only after initial poisoning, making it particularly dangerous for high-traffic pages. Session token extraction via window.INITIAL_STATE suggests client-side JavaScript initialization of sensitive data, creating the condition for credential theft.

## Full report
<details><summary>Expand</summary>

## Summary:

Report #1698316 was closed as resolved 

You told me that the stored XSS was going to be resolved since "As this relies on the same root cause, we will be closing it as duplicate", but no 


abritel.fr has a strong WAF, however the server hides double quotes, allowing to bypass the WAF

e.g

The server blocks `</script`but if I send `</sc"ript>`

WAF is bypassed and the output is </script>


## Steps To Reproduce:


1-> Send this request 

```http
GET /annonces/location-vacances/france_midi-pyrenees_46_stcere_dt0.php.js?xxxd HTTP/2
Host: www.abritel.fr
Cookie: hav=xss"</sc"ript><sv"g/onloa"d=aler"t"(document.doma"in)>
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.abritel.fr/signup?enable_registration=true&redirectTo=%2Fsearch%2Fkeywords%3Asoissons-france-%28xss%29%2FminNightlyPrice%2F0%3FpetIncluded%3Dfalse%26filterByTotalPrice%3Dtrue%26ssr%3Dtrue&referrer_page_location=serp
Upgrade-Insecure-Requests: 1
Te: trailers
```

2-> Using another browser visit: 

https://www.abritel.fr/annonces/location-vacances/france_midi-pyrenees_46_stcere_dt0.php.jpeg?xxxd

Exploit:

This is the payload to extract the HASESSIONV3 
xss"</sc"ript><sv"g/onloa"d=aler"t"(window.INITIAL_STATE.system.cookie)>


## Supporting Material/References:

{F2016192}

## Impact

Stored XSS to Account Takeover

</details>

---
*Analysed by Claude on 2026-05-12*
