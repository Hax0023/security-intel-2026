# ASP.NET ResolveUrl Path Traversal Leading to XSS via Cookieless Session Identifiers

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, designed to resolve app-root-relative URLs using the tilde (~) notation, can be exploited to inject arbitrary paths when cookieless session identifiers are present in the URL. Attackers can inject malicious URIs into script and resource tags by manipulating URL-based session identifiers like (A(ABCD)), (S(SESSIONID)), or (F(AUTHTICKET)), even when the application is configured to use cookies exclusively.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl with tilde notation for resource inclusion (e.g., ~/Script.js)
2. Attacker crafts a URL containing cookieless session identifiers in the path segment: http://localhost/(A(ATTACKER_PAYLOAD))/A/B/C/default.aspx
3. When the page renders, ResolveUrl processes the tilde and inadvertently includes the injected identifier in the resolved path
4. The injected path appears in the rendered HTML as <script src="/(A(ATTACKER_PAYLOAD))/Script.js"></script>
5. Attacker uses this mechanism to inject external script sources or craft paths that redirect to malicious resources
6. Browser executes the malicious script, leading to session hijacking, credential theft, or data exfiltration

## Root cause
ASP.NET's ResolveUrl method does not properly sanitize or validate URL path segments that contain cookieless session identifiers before resolving tilde-based paths. The framework treats these identifiers as legitimate path components rather than reserved syntax, allowing them to be injected into resolved URLs.

## Attacker mindset
The attacker exploits a misunderstanding between the framework's convenience feature (automatic path resolution) and its legacy support for cookieless sessions. By recognizing that ASP.NET still processes cookieless identifiers even when disabled, the attacker leverages this discrepancy to manipulate URLs in a way that appears legitimate to the application but injects arbitrary paths into resource references.

## Defensive takeaways
- Validate and sanitize all user-controlled input in URL paths, including session identifiers and path segments, before using them in ResolveUrl or similar methods
- Explicitly disable cookieless session support in web.config if not required, and ensure configuration is properly enforced
- Use Content Security Policy (CSP) headers to restrict script execution and prevent loading resources from unexpected origins
- Implement URL encoding and path normalization before resolving app-relative paths
- Avoid placing user-controllable data in URL path segments that will be processed by path resolution methods
- Use subresource integrity (SRI) for external scripts to verify authenticity
- Test path resolution logic with various URL encodings and injected identifiers to identify similar vulnerabilities

## Variant hunting
Search for similar path traversal vulnerabilities in other frameworks with app-relative path resolution features (e.g., Ruby on Rails asset pipelines, PHP include_path handling). Investigate other ASP.NET path resolution methods like ResolveClientUrl, ResolveServerUrl, and custom path helpers. Test URL-based authentication mechanisms (Forms Authentication Tickets) for similar injection possibilities. Examine applications using URL rewriting modules that may interact unexpectedly with path resolution.

## MITRE ATT&CK
- T1190
- T1583.001
- T1598.003

## Notes
This vulnerability was recognized as one of the Top 10 web hacking techniques of 2019. The core issue is ASP.NET's backward compatibility with cookieless sessions—the framework continues processing session identifiers in URLs even when the feature is explicitly disabled, creating an unexpected attack surface. The vulnerability is particularly dangerous because it affects a fundamental framework feature (ResolveUrl) used throughout ASP.NET applications for resource inclusion.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
