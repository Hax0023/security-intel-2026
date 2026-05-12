# Rails ActionView sanitize helper bypass leading to XSS using SVG tag

## Metadata
- **Source:** HackerOne
- **Report:** 1805873 | https://hackerone.com/reports/1805873
- **Submitted:** 2022-12-14
- **Reporter:** haqpl
- **Program:** Ruby on Rails
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), HTML Sanitization Bypass, SVG-based Attack
- **CVEs:** CVE-2022-23515
- **Category:** web-api

## Summary
The Rails ActionView sanitize helper can be bypassed when SVG and use tags are whitelisted, allowing attackers to embed base64-encoded SVG payloads containing XSS vectors. By leveraging the SVG use tag's href attribute with data URIs, an attacker can execute arbitrary JavaScript despite sanitization attempts.

## Attack scenario
1. Attacker identifies that an application uses sanitize helper with svg and use tags whitelisted in configuration or inline
2. Attacker crafts a payload SVG containing an image tag with onerror event handler executing malicious JavaScript
3. Attacker base64 encodes the malicious SVG payload
4. Attacker embeds the encoded payload in a use tag's href attribute as a data URI within an outer SVG element
5. When the sanitize helper processes the input, it allows the outer SVG and use tags through the whitelist
6. Browser decodes and processes the data URI, executing the JavaScript in the onerror event handler within the embedded SVG context

## Root cause
The sanitize helper's whitelist mechanism does not properly validate or restrict the href attribute values of SVG use elements. The use tag's ability to load external resources via data URIs was not considered during the whitelist design, allowing embedded SVG payloads with event handlers to bypass sanitization filters.

## Attacker mindset
An attacker would recognize that SVG elements have special parsing rules and that the use tag can reference external content. By combining base64 encoding with data URIs, they can obfuscate malicious SVG code while staying within allowed tags, exploiting the assumption that whitelisting specific tags without attribute restrictions is sufficient for security.

## Defensive takeaways
- Never whitelist SVG and use tags together without strict attribute filtering, particularly for href/xlink:href attributes
- Implement attribute-level sanitization that explicitly blocks data: URIs and javascript: protocols in href attributes
- Use a more restrictive default sanitization policy and require explicit opt-in for dangerous elements like SVG
- Consider using a dedicated SVG sanitization library (e.g., DOMPurify) rather than generic HTML sanitizers for SVG content
- Avoid relying solely on tag whitelisting; implement comprehensive attribute whitelisting with URI scheme validation
- Regularly audit sanitizer configurations and test with polyglot payloads combining multiple encoding techniques

## Variant hunting
Search for similar bypasses using: SVG script tags with CDATA sections, foreign content context escaping, XML entity expansion in SVG, use tags referencing external DTDs, animate tags with event handlers, feImage filters with href attributes, or other SVG elements supporting resource references (image, use, tref). Test combinations of nested SVG contexts and different encoding schemes (base64, URL encoding, UTF-16).

## MITRE ATT&CK
- T1190
- T1059.007

## Notes
This vulnerability demonstrates the complexity of sanitizing XML-based formats like SVG, where element and attribute interactions create security boundaries that generic HTML sanitizers may not fully understand. The base64 encoding serves as an obfuscation layer that bypasses simple pattern-matching detection. This highlights the need for format-specific security knowledge when dealing with multimedia content formats.

## Full report
<details><summary>Expand</summary>

In the specific configuration, it was possible to bypass HTML sanitization by using the `use` tag of the `SVG` element.

In the `index.html.erb`:

```ruby
<%= sanitize "<svg><use href=\"data:image/svg+xml;base64,PHN2ZyBpZD0neCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluaycgd2lkdGg9JzEzMzcnIGhlaWdodD0nMTMzNyc+CjxpbWFnZSBocmVmPSIxIiBvbmVycm9yPSJhbGVydCh3aW5kb3cub3JpZ2luKSIgLz4KPC9zdmc+#x\"/></svg>", tags: %w(svg use) %>
```
`use` tag allows to embed another base64 encoded `SVG` containing target XSS payload, base64 after decoding:

```svg
<svg id='x' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='1337' height='1337'>
<image href="1" onerror="alert(window.origin)" />
</svg>
```
`SVG` and `use` tags had to be allowed either in global configuration  `config.action_view.sanitized_allowed_tags = ['svg', 'use']`
or inline with `tags` argument of the helper.

## Impact

XSS could lead to data theft through the attacker’s ability to manipulate data through their access to the application, and their ability to interact with other users, including performing other malicious attacks, which would appear to originate from a legitimate user. These malicious actions could also result in reputational damage for the business through the impact on customers’ trust.

</details>

---
*Analysed by Claude on 2026-05-12*
