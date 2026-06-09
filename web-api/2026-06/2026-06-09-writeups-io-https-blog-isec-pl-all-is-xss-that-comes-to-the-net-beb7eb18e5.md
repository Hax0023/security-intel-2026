# ASP.NET ResolveUrl XSS via Cookieless Session Identifiers

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), URL Path Traversal, Session Management Bypass
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, when combined with cookieless session identifiers, allows attackers to inject arbitrary URI paths into resolved URLs, enabling XSS attacks. By inserting malicious session identifiers like (A(ABCD)) into request URLs, attackers can manipulate how relative paths are resolved in script and resource tags, even when the application disables cookieless sessions.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing a cookieless session identifier, e.g., http://localhost/(A(PAYLOAD))/A/B/C/default.aspx
2. Victim visits the malicious link or clicks it from an email/social engineering campaign
3. ASP.NET processes the request and encounters the (A(PAYLOAD)) segment in the URL path
4. The ResolveUrl method resolves ~/Script.js while preserving the injected path segment, resulting in <script src="/(A(PAYLOAD))/Script.js"></script>
5. Browser interprets the malformed path as a valid resource request to an attacker-controlled domain or protocol handler
6. JavaScript payload executes in the victim's browser with the application's context, allowing session hijacking, credential theft, or malware delivery

## Root cause
ASP.NET's ResolveUrl method does not properly sanitize or validate URL path components when resolving application-root-relative paths (~). The method preserves cookieless session identifiers in the URL even when they are not explicitly enabled, allowing attackers to inject arbitrary path components that get incorporated into resolved resource URLs.

## Attacker mindset
Attackers exploit the implicit trust in framework-provided URL resolution functions. By understanding that developers rely on ResolveUrl for security and convenience, attackers leverage the framework's backward compatibility with legacy cookieless session features to bypass expected path resolution behavior. This is a classic case of framework feature interaction creating unintended attack surface.

## Defensive takeaways
- Validate and sanitize all URL components, especially those that appear in resource references (scripts, stylesheets, images)
- Disable cookieless sessions explicitly in web.config and validate that the application handles URL-based session identifiers safely
- Use Content Security Policy (CSP) headers to restrict script execution and resource loading sources
- Implement URL parsing and validation to detect anomalous path segments like (A(...)), (S(...)), or (F(...))
- Regularly audit framework documentation and update knowledge of feature interactions that could create security gaps
- Use context-aware output encoding when generating resource URLs, especially when framework methods are involved
- Consider using absolute CDN URLs or integrity checking (SRI) for static resources to reduce reliance on dynamic URL resolution

## Variant hunting
['Investigate other ASP.NET URL resolution methods (Url.Content, Url.RouteUrl) for similar behavior', 'Test whether other framework methods inadvertently preserve special URL segments', 'Examine applications using Server.MapPath with user-influenced paths combined with cookieless identifiers', 'Search for applications embedding ResolveUrl output in CSS, data attributes, or event handlers', 'Test interaction between cookieless identifiers and URL rewriting modules that may double-process paths', 'Investigate whether Form Authentication Ticket (F(...)) and Anonymous ID (A(...)) identifiers have similar exploitation vectors', 'Check if path-based session handling in other frameworks (Java, Python, PHP) suffer similar issues when combined with URL resolution helpers']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1059

## Notes
This vulnerability was selected as one of Top 10 web hacking techniques of 2019. The attack is particularly insidious because it exploits the interaction between a legacy feature (cookieless sessions) and a modern convenience feature (ResolveUrl), both considered secure in isolation. The vulnerability affects any ASP.NET application using ResolveUrl for resource paths, regardless of whether cookieless sessions are explicitly enabled. The attacker need not control a server; they only need to trick users into clicking specially-crafted links. Remediation requires understanding both the historical context of cookieless sessions and the limitations of path resolution functions.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
