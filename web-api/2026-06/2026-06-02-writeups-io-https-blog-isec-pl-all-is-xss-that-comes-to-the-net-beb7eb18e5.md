# ASP.NET ResolveUrl XSS via Cookieless Session ID Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Not specified
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), URL Manipulation, Path Traversal
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, when handling app-root-relative paths with the tilde (~) notation, inadvertently includes cookieless session identifiers from the URL path into resolved resource URLs. An attacker can inject arbitrary cookieless session tokens (formatted as (A(payload)), (S(payload)), or (F(payload))) to manipulate script sources and achieve XSS.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl to load resources like JavaScript from app-root-relative paths (e.g., ~/Script.js)
2. Attacker crafts a malicious URL containing a cookieless session identifier with XSS payload: http://target.com/(A(xss_payload))/page.aspx
3. When the page at /A/B/C/default.aspx loads with ResolveUrl, the session identifier is incorporated into the resource path
4. The resolved script src becomes <script src="/(A(xss_payload))/Script.js"></script>
5. Browser attempts to fetch the malicious path, which may execute injected JavaScript or load attacker-controlled resources
6. Session data may be inadvertently created or modified due to cookieless session handling

## Root cause
ASP.NET's ResolveUrl method processes cookieless session identifiers embedded in the request URI path without sanitization. The method treats these identifiers as legitimate path components and includes them in the resolved URLs, even when cookieless sessions are disabled. This design flaw combines legacy cookieless session support with modern URL resolution without proper validation.

## Attacker mindset
An attacker exploits the framework's backward compatibility feature (cookieless sessions) that remains active even when disabled. By understanding how ResolveUrl processes paths and how ASP.NET interprets special URI segments, the attacker leverages framework internals to inject content into resource URLs. The attack is particularly attractive because it doesn't require application-level input validation bypasses—it exploits framework behavior itself.

## Defensive takeaways
- Validate and sanitize all user-controlled URL components before using them in path resolution
- Disable cookieless sessions entirely in web.config if not required, and monitor for requests containing cookieless identifiers
- Implement Content Security Policy (CSP) headers to restrict script sources and prevent inline script execution
- Use absolute resource paths with domain-specific URLs instead of app-root-relative paths when security is critical
- Regularly update ASP.NET framework to patches addressing ResolveUrl vulnerabilities
- Implement output encoding for all dynamically generated HTML attributes, particularly src attributes
- Review and test applications for XSS vulnerabilities through unusual URL path encoding and special ASP.NET identifiers

## Variant hunting
Search for other ASP.NET methods that process or resolve paths without sanitizing cookieless session identifiers. Investigate similar vulnerabilities in other server-side frameworks with legacy session management features. Test other server controls that generate HTML with ResolveUrl (image tags, link elements, form actions). Examine applications using other URI-based state management mechanisms (authentication tickets, anonymous identifiers) combined with dynamic resource loading.

## MITRE ATT&CK
- T1190
- T1598

## Notes
This vulnerability was selected as one of Top 10 web hacking techniques of 2019. The attack exploits a gap between ASP.NET's legacy cookieless session feature and modern URL handling. The vulnerability is particularly insidious because ResolveUrl is a security-conscious feature designed to handle relative paths safely, yet it becomes a vector for attack when combined with cookieless session handling. Applications using ResolveUrl in resource inclusion statements (script src, link href, img src) are most vulnerable.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
