# Reflected XSS on Multiple Starbucks Assets via Double-Encoded Payload in 404 Pages

## Metadata
- **Source:** HackerOne
- **Report:** 629745 | https://hackerone.com/reports/629745
- **Submitted:** 2019-06-26
- **Reporter:** stealthy
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), WAF Bypass, Input Validation Failure
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple Starbucks websites (starbucks.co.uk, starbucks.fr, etc.) are vulnerable to reflected XSS on 404 error pages due to insufficient sanitization of double quotes in hidden input tags and canonical link elements. An attacker can bypass the WAF's double-quote filter using double-URL encoding to inject malicious JavaScript that executes in victim browsers via accesskey and onclick event handlers.

## Attack scenario
1. Attacker crafts a payload using double-encoded characters (%2522 for ", %2520 for space) to bypass WAF filtering of double quotes
2. Attacker creates a malicious URL with the encoded payload as a path parameter (e.g., starbucks.co.uk/PAYLOAD)
3. Attacker sends the link to victims via phishing email, social media, or other social engineering tactics
4. Victim clicks the link and is redirected to a Starbucks 404 error page
5. The unencoded payload is reflected in the canonical link href and input tag attributes without proper escaping
6. JavaScript executes when victim uses accesskey keyboard shortcut (CTRL+ALT+X on Mac, ALT+SHIFT+X on Windows), stealing session tokens, personal data, or performing unauthorized actions

## Root cause
The application reflects user-supplied URL path parameters into HTML attributes (canonical link href and input value) without proper sanitization or escaping. While the WAF blocks direct double-quote characters, it fails to detect double-encoded payloads (%2522). Upon decoding the URL, the quotes are reconstructed in the HTML, allowing attribute breakout and event handler injection.

## Attacker mindset
An attacker discovered this vulnerability while testing SQL injection filters and recognized the reflected input in HTML source. They leveraged knowledge of HTML entity encoding, WAF bypass techniques, and browser keyboard shortcut behavior (accesskey) to craft a reliable exploit that executes without user interaction beyond a keyboard shortcut.

## Defensive takeaways
- Implement output encoding/escaping appropriate to context (HTML entity encoding for HTML attributes, JavaScript encoding for JavaScript contexts)
- Validate and sanitize all user input at server-side, not relying solely on client-side or WAF filtering
- Apply defense-in-depth: use both input validation AND output encoding
- Ensure WAF rules detect double-encoded payloads and other encoding bypasses
- Use Content Security Policy (CSP) with strict directives to prevent inline script execution
- Avoid reflecting user input in sensitive HTML attributes; use safe alternatives like data attributes
- Test error pages and less-trafficked URLs for XSS vulnerabilities, as they are often overlooked
- Implement automated security scanning covering multiple encoding layers
- Educate developers on XSS prevention best practices and secure coding patterns

## Variant hunting
Test other encoding schemes (triple-encoding, mixed encoding, UTF-8 encoding) against WAF rules
Check other Starbucks subdomains and regional sites for similar 404 page implementations
Investigate if other HTML attributes beyond canonical href are vulnerable (meta tags, script src, iframe src)
Test if the vulnerability exists on other error pages (403, 500, etc.) or search result pages
Examine if accesskey vulnerabilities exist on other elements (form inputs, links) without onclick handlers
Check if similar WAF bypass techniques work against other filters (angle brackets, event handlers, data URIs)
Test if SVG or data URI payloads can bypass the WAF filters
Investigate reflected parameters in other parts of the application for similar encoding bypass opportunities

## MITRE ATT&CK
- T1190
- T1566.002
- T1566.003

## Notes
The accesskey vector is noteworthy as it requires a keyboard shortcut to trigger, reducing but not eliminating impact. The multi-domain scope (co.uk, .fr, etc.) suggests a shared codebase vulnerability. The WAF bypass via double-encoding demonstrates the importance of testing encoding attacks against security controls. The vulnerability was discovered serendipitously while testing SQL injection, highlighting the value of broad security testing approaches.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Please indicate NA, if not applicable. Remember, the more detail you provide, the easier it is for us to verify and then potentially issue a bounty, so be sure to take your time filling out the report!

**Summary:** [Many Starbucks websites are vulnerable to cross-site scripting on 404 pages because double quotes lack sanitizing in hidden input tags, which leads to JavaScript execution.]

**Description:** [Starbucks employs a WAF which redirects any URL with a double quote to an error page. However, using double encoding, this can be bypassed. I used double encoding for most of the payload, which includes white spaces. My payload is below.

```text
htp8bi2zcg%2522%2520accesskey=%2527x%2527%2520onclick=%2527confirm`1`%2527%2520//2injectiontrme47nbfq/blonde/bright-sky-blend/ground=1
```
The payload is just the on click event with the access key set as x, and the rest of a Starbucks URL added as an arbitrary parameter to make sure the onclick event works.
```text
htp8bi2zcg" accesskey='x' onclick='confirm`1`' //2injectiontrme47nbfq/blonde/bright-sky-blend/ground=1
```
This vulnerability affects multiple Starbucks websites. Two are listed below.

    https://www.starbucks.co.uk/htp8bi2zcg%2522%2520accesskey=%2527x%2527%2520onclick=%2527confirm%601%60%2527%2520//2injectiontrme47nbfq/blonde/bright-sky-blend/ground=1

    https://www.starbucks.fr/htp8bi2zcg%2522%2520accesskey=%2527x%2527%2520onclick=%2527confirm%601%60%2527%2520//2injectiontrme47nbfq/blonde/bright-sky-blend/ground=1

The vulnerable HTML is below.
```html
<link rel="canonical" href="https://www.starbucks.co.uk/htp8bi2zcg" accesskey="x" onclick="confirm`1`" 2injectiontrme47nbfq="" blonde="" bright-sky-blend="" ground="1&quot;">
```
As you can see, the injection is successful.]

**Platform(s) Affected:** [Tested in Firefox Quantum 67.0.]

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

1: Visit the link below.

    https://www.starbucks.fr/htp8bi2zcg%2522%2520accesskey=%2527x%2527%2520onclick=%2527confirm%601%60%2527%2520//2injectiontrme47nbfq/blonde/bright-sky-blend/ground=1

2: The key bind on MAC is CONTROL+ALT+X and on Windows is ALT+SHIFT+X.

## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, etc.)
{F516988}
██████


## How can the system be exploited with this bug?
Execute arbitrary JavaScript in a victim's browser to steal information or perform unwanted actions on the victim's behalf.

## How did you come across this bug ?
I was trying to bypass the double quote filter for SQL injection and came across this XSS when I looked at the HTML.

## Recommendations for fix
 
* Escape double quotes.

## Impact

JavaScript is against Starbucks users on multiple critical domains. JavaScript execution results in information theft and an attacker can perform unwanted actions on a victim's behalf.

</details>

---
*Analysed by Claude on 2026-05-12*
