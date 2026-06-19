# ASP.NET ResolveUrl App-Root-Relative Path Traversal Leading to XSS

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method for app-root-relative URLs (~) can be exploited through cookieless session identifiers embedded in URL paths. An attacker can inject malicious identifiers (A/S/F parameters) that are preserved during path resolution, allowing arbitrary script injection and XSS attacks.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl for resource loading with tilde notation (~/script.js)
2. Attacker crafts a malicious URL containing cookieless session identifiers: http://target.com/(A(MALICIOUS))/path/page.aspx
3. When the target visits or is redirected to this URL, ASP.NET processes the request and preserves the identifier
4. ResolveUrl resolves ~/Script.js to /(A(MALICIOUS))/Script.js in the HTML output
5. Browser interprets the src attribute, attempting to load the attacker-controlled path
6. Attacker serves malicious JavaScript from a path matching the injected identifier, achieving XSS execution

## Root cause
ASP.NET's ResolveUrl method blindly resolves tilde paths without properly sanitizing or separating cookieless session identifiers from the actual path components. The framework preserves these identifiers during path resolution, allowing them to be injected into resource URLs where they can manipulate script source paths.

## Attacker mindset
Exploit framework convenience features that weren't designed with attack paths in mind. Leverage legacy features (cookieless sessions) that are still supported for backward compatibility but create new attack surface when combined with modern conveniences (ResolveUrl). The attacker recognizes that developers use these features without understanding the security implications of identifier injection.

## Defensive takeaways
- Validate and sanitize all URL components separately, especially session identifiers and path data
- Disable cookieless session support entirely if not required; avoid AutoDetect mode
- Implement strict Content Security Policy (CSP) headers to restrict script source origins
- Use absolute URLs or server-side URL generation that prevents path injection
- Sanitize user-controlled input in URLs before passing to URL resolution functions
- Implement URL encoding/validation for all dynamic resource references
- Consider using modern authentication mechanisms instead of URL-based session identifiers

## Variant hunting
['Test other ASP.NET URL resolution methods (ResolveClientUrl, etc.) for similar issues', 'Examine cookie-based session handling combined with reflected XSS in cookie values', 'Investigate other framework versions and their handling of special URL parameters', 'Test if Form Authentication (F()) identifiers are similarly injectable', 'Analyze custom URL routing implementations that might have similar flaws', 'Check for DOM-based XSS in JavaScript that processes current page URLs', 'Test application behavior with non-standard cookieless identifier formatting']

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability was recognized as one of Top 10 web hacking techniques of 2019. The issue is particularly insidious because it combines two legitimate ASP.NET features in an unexpected way. The vulnerability affects applications that: (1) use ResolveUrl with tilde notation, (2) may receive requests with cookieless session identifiers (even if not using cookieless sessions), and (3) don't properly validate URL structure. This represents a classic case of feature interaction creating security issues not apparent when features are considered individually.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
