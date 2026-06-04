# ASP.NET ResolveUrl XSS via Cookieless Session Identifiers

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), URL Path Traversal, Session Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method improperly handles cookieless session identifiers (format: (A()), (S()), (F())) injected into URL paths, allowing attackers to manipulate resolved resource paths. When an attacker injects these identifiers into the URL, ResolveUrl preserves them in the resolved path, enabling injection of arbitrary URIs into HTML attributes like script src, resulting in XSS attacks.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl() for resource resolution (e.g., <script src="<%= ResolveUrl("~/Script.js") %>"></script>)
2. Attacker crafts a malicious URL containing cookieless session identifier syntax: http://target.com/(A(PAYLOAD))/A/B/C/default.aspx or http://target.com/A/B/C/(A(PAYLOAD))/default.aspx
3. Victim clicks the crafted link or is redirected to it
4. ASP.NET processes the request and ResolveUrl() constructs the resource path while preserving the injected identifier: <script src="/(A(PAYLOAD))/Script.js"></script>
5. Browser parses the malicious script tag, treating the identifier portion as part of the URL path
6. Attacker can inject XSS payload or redirect to external malicious script, executing arbitrary JavaScript in victim's browser context

## Root cause
ResolveUrl method does not sanitize or validate cookieless session identifiers present in the URL path before resolving app-root-relative URLs (~). The method treats these identifiers as legitimate path components and includes them in the resolved path, violating the expectation that only the application root path would be prepended to the tilde-prefixed resource.

## Attacker mindset
Exploit framework conveniences designed to reduce developer burden. Leverage legitimate ASP.NET features (cookieless sessions, ResolveUrl) in unintended ways to achieve code execution. Target the disconnect between legacy session management features and modern URL handling assumptions.

## Defensive takeaways
- Validate and sanitize all URL path components, including those that appear to be session identifiers
- Implement strict Content Security Policy (CSP) headers to restrict script sources and prevent inline script execution
- Use explicit absolute paths or Content-Relative URLs instead of relying on ResolveUrl when security-critical (especially for script/stylesheet inclusion)
- Disable cookieless sessions if not required; explicitly set SessionStateSection.Cookieless to 'UseCookies'
- Apply output encoding to all resource URLs before rendering in HTML attributes
- Regularly update ASP.NET framework to patch ResolveUrl behavior
- Implement URL canonicalization to detect and reject malformed paths containing cookieless identifiers in unexpected locations

## Variant hunting
['Test other ResolveUrl contexts beyond script src (stylesheets, images, form actions, iframes)', 'Investigate whether other ASP.NET URL resolution methods (ClientScriptManager.GetWebResourceUrl, Page.ResolveClientUrl) have similar issues', 'Check if data attributes or HTML5 custom attributes using ResolveUrl are exploitable', 'Test ASP.NET MVC/Core equivalents of URL resolution mechanisms', 'Examine third-party URL resolution libraries built on top of ResolveUrl', 'Test encoded variations of session identifier syntax: %28A%28, &#40;A&#40;, etc.', 'Analyze whether ResolveUrl is affected when combined with other ASP.NET features (URL routing, Module rewriting)']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539

## Notes
This technique was selected as one of Top 10 web hacking techniques of 2019. The vulnerability highlights the danger of mixing legacy compatibility features (cookieless sessions from ASP.NET v1.0) with modern URL resolution mechanisms. The issue is particularly insidious because ResolveUrl() is documented and recommended for handling application-relative paths, yet developers using it have little reason to suspect it could introduce XSS. The root cause is ASP.NET's permissive handling of cookieless identifiers even when they are disabled in configuration—the framework accepts them in URLs without validation, which ResolveUrl then preserves.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
