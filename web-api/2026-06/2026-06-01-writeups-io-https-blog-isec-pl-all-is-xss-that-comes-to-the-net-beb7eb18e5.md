# ASP.NET ResolveUrl XSS via Cookieless Session ID Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, which resolves app-root-relative paths using the tilde (~) notation, fails to properly sanitize cookieless session identifiers injected into URLs. An attacker can inject arbitrary URI paths containing malicious payloads through the (A()), (S()), or (F()) syntax, which ASP.NET preserves and includes in resolved resource URLs, leading to XSS attacks.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing a cookieless session identifier with XSS payload: http://localhost/(A(ABCD))/A/B/C/default.aspx
2. Victim visits the crafted URL or clicks a link to it
3. ASP.NET application renders the page with ResolveUrl() calls that reference resources like ~/Script.js
4. ResolveUrl preserves the injected session ID in the resolved path: /(A(ABCD))/Script.js
5. The script tag renders with the attacker-controlled path: <script src="/(A(ABCD))/Script.js"></script>
6. Browser attempts to load the resource from the injected path, allowing payload execution or redirect to attacker-controlled domain

## Root cause
ASP.NET's ResolveUrl method does not strip or validate cookieless session identifiers (A(), S(), F()) from the URL path before resolving tilde-prefixed relative paths. The method preserves these identifiers when computing the resolved URL, treating them as legitimate path components rather than special session tokens.

## Attacker mindset
An attacker recognizes that ASP.NET's backward compatibility with cookieless sessions creates an overlooked input vector. By understanding how ResolveUrl processes paths and how session identifiers are formatted, the attacker realizes they can inject arbitrary content into resolved URLs without triggering validation, enabling XSS in contexts where direct query parameter/form input XSS might be blocked.

## Defensive takeaways
- Validate and sanitize all URL components, including session identifiers, before using them in resource resolution
- Implement strict output encoding for all dynamically generated URLs, especially in script src and link href attributes
- Disable cookieless sessions in web.config (set cookieless="UseCookies") unless explicitly required, and document the security implications
- Use Content Security Policy (CSP) headers to restrict script loading to trusted domains and prevent injection attacks
- Apply input validation to reject URLs containing suspicious patterns like parentheses-wrapped identifiers in unexpected locations
- Consider using ASP.NET's built-in URL encoding utilities consistently across the application
- Implement additional path validation to ensure resolved URLs conform to expected application structure

## Variant hunting
['Test other ASP.NET built-in functions that resolve relative paths (ResolveClientUrl, GetWebResourceUrl) for similar vulnerabilities', 'Check for similar issues in other server-side frameworks with path resolution features (Java, PHP, Ruby)', 'Investigate whether other special URL formats recognized by ASP.NET can be injected similarly', 'Test if HTML5 forms, iframes, and other resource-loading contexts are affected', 'Examine third-party libraries that wrap or extend ResolveUrl functionality', 'Probe for variations using different session identifier formats or encoding techniques']

## MITRE ATT&CK
- T1190
- T1598

## Notes
This vulnerability was selected as one of Top 10 web hacking techniques of 2019. The attack leverages a feature designed for convenience (app-root-relative URLs) combined with backward compatibility support (cookieless sessions) to achieve code execution. The vulnerability is particularly dangerous because it affects framework-level functionality that many developers rely on without security scrutiny, and successful exploitation can lead to session hijacking, credential theft, or malware injection.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
