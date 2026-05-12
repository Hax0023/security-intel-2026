# ActionView sanitize helper bypass leading to XSS using SVG tag

## Metadata
- **Source:** HackerOne
- **Report:** 1694173 | https://hackerone.com/reports/1694173
- **Submitted:** 2022-09-07
- **Reporter:** haqpl
- **Program:** Rails/Ruby on Rails
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), HTML Sanitization Bypass, SVG-based XSS
- **CVEs:** CVE-2022-23515, CVE-2022-23518
- **Category:** web-api

## Summary
The Rails ActionView sanitize helper could be bypassed using SVG `use` tags combined with base64-encoded data URIs, allowing execution of arbitrary JavaScript. When SVG and use tags were explicitly whitelisted in sanitization configuration, attackers could embed malicious SVG payloads within the data attribute to execute code.

## Attack scenario
1. Attacker identifies application uses sanitize helper with svg and use tags whitelisted
2. Attacker crafts SVG containing image element with onerror event handler
3. Attacker base64 encodes the malicious SVG payload
4. Attacker injects outer SVG with use tag referencing base64-encoded payload via data URI
5. Sanitizer allows the structure through whitelist, base64 content is decoded client-side
6. Browser executes onerror handler in malicious nested SVG, stealing user data or session tokens

## Root cause
The sanitization filter did not properly validate or restrict the href attribute of SVG use tags, specifically data URIs containing base64-encoded content. The nested SVG within the data URI was decoded and executed without additional sanitization checks, allowing event handlers in the embedded content to execute.

## Attacker mindset
Attacker recognized that SVG use tags enable resource references through href attributes and that base64-encoded data URIs could bypass simple content filtering. By nesting malicious SVG within an allowed tag's attribute, the attacker exploited the trust placed in whitelisted tag names without scrutinizing their behavioral capabilities.

## Defensive takeaways
- Never rely solely on tag whitelisting for HTML sanitization; validate and restrict dangerous attributes like href, src, and data URIs
- Apply recursive sanitization to attribute values, especially those containing encoded content (base64, percent-encoding)
- SVG presents elevated XSS risk due to event handlers and embedding capabilities; require explicit, strict whitelisting of SVG features
- Review sanitization configuration regularly; whitelisting SVG/use tags requires deep understanding of SVG attack vectors
- Use Content Security Policy (CSP) to restrict script execution and data URI usage as defense-in-depth
- Prefer server-side rendering libraries over client-side HTML sanitization when possible
- Test sanitization bypass techniques including encoding variations, nested structures, and namespace manipulation

## Variant hunting
Test other SVG embedding techniques: object, embed, iframe tags with data URIs
Attempt XSS through other SVG elements with href/xlink:href: image, animation tags
Try percent-encoding or double base64 encoding to bypass decoding checks
Test MathML similar attack patterns if allowed in sanitization
Explore other event handlers in SVG contexts: onload, onbegin, onend
Test nested use tags referencing further encoded payloads
Investigate style-based XSS in SVG: style attribute with CSS expressions or filters

## MITRE ATT&CK
- T1190
- T1059.007
- T1566.002
- T1204.001

## Notes
This vulnerability required specific configuration (whitelisting svg and use tags) making it lower impact in default Rails installations. However, developers who explicitly enable SVG sanitization often do so to support rich content features, making them vulnerable if not aware of SVG attack vectors. The use of data URIs with base64 encoding is a common obfuscation technique in XSS attacks that sanitizers must explicitly handle.

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
