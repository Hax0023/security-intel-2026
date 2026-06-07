# ASP.NET ResolveUrl Path Traversal Leading to XSS via Cookieless Session Identifiers

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, designed to resolve app-root-relative URLs using tilde (~) notation, can be exploited to inject arbitrary URI paths through cookieless session identifiers. When cookieless sessions are enabled or when the application accepts such identifiers, attackers can inject malicious paths into resolved URLs, leading to XSS vulnerabilities in resource includes like scripts and stylesheets.

## Attack scenario (step by step)
1. Attacker crafts a URL containing a cookieless session identifier in the format (A(PAYLOAD)) or (S(PAYLOAD))
2. Attacker places the identifier either before the application path or within the path hierarchy: http://localhost/(A(PAYLOAD))/A/B/C/default.aspx
3. The application serves the page with a script tag using ResolveUrl(~/Script.js)
4. ASP.NET's ResolveUrl method preserves the cookieless identifier while resolving the tilde, resulting in: <script src="/(A(PAYLOAD))/Script.js"></script>
5. The browser interprets this as a valid script path and may execute malicious content from the attacker-controlled path
6. Session data or other sensitive resources can be exfiltrated or XSS payload delivered depending on server configuration

## Root cause
ResolveUrl method does not sanitize or strip cookieless session identifiers from the resolved path. The method treats these identifiers as legitimate path components and preserves them in the output, even when cookieless sessions are disabled. This allows attackers to inject arbitrary path segments that become part of the resolved URL.

## Attacker mindset
An attacker recognizes that legacy ASP.NET features (cookieless sessions) are still processed by the framework even when disabled. They exploit the fact that ResolveUrl blindly preserves URL structure, including session identifiers, treating attacker-controlled input as legitimate path components. The attacker abuses a convenience feature (automatic path resolution) to achieve code execution.

## Defensive takeaways
- Validate and sanitize all URL components before using them in resource includes; implement strict URL parsing to reject or strip cookieless identifiers
- Disable cookieless sessions entirely if not required; set SessionStateSection.Cookieless to UseCookies and enforce this configuration
- Use Content Security Policy (CSP) headers to restrict script execution and prevent unauthorized resource loading
- Implement URL validation logic that explicitly removes or rejects patterns matching cookieless session identifier formats (S(...), A(...), F(...))
- Use absolute, fully-qualified URLs for critical resources rather than relying on relative path resolution
- Apply output encoding to all dynamically generated URLs and test URL generation with malicious input
- Regularly audit ResolveUrl usage across the codebase and consider custom wrapper functions with validation

## Variant hunting
['Test ResolveUrl with other ASP.NET path manipulation patterns (e.g., directory traversal sequences, URL-encoded variants)', 'Investigate ResolveClientUrl method for similar vulnerabilities', 'Check if other frameworks using tilde-notation path resolution have similar issues', 'Test with cookieless authentication tickets (F(...)) instead of session identifiers', 'Examine how ResolveUrl behaves with doubly-encoded session identifiers or special characters', 'Investigate if virtual directory deployments compound this vulnerability', 'Test combinations of multiple cookieless identifiers in a single path', 'Check for similar issues in client-side URL resolution mechanisms']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1204 - User Execution

## Notes
This vulnerability was recognized as a Top 10 web hacking technique of 2019. The attack exploits the assumption that cookieless identifiers are only present in legitimate requests, when they can actually be injected by attackers. The vulnerability particularly affects applications using ASP.NET v2.0 or later with ResolveUrl for script/stylesheet includes. The fix requires explicit validation logic rather than framework patches, as the behavior is by design. Organizations should audit all uses of ResolveUrl, especially in pages that include external resources.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
