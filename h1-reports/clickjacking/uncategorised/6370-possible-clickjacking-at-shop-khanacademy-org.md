# Missing X-Frame-Options Header - Clickjacking Vulnerability at shop.khanacademy.org

## Metadata
- **Source:** HackerOne
- **Report:** 6370 | https://hackerone.com/reports/6370
- **Submitted:** 2014-04-08
- **Reporter:** internetwache
- **Program:** Khan Academy
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, Missing Security Header, UI Redressing
- **CVEs:** None
- **Category:** uncategorised

## Summary
The shop.khanacademy.org domain fails to implement the X-Frame-Options security header, leaving it vulnerable to clickjacking attacks. An attacker can frame the website within a malicious page and trick users into performing unintended actions such as making purchases or account modifications through UI redressing techniques.

## Attack scenario
1. Attacker creates a malicious webpage that embeds shop.khanacademy.org in an invisible iframe
2. Attacker overlays transparent or disguised clickable elements on top of the framed Khan Academy shop interface
3. Victim visits the attacker's webpage, believing they are interacting with benign content
4. When victim clicks on what they think is a harmless button, their click is actually directed to the hidden iframe
5. Victim unknowingly completes an action on the Khan Academy shop (e.g., purchases merchandise, changes account settings)
6. Attacker harvests any sensitive information or benefits from the unintended user action

## Root cause
The server fails to implement the X-Frame-Options HTTP response header. Without this header, browsers allow the page to be framed by any domain, enabling clickjacking attacks. The response headers show various security measures (X-XSS-Protection, X-Content-Type-Options) but lack frame-origin protection.

## Attacker mindset
An attacker recognizes that many users trust the Khan Academy brand and would be willing to make purchases or donate through their shop. By framing the legitimate site within a malicious context, the attacker exploits this trust to trick users into performing financial transactions or revealing information without their knowledge or consent.

## Defensive takeaways
- Implement X-Frame-Options header with 'SAMEORIGIN' or 'DENY' value to restrict framing to same-origin requests or disallow framing entirely
- Use Content-Security-Policy header with 'frame-ancestors' directive as a modern alternative to X-Frame-Options
- Implement frame-busting JavaScript code as an additional layer of defense against clickjacking
- Conduct regular security header audits across all subdomains and applications
- Test all user-facing applications with automated security scanning tools to detect missing security headers
- Apply consistent security header policies across all Khan Academy domains, not just primary domains

## Variant hunting
Look for similar missing security headers on other Khan Academy subdomains (*.khanacademy.org). Check for incomplete CSP implementations that don't restrict frame-ancestors. Test other e-commerce or transaction-related pages that may be vulnerable to clickjacking. Examine sister organizations or related properties for the same vulnerability pattern.

## MITRE ATT&CK
- T1566.002
- T1189
- T1204.1

## Notes
The reporter correctly identified the vulnerability but suggested 'X-Frame-Origin: sameorigin' when the correct header name is 'X-Frame-Options: SAMEORIGIN'. The proof of concept clearly demonstrates the absence of frame-origin protection headers. This is a straightforward configuration issue with a simple remediation path. The vulnerability is particularly concerning for financial transactions on the shop subdomain.

## Full report
<details><summary>Expand</summary>

Hello there,

the website at shop.khanacademy.org isn't protected against clickjacking properly.

###PoC

```
curl -L -I http://shop.khanacademy.org/ 
HTTP/1.1 200 OK
Server: nginx
Date: Tue, 08 Apr 2014 00:33:39 GMT
Content-Type: text/html; charset=utf-8
Vary: Accept-Encoding
Status: 200 OK
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-UA-Compatible: chrome=1
X-ShopId: 1494466
X-ShardId: 0
X-Stats-Unique-Token: 2dd016682529fa6dc0ac02f03b41cb145bdeb1906793867d2f763e05dad4a464
X-Stats-Visit-Token: d52a2198c1a197fb3535f0ea5db92ee9381f41ad8a910d9997859a4a7d21a6bb
ETag: cacheable:8709c7da7c24e09f7f45bab2c9d17d6a
X-Alternate-Cache-Key: cacheable:214f21e7ce7fcc794113ab6ec2eac291
X-Cache: miss
Set-Cookie: _shopify_y=2dd016682529fa6dc0ac02f03b41cb145bdeb1906793867d2f763e05dad4a464; path=/; expires=Sat, 08 Apr 2034 00:33:39 -0000
Set-Cookie: _shopify_s=d52a2198c1a197fb3535f0ea5db92ee9381f41ad8a910d9997859a4a7d21a6bb; path=/; expires=Tue, 08 Apr 2014 01:03:39 -0000
Set-Cookie: request_method=HEAD; path=/
Set-Cookie: _session_id=289a218d076bea034b85e5e807e00aa9; path=/; HttpOnly
X-Request-Id: 6a3f8d62-4d9d-4303-af04-12e201856770
P3P: CP="NOI DSP COR NID ADMa OPTa OUR NOR"

```


You should add the ```X-Frame-Origin: sameorigin``` header to the server http responses. Otherwise you're vulnerable to clickjacking attacks.


Best regards,
Sebastian

</details>

---
*Analysed by Claude on 2026-05-24*
