# Cloudflare /cdn-cgi/ Image Resizing Allows Unrestricted External Resource Rendering on enjinusercontent.com

## Metadata
- **Source:** HackerOne
- **Report:** 2545994 | https://hackerone.com/reports/2545994
- **Submitted:** 2024-06-11
- **Reporter:** 19whoami19
- **Program:** Enjin (via HackerOne)
- **Bounty:** Unknown (report number 2545994)
- **Severity:** High
- **Vuln:** Improper Access Control, Server-Side Request Forgery (SSRF), HTML Injection, Content Injection, Path Traversal/Open Redirect, Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Cloudflare /cdn-cgi/image endpoint on nft.production.enjinusercontent.com lacks proper origin validation, allowing attackers to render arbitrary external resources (images, HTML, SVGs) through the image resizing service. This enables HTML injection, SSRF exploitation, and potential malware/phishing delivery without access control checks.

## Attack scenario
1. Attacker identifies that /cdn-cgi/image endpoint accepts arbitrary external URLs as parameters
2. Attacker crafts malicious URL containing external SVG/HTML resource: /cdn-cgi/image/width=1000,format=auto/https://attacker.com/malicious.svg
3. When victim visits the crafted enjinusercontent.com URL, the CDN service fetches and renders the external resource
4. Attacker's HTML/SVG executes in the context of enjinusercontent.com domain, enabling phishing, credential theft, or XSS
5. Attacker can probe internal network resources via SSRF by pointing to internal IPs/services through the CDN endpoint
6. Attacker hosts misinformation content and shares link appearing to come from legitimate Enjin domain

## Root cause
Cloudflare's /cdn-cgi/image endpoint was configured without whitelist validation of allowed source domains. The service accepts any URL parameter without verifying that the source is authorized, treating all external URLs as equally valid for fetching and rendering.

## Attacker mindset
Opportunistic abuse of misconfigured CDN services to achieve multiple attack objectives: domain reputation hijacking, malware distribution through trusted domain, SSRF reconnaissance of internal networks, and low-friction phishing/defacement campaigns.

## Defensive takeaways
- Implement strict whitelist of allowed source domains for CDN image resizing endpoints
- Validate and sanitize all URL parameters before fetching external resources
- Add origin validation headers (e.g., Referer checks) and CORS restrictions
- Disable SVG rendering or implement Content-Security-Policy to prevent HTML injection
- Implement request rate limiting and monitoring for /cdn-cgi/ endpoints
- Regularly audit CDN configurations for overly permissive access controls
- Consider blocking private/internal IP ranges from being accessed via SSRF vectors
- Log and alert on requests to suspicious external domains

## Variant hunting
Check for similar misconfigurations on other Enjin subdomains (production.enjinusercontent.com, staging variants). Audit other Cloudflare /cdn-cgi/ endpoints across different organizations. Test image optimization, transformation, and caching endpoints for similar bypass techniques. Review other CDN providers (Akamai, AWS CloudFront, Fastly) for identical misconfiguration patterns.

## MITRE ATT&CK
- T1190
- T1498
- T1557
- T1583.004
- T1583.005
- T1566.002
- T1589.001

## Notes
The vulnerability demonstrates a critical flaw in assuming third-party CDN services implement proper access controls by default. Organizations must actively configure restrictions on what resources CDN services can fetch. The SSRF component is particularly dangerous for internal network reconnaissance. The HTML injection via SVG is a known attack vector that many developers underestimate.

## Full report
<details><summary>Expand</summary>

##Summary

Hello team,
During a review of the website: https://nft.production.enjinusercontent.com/ I discovered that any resource hosted under any external CDN can be rendered on the website without any restrictions. This behavior leads display of images or resources on the website, which may cause confusion for users or expose potentially sensitive assets or otherwise deface the websites or carry our misinformation or malware campaigns.

- You Achive :
1- HTML INJECTION
2- SSRF and Portal Scanning
3- Unrestricted rendering of resources from external CDNs

##Steps to Reproduce :

1- For HTMLi Visit : https://nft.production.enjinusercontent.com/cdn-cgi/image/width=1000,format=auto/https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/cloudflare.svg

{F3347763}

## Impact

Misuses of the cdn-cgi Misconfig to render external resources
Access control Bypass by smuggling in external resources to render at the company url unrestricted
Misinformation and platform manipulation for displayed content to any user without interaction
Attacker can redirect users to another websites, virtual defacement of your website etc.
Webpage modifications
HTML Injection

</details>

---
*Analysed by Claude on 2026-05-24*
