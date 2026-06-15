# All is XSS that comes to the .NET - ASP.NET ResolveUrl Path Traversal leading to XSS

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** ASP.NET Framework (General/Multiple)
- **Bounty:** Not specified - Top 10 web hacking techniques of 2019
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method for handling app-root-relative URLs (~) can be abused when combined with cookieless session identifiers injected into URL paths. An attacker can manipulate the URL path segments to inject arbitrary paths into script src and resource attributes, bypassing intended directory structures and causing the application to load attacker-controlled resources from unexpected locations.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl with tilde (~) notation for resource paths (e.g., <script src='~/Script.js'></script>)
2. Attacker discovers the application is vulnerable to cookieless session identifier injection or the app accepts such identifiers in URLs without strict validation
3. Attacker crafts a malicious URL incorporating ASP.NET path segments like (A(ABCD)) or (S(sessionid)) within the URL hierarchy
4. When a victim visits the crafted URL, ResolveUrl resolves the tilde relative to the poisoned path, causing the resolved path to include the injected segment
5. The browser renders <script src='/(A(ABCD))/Script.js'></script> which loads from an attacker-controlled or poisoned path location
6. If attacker can host content at that path or perform path traversal, arbitrary JavaScript is executed in the victim's browser context

## Root cause
ASP.NET's ResolveUrl method does not properly sanitize or validate URL path segments when resolving tilde (~) relative paths. The method treats cookieless session identifiers and other URL-injected segments as legitimate path components, allowing them to alter the final resolved URL without validation. The framework accepts these identifiers even when cookieless sessions are disabled, creating an unexpected attack surface.

## Attacker mindset
An attacker recognizes that convenience features (app-root-relative URLs via ResolveUrl) can be weaponized when combined with legacy features (cookieless session support) that are maintained for backward compatibility. The attacker exploits the gap between what developers expect the URL to resolve to and what it actually resolves to when path manipulation occurs. By injecting legitimate-looking ASP.NET path syntax, the attacker blends their payload into the URL structure, evading naive validation.

## Defensive takeaways
- Validate and sanitize all URL path components before processing, especially those appearing to be session identifiers or special ASP.NET markers
- Implement strict URL parsing that explicitly rejects or isolates cookieless session identifier patterns (A(?), S(?), F(?)) if not explicitly required
- Use Content Security Policy (CSP) headers to restrict script and resource loading to expected origins and paths
- Avoid relying solely on ResolveUrl for security; implement additional path validation for dynamically resolved resource URLs
- Disable cookieless sessions entirely via web.config if not required for legacy browser support, and explicitly reject URLs containing these patterns
- Implement allowlist-based validation for resource paths before rendering them in HTML attributes
- Consider using integrity attributes (SRI - Subresource Integrity) on critical script tags to prevent loading of unexpected resources

## Variant hunting
['Test other ASP.NET ResolveUrl variants and similar path resolution methods in VB.NET applications', 'Check if the vulnerability extends to other resource types: stylesheets (link href), images (img src), iframes (iframe src)', 'Test if Server.MapPath has similar vulnerabilities when combined with user input or URL segments', 'Investigate if ASP.NET Core applications with similar path resolution logic are vulnerable', 'Look for similar path traversal patterns in other frameworks that support relative path resolution (e.g., Java, PHP)', 'Test if combining multiple path segments or nested parentheses can bypass validation: (A(A(ABCD)))', 'Check if URL encoding of the session identifier pattern bypasses detection: %28A%28ABCD%29%29']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1059

## Notes
This vulnerability highlights the danger of maintaining backward compatibility features (cookieless sessions from ASP.NET v1.0/v1.1 era) without proper isolation. The technique was recognized as one of Top 10 web hacking techniques of 2019. The vulnerability is particularly subtle because ResolveUrl is considered a 'best practice' convenience feature, making developers less likely to apply additional security validation. The attack leverages the gap between framework behavior (accepting cookieless identifiers even when disabled) and developer expectations (URL normalization without security implications). This writeup demonstrates excellent real-world security research by connecting disparate framework features to create a novel attack vector.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
