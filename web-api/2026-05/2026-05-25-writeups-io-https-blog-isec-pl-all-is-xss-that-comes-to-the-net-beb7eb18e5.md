# ASP.NET ResolveUrl XSS via Cookieless Session Path Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, used for resolving app-root-relative paths with the tilde (~) syntax, fails to sanitize cookieless session identifiers injected into URLs. An attacker can inject arbitrary path segments through crafted URLs containing session tokens, causing ResolveUrl to generate malicious resource paths that load attacker-controlled content. This leads to reflected XSS attacks via manipulation of script src and stylesheet href attributes.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing cookieless session identifier syntax, e.g., http://vulnerable-site.com/(A(MALICIOUS))/page.aspx or http://vulnerable-site.com/page/(A(MALICIOUS))/default.aspx
2. Victim clicks the link or is redirected to it via phishing/social engineering
3. ASP.NET processes the request and ResolveUrl method resolves ~/Script.js path while preserving the injected identifier
4. The rendered HTML includes the attacker-controlled path in resource references, e.g., <script src="/(A(MALICIOUS))/Script.js"></script>
5. Browser parses the malicious src attribute and attempts to load the resource from attacker-controlled location
6. Attacker hosts malicious JavaScript at that path, achieving arbitrary code execution in victim's browser context

## Root cause
ASP.NET's ResolveUrl method does not sanitize or validate cookieless session identifier path segments when resolving tilde-prefixed paths. The framework tolerates these identifiers in URLs even when cookieless sessions are disabled, and propagates them unchanged through the path resolution logic, treating them as legitimate path components.

## Attacker mindset
Exploit framework convenience features that weren't designed with security-by-default principles. Abuse backward compatibility mechanisms (cookieless sessions) that persist in modern deployments for edge cases. Leverage trusted path resolution functions to bypass developer expectations about what constitutes a 'safe' relative path.

## Defensive takeaways
- Validate and sanitize all URL components before passing to path resolution functions, including injected session identifiers
- Implement strict Content Security Policy (CSP) headers to restrict script and stylesheet loading sources
- Use URL encoding/canonicalization before processing path segments
- Disable cookieless sessions explicitly and remove support if not required for legacy browsers
- Apply output encoding when rendering resolved URLs in HTML attributes
- Implement allowlists for valid resource paths rather than relying on framework path resolution alone
- Use SRI (Subresource Integrity) attributes on script and stylesheet tags to prevent unauthorized resource substitution
- Regularly audit framework and library documentation for security implications of convenience features

## Variant hunting
['Test other path-resolving methods in ASP.NET framework (ResolveClientUrl, ResolveServerUrl) for similar vulnerabilities', 'Check for similar behavior in other server-side frameworks with tilde-based path resolution (Java servlets, Ruby on Rails, etc.)', 'Investigate if other URL-embedded identifiers (F(?), (S(?))) can be similarly abused', 'Test interaction with URL rewriting modules and handlers that might double-process paths', 'Check if path segments with encoded characters (%XX) can bypass sanitization', 'Examine whether the vulnerability extends to other resource types: images, iframes, forms, stylesheets', 'Test if combining multiple injected segments creates bypasses: /(A(X))/(A(Y))/path', 'Investigate whether query parameters in injected paths complicate exploitation detection']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Generic
- T1104 - Ingress Tool Transfer
- T1059 - Command and Scripting Interpreter

## Notes
This vulnerability was selected as one of Top 10 web hacking techniques of 2019. The core issue is that ASP.NET's design accommodates legacy features (cookieless sessions from v1.0-1.1 era) that persist in modern versions for backward compatibility, creating an unexpected attack surface. The vulnerability is particularly dangerous because it abuses a security-intended feature (tilde-relative paths) to achieve XSS. Developers using ResolveUrl without additional output encoding or CSP protection are vulnerable. The writeup demonstrates excellent attack methodology by showing how historical design decisions create modern security problems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
