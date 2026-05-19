# ASP.NET ResolveUrl XSS via Cookieless Session Path Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, designed to resolve app-root-relative paths using tilde (~) notation, can be exploited to inject arbitrary URI paths when cookieless session identifiers are present in the URL. Attackers can manipulate URL segments containing session IDs (like (A(ABCD)) or (S(...))) which are preserved by ResolveUrl, allowing injection of malicious paths into resource references such as script tags.

## Attack scenario (step by step)
1. Attacker crafts a URL containing a cookieless session identifier in the path, e.g., http://target.com/(A(attacker-payload))/A/B/C/default.aspx
2. ASP.NET processes the request and ResolveUrl method encounters the ~/Script.js reference in the page
3. ResolveUrl resolves the tilde but preserves the cookieless identifier from the request path
4. The malicious identifier is inserted into the resolved path: /(A(attacker-payload))/Script.js
5. The rendered HTML contains the attacker-controlled path in script src attribute or other resource references
6. When browser processes the page, it attempts to load the malicious resource URL, enabling XSS or resource loading attacks

## Root cause
ResolveUrl method does not filter or sanitize cookieless session identifier segments (A(...), S(...), F(...)) from the incoming request path when constructing resolved URLs. ASP.NET preserves these path segments even when cookieless sessions are disabled, creating a vector for path injection into resolved resource URLs.

## Attacker mindset
An attacker recognizes that legacy ASP.NET cookieless session handling creates an unexpected interaction with modern URL resolution. By injecting special formatted path segments that ASP.NET treats as metadata rather than validating them, the attacker can pollute resource references without needing traditional input validation bypass techniques. This exploits a semantic mismatch between framework features.

## Defensive takeaways
- Validate and sanitize all URL path segments before processing, especially those containing special ASP.NET identifiers like (A(...)), (S(...)), and (F(...))
- Explicitly disable cookieless sessions in web.config if not required, and configure strict validation of any remaining cookieless-related functionality
- Implement Content Security Policy (CSP) headers to restrict script and resource loading origins
- Use ResolveUrl cautiously and apply additional sanitization to URLs destined for HTML attributes
- Audit all ResolveUrl and relative URL resolution calls for potential injection points
- Keep ASP.NET framework and runtime updated to patched versions
- Consider using absolute URLs with strict validation rather than relative resolution when dealing with user-influenced paths

## Variant hunting
['Test other URL resolution methods in ASP.NET (ResolveClientUrl, GetRouteUrl) for similar path injection', 'Investigate cookieless identifiers in other frameworks with app-root-relative path features', 'Check if other special ASP.NET path segments besides (A), (S), (F) can be abused', 'Research if this technique applies to embedded resources or static file handlers', 'Test if the vulnerability persists across different ASP.NET versions and .NET Core versions', 'Explore whether the injected paths can be used for directory traversal beyond XSS']

## MITRE ATT&CK
- T1190
- T1071
- T1566

## Notes
This technique was selected as one of the Top 10 web hacking techniques of 2019. The vulnerability represents a semantic security issue where two legitimate framework features (app-root-relative URLs and cookieless sessions) combine to create an exploitable condition. The flaw is particularly dangerous because developers using ResolveUrl for convenience may not anticipate that benign-looking path segments could be user-controlled attack vectors. Modern browsers and strict CSP policies provide some mitigation, but the core issue requires framework-level fixes or explicit developer-implemented validation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
