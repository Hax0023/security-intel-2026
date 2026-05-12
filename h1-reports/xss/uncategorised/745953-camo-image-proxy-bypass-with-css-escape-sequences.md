# Camo Image Proxy Bypass with CSS Escape Sequences

## Metadata
- **Source:** HackerOne
- **Report:** 745953 | https://hackerone.com/reports/745953
- **Submitted:** 2019-11-25
- **Reporter:** zhutyra
- **Program:** Stream (Highweb Media)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Security Filter Bypass, CSS Injection, SSRF, Request Forgery
- **CVEs:** None
- **Category:** uncategorised

## Summary
The image URL proxy filter fails to detect and sanitize CSS url() properties when they contain CSS escape sequences (e.g., \72 for 'r'). This allows bypassing the content security mechanism that proxies external image URLs through a camo service. An attacker can craft malicious CSS to cause browsers to make direct requests to arbitrary external URLs.

## Attack scenario
1. Attacker edits their profile bio or wishlist field with HTML containing CSS escape sequences
2. The server's URL filter fails to recognize 'u\72l(http://attacker.com)' as a url() function due to escaped characters
3. The payload is saved without being proxied through the camo.stream service
4. When a victim visits the attacker's profile, their browser parses the CSS escape sequences correctly
5. The browser makes a direct request to attacker.com, bypassing CSP restrictions on the proxy domain
6. Attacker can harvest visitor IPs, perform CSRF attacks, or trigger other unintended requests

## Root cause
The server-side URL sanitizer uses a simplistic regex or string matching approach that looks for literal 'url(' patterns without accounting for CSS escape sequences defined in CSS specifications. CSS allows any character to be escaped as \HH (hex) or \HHHHHH (up to 6 hex digits), which the parser failed to normalize before filtering.

## Attacker mindset
An attacker could abuse this to perform CSRF attacks, harvest visitor IP addresses, trigger unintended API calls on victim networks, or track profile visitors. The attacker recognizes that input filters often miss edge cases in character encoding schemes.

## Defensive takeaways
- Normalize all CSS escape sequences before applying URL filters (decode \XX sequences)
- Use a proper CSS parser instead of regex to identify url() functions
- Implement allowlist-based filtering rather than blacklist/replacement approaches
- Apply CSP headers to restrict resource loading origins regardless of proxy implementation
- Consider disallowing style attributes entirely in user-controlled HTML, or use a robust HTML sanitizer library
- Test filter bypass with character encoding variations (hex, unicode, double encoding, etc.)

## Variant hunting
Look for similar bypass techniques in other user input fields that accept HTML/CSS. Check if other escape sequences (unicode \UXXXXXXXX, octal \000) bypass filters. Test other CSS properties that load resources (background-image, mask, clip-path). Examine if the same issue exists in other proxy implementations or CDN services.

## MITRE ATT&CK
- T1190
- T1566
- T1583

## Notes
The reporter responsibly noted the lack of immediate exploitability due to CSP, but correctly identified it as a security filter bypass. The vulnerability chain could be dangerous with additional weaknesses (CSRF tokens, network position attacks, or if CSP were misconfigured). The fix requires proper CSS normalization, not just a simple regex pattern adjustment.

## Full report
<details><summary>Expand</summary>

## Summary

With CSS escape sequences it is possible to bypass CSS url detection and filtering.

## Details

Users can use HTML tags in their Profile Bio in *About Me* and *Wish List* fields. Among other filtering and sanitization, image URLs are replaced by URLs on internal image proxy. For example, this content in *About Me*:
```html
<span style="background:url(http://foo.com/bar)">XX</span>
```
Will be replaced by this:
```html
<span style="background:url(https://camo.stream.highwebmedia.com/f923a95762fc0b6025015c00b58922b72f25096d/687474703a2f2f666f6f2e636f6d2f626172)" target="_blank" rel="nofollow">XX</span>
```
The problem is that the parser doesn't support CSS escape sequences, and for example this form, with letter `r` written as hexadecimal escape sequence, will not be detected as image link:
```html
<span style="background:u\72l(http://foo.com/bar)">XX</span>
```
## Steps To Reproduce:

Put the code mentioned above in your Bio.
{F643234}
After saving the edit, you can use the Developer Tools to inspect the element and see that the URL has not been replaced.
{F643235}
And in Network monitor in Developer Tools you can see that it was processed. In this case blocked by Content Security Policies.
{F643236}

## Note

I'm not aware of any immediate security threat from this. Like, I have no accompanying CSRF or information leak and I assume use of browsers that adhere to CSP. But definitely it is something that should be fixed.

## Impact

The room owner can force room visitors to make unintended URL requests.

</details>

---
*Analysed by Claude on 2026-05-12*
