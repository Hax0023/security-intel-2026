# ASP.NET ResolveUrl XSS via Path Traversal and Cookieless Session Identifiers

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Unknown
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, combined with cookieless session identifiers, allows attackers to inject arbitrary URI paths into resolved resource URLs. By crafting URLs containing session identifiers like (A(ABCD)) or (S(SESSIONID)), attackers can manipulate the resolved paths of script tags and other resources, leading to XSS attacks.

## Attack scenario (step by step)
1. Attacker identifies a vulnerable ASP.NET application using ResolveUrl for script/resource inclusion (e.g., <script src="<%= ResolveUrl("~/Script.js") %>"></script>)
2. Attacker crafts a malicious URL containing cookieless session identifier syntax: http://target.com/(A(PAYLOAD))/A/B/C/default.aspx
3. When the victim visits the malicious URL, ResolveUrl processes the path and incorporates the identifier into the resolved resource path
4. The rendered HTML contains a modified script source pointing to attacker-controlled location: <script src="/(PAYLOAD)/Script.js"></script>
5. Browser attempts to load the script from the attacker-injected path, executing arbitrary JavaScript in the victim's context
6. Attacker successfully performs session hijacking, credential theft, or malware distribution

## Root cause
ASP.NET's ResolveUrl method blindly processes and preserves cookieless session identifier syntax (e.g., (A(?)), (S(?)), (F(?))) in URLs without validation or filtering. The framework treats these identifiers as legitimate path components rather than special tokens, allowing them to be injected into resolved resource paths when using tilde (~) notation.

## Attacker mindset
Attackers recognized that ASP.NET's convenience feature (app-root-relative URLs via ResolveUrl) combined with legacy cookieless session support created an unintended information disclosure and XSS vector. By understanding how ResolveUrl parses and resolves paths while preserving special identifiers, attackers could manipulate resource loading without needing direct application code modification.

## Defensive takeaways
- Sanitize and validate all user-supplied path components before passing to ResolveUrl or similar URL resolution methods
- Explicitly disable cookieless session features in web.config (set Cookieless='UseCookies') if not required for legacy browser support
- Implement strict URL validation to reject requests containing suspicious patterns like session identifier syntax in unexpected locations
- Use Content Security Policy (CSP) headers to restrict script loading to trusted sources and mitigate XSS impact
- Prefer relative paths with explicit directory traversal logic over framework-dependent path resolution when handling user-influenced paths
- Apply output encoding to all dynamically generated URLs in HTML/JavaScript contexts

## Variant hunting
['Test other ASP.NET URL resolution methods (Control.ResolveUrl, VirtualPathUtility.ToAbsolute, etc.) for similar vulnerabilities', 'Investigate whether other session identifier patterns (F(?), D(?)) can be exploited in similar ways', 'Check if CSS @import statements and other resource inclusion mechanisms are affected', 'Test whether URL-encoded versions of parentheses (%28, %29) bypass existing filters', 'Examine applications using Microsoft Dynamics, SharePoint, or other ASP.NET-based platforms for the same vulnerability', 'Research similar path manipulation issues in other frameworks supporting cookieless sessions or virtual path resolution']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1598 - Phishing - Spearphishing Link
- T1566 - Phishing - Phishing - Email
- T1005 - Data from Local System

## Notes
This vulnerability was selected as one of the Top 10 web hacking techniques of 2019. The issue highlights how legacy features designed for older browser compatibility can create new attack surfaces when combined with modern convenience features. The vulnerability requires user interaction (visiting a crafted URL) but is trivial to exploit and can be delivered via phishing. The root cause stems from ASP.NET treating session identifiers as path components rather than metadata that should be stripped before path resolution.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
