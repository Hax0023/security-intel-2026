# ASP.NET ResolveUrl XSS via Cookieless Session Identifiers

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), URL Path Manipulation, Cookie Handling Bypass
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method insecurely resolves app-root-relative paths when cookieless session identifiers are present in the URL, allowing attackers to inject arbitrary URIs into resolved resource paths. By crafting URLs containing session identifiers like (A(ABCD)), attackers can manipulate script src attributes and other resource references to point to attacker-controlled domains, leading to XSS attacks. This vulnerability affects applications using the tilde (~) path resolution feature regardless of whether cookieless sessions are explicitly enabled.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing a cookieless session identifier: http://localhost/(A(malicious))/A/B/C/default.aspx
2. The victim clicks the link or is redirected to this URL by the attacker
3. ASP.NET processes the request and passes the session identifier through ResolveUrl
4. ResolveUrl generates: <script src="/(A(malicious))/Script.js"></script>
5. The browser interprets the path as a valid URL and attempts to load the script from the attacker's domain
6. Attacker-controlled JavaScript executes in the victim's browser within the application's origin context

## Root cause
ResolveUrl fails to sanitize or validate cookieless session identifiers before resolving tilde-prefixed paths. The method treats these identifiers as legitimate path components, allowing them to be injected into the resolved URL without validation. Additionally, ASP.NET continues accepting and processing cookieless identifiers even when the feature is explicitly disabled via configuration.

## Attacker mindset
An attacker recognizes that legacy ASP.NET session management mechanisms are still processed despite modern defaults, creating an overlooked attack surface. They understand that framework convenience features (ResolveUrl) may not account for all possible input formats, particularly historical ones. The attacker exploits the implicit trust ASP.NET places in URL path components to inject malicious session identifiers that get propagated into DOM-relevant attributes.

## Defensive takeaways
- Implement strict input validation on all URL path components, including session identifiers, before using them in resource resolution
- Sanitize or reject URLs containing cookieless session identifier patterns if the application doesn't explicitly require them
- Consider disabling cookieless session support entirely if not needed, and properly validate any URLs that contain these patterns
- Use Content Security Policy (CSP) headers to restrict script loading to trusted domains only
- Apply output encoding to all resolved URLs before inserting them into HTML attributes
- Conduct security reviews of legacy feature interactions, particularly how modern path resolution handles historical session management mechanisms
- Use subresource integrity (SRI) for external script resources to detect tampering

## Variant hunting
['Test other ASP.NET path resolution methods (ResolveClientUrl, etc.) for similar vulnerabilities', 'Investigate whether other URL formats like (S(sessionid)), (F(formauth)), or custom tokens bypass similar protections', 'Check if the vulnerability affects other resource types beyond scripts (stylesheets, images, iframes)', 'Examine whether querystring-based session identifiers can be similarly injected', 'Test if path traversal sequences can be combined with session identifiers to escape the app root', 'Evaluate whether this affects IIS URL rewriting rules or other path manipulation mechanisms', 'Assess impact on applications using URL-based authentication tokens or session management']

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability was recognized as one of the Top 10 web hacking techniques of 2019. The core issue is that ASP.NET's backward compatibility with cookieless sessions creates an implicit trust in path components that should be treated as user-controlled input. The vulnerability demonstrates how convenience features in frameworks can create security gaps when they don't account for all possible input formats. The attack is particularly insidious because it affects the app-root-relative path resolution feature, which developers use specifically to improve security and maintainability. Organizations should audit their ASP.NET applications for this pattern, particularly those using ResolveUrl in resource includes without output encoding.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
