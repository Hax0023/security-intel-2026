# ASP.NET ResolveUrl Path Traversal Leading to XSS via Cookieless Session Identifiers

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Injection
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, designed to safely resolve app-root-relative paths using tilde (~) notation, can be exploited to inject arbitrary URI paths by abusing cookieless session identifiers. Attackers can inject malicious paths like (A(ABCD)) into URLs, which ResolveUrl will incorporate into resolved script src attributes, enabling XSS attacks even when cookies are disabled or AutoDetect is configured.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl to reference resources with ~/path notation
2. Attacker crafts a malicious URL containing cookieless session identifier syntax, e.g., http://target.com/(A(payload))/page.aspx
3. ASP.NET accepts the malicious identifier in the URL path despite cookieless sessions being disabled
4. ResolveUrl resolves ~/Script.js and inadvertently incorporates the injected identifier into the path
5. Browser renders <script src="/(A(payload))/Script.js"></script> pointing to attacker-controlled location
6. XSS payload executes in user's browser, compromising session or stealing credentials

## Root cause
ASP.NET's ResolveUrl method does not properly validate or sanitize cookieless session identifiers (A(?), S(?), F(?)) in URL paths before resolving tilde-notation paths. The framework accepts these identifiers in URLs regardless of cookieless session configuration, and ResolveUrl naively incorporates them into resolved paths without stripping them out.

## Attacker mindset
Exploit framework convenience features that were designed for backward compatibility. Recognize that ASP.NET's permissive URL handling of legacy cookieless identifiers can be weaponized. Target the gap between what developers expect ResolveUrl to do (safely resolve paths) and what it actually does (preserve injected path components).

## Defensive takeaways
- Implement strict input validation on all URL segments, including legacy session identifier formats
- Do not rely solely on ResolveUrl for XSS prevention; implement additional output encoding for all dynamic path attributes
- Disable cookieless sessions explicitly and reject requests containing cookieless identifiers with HTTP 400 errors
- Use Content Security Policy (CSP) headers with strict script-src directives to mitigate XSS impact
- Regularly audit resource inclusion mechanisms and test with various URL path injection patterns
- Consider using sealed/signed URLs or explicit whitelisting for resource paths instead of dynamic resolution

## Variant hunting
['Test with Form Authentication identifier syntax: (F(payload))', 'Test with Anonymous ID syntax: (A(payload)) in various URL path positions', 'Probe other ASP.NET path resolution methods (AppRelativeCodeExpressionBuilder, VirtualPathUtility.ToAbsolute)', 'Test interaction with URL rewriting modules that may further process paths', 'Investigate other attribute contexts beyond src (href, data, etc.)', 'Test with nested identifiers: (A(A(payload)))', 'Check if issue affects both aspx and compiled controls differently', 'Test with other virtual path notations (~/../../, ./ combinations)']

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability was selected as one of Top 10 web hacking techniques of 2019. The issue highlights the danger of framework features designed for convenience without adequate security consideration. The cookieless session feature is a legacy compatibility mechanism that creates an attack surface in modern configurations. Developers may be unaware that ResolveUrl does not strip path components it doesn't recognize, treating them as valid path elements instead.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
