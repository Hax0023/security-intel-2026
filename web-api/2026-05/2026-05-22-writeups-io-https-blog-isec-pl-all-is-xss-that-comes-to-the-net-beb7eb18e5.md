# ASP.NET ResolveUrl XSS via Cookieless Session Path Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** General ASP.NET Applications
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, which resolves app-root-relative URLs using the tilde (~) notation, can be exploited to inject arbitrary paths when cookieless session identifiers are inserted into URLs. An attacker can craft URLs containing cookieless session markers (A(), S(), F()) that get incorporated into resolved resource paths, allowing injection of malicious script sources or other arbitrary URIs.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl with tilde notation for resource loading (e.g., <script src="<%= ResolveUrl("~/Script.js") %>"></script>)
2. Attacker crafts a malicious URL containing cookieless session identifier syntax, such as http://target.com/(A(MALICIOUS))/page.aspx or http://target.com/path/(S(PAYLOAD))/page.aspx
3. When the victim accesses this crafted URL, ASP.NET processes the cookieless identifier and adds it to the resolved path
4. The ResolveUrl method outputs the injected path, resulting in <script src="/(A(MALICIOUS))/Script.js"></script>
5. The browser attempts to load the script from the attacker-controlled path, which can point to malicious content or external resources
6. Attacker achieves XSS execution in the victim's browser context, potentially stealing session tokens or performing actions on behalf of the user

## Root cause
ResolveUrl does not sanitize or validate cookieless session identifiers before incorporating them into resolved paths. ASP.NET's backward compatibility with cookieless sessions causes it to preserve and embed these identifiers in URLs even when cookieless sessions are disabled, and the resolution logic treats them as legitimate path components.

## Attacker mindset
An attacker recognizes that framework conveniences designed for developer ease-of-use can introduce security blind spots when legacy features interact with modern functionality. By understanding ASP.NET's historical cookieless session mechanism and how it coexists with contemporary path resolution, the attacker exploits the implicit trust developers place in framework utilities to safely handle URLs.

## Defensive takeaways
- Validate and sanitize all user-controlled input before using it in URL contexts, even when passed through framework utility methods
- Explicitly disable cookieless sessions in web.config (set cookieless="UseCookies") and reject requests containing cookieless session markers
- Implement Content Security Policy (CSP) headers to restrict script sources and mitigate XSS impact
- Use absolute URL validation or allowlisting for dynamically resolved resources rather than relying solely on framework path resolution
- Apply output encoding/escaping to all dynamically generated src attributes and URLs
- Treat ResolveUrl and similar path resolution methods as unsafe for user-influenced input without additional validation
- Regularly audit resource inclusion patterns and test with malicious URL path components

## Variant hunting
['Test other ASP.NET URL resolution methods (ResolveClientUrl, Page.ClientScript.GetWebResourceUrl) for similar injection vectors', 'Explore injection through URL rewriting modules that might preserve or process cookieless identifiers differently', 'Investigate whether other resource types (stylesheets, images, iframes) can be exploited via similar path injection', 'Test cookieless session identifiers in different URL positions (subdomains, query parameters, fragments) for bypass opportunities', 'Check for variations with Forms Authentication Tickets (F()) and Anonymous Identification (A()) markers in other ASP.NET features', 'Examine MVC/Web API implementations and custom routing handlers for similar path resolution vulnerabilities']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing

## Notes
This vulnerability was selected as one of the Top 10 web hacking techniques of 2019. The bug demonstrates how legacy features (cookieless sessions from ASP.NET v1.0-v1.1) can create security implications when interacting with modern APIs and developer conveniences. The attack is particularly insidious because developers trust framework utilities to handle URL safety correctly. The vulnerability affects any ASP.NET application using ResolveUrl with tilde notation for resource inclusion, regardless of whether cookieless sessions are explicitly enabled. The researcher demonstrated this on .NET applications generally, suggesting broad applicability across ASP.NET versions.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
