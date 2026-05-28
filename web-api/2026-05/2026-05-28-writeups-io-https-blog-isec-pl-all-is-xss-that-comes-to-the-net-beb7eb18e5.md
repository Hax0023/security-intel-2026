# ASP.NET ResolveUrl() XSS via Cookieless Session ID Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), URL Path Traversal, Session ID Injection
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl() method, designed to resolve app-root-relative URLs using the tilde (~) notation, can be exploited to inject arbitrary paths when cookieless session identifiers are present in the URL. An attacker can craft URLs containing malicious cookieless session markers (like (A(ABCD))) that get incorporated into resolved resource paths, enabling XSS attacks through script/resource injection.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl() to reference external resources (scripts, stylesheets) with tilde notation
2. Attacker crafts a malicious URL containing cookieless session identifiers with XSS payload, e.g., http://victim.com/(A(PAYLOAD))/page.aspx
3. When a user visits the attacker-controlled link, ASP.NET processes the URL and ResolveUrl() incorporates the cookieless identifier into resource paths
4. The resolved script src becomes something like /(A(PAYLOAD))/Script.js instead of /Script.js
5. If the server returns the injected path in HTML response without sanitization, the browser attempts to load the malicious resource path
6. Depending on server configuration and error handling, this can lead to loading attacker-controlled content or triggering XSS

## Root cause
ASP.NET's ResolveUrl() method does not validate or sanitize cookieless session identifiers that appear in URL paths before incorporating them into resolved resource URLs. The framework treats these path segments as legitimate directory components, allowing attacker-controlled data to flow into href/src attributes without proper escaping.

## Attacker mindset
An attacker recognizes that ASP.NET's convenience feature (automatic path resolution) creates an implicit trust boundary—developers assume ResolveUrl() output is safe. By leveraging the legacy cookieless session feature (still accepted even when disabled), the attacker injects data into a trusted code path that developers believe is sanitized by the framework itself.

## Defensive takeaways
- Always HTML-encode output of ResolveUrl() or any dynamic URL generation before inserting into HTML attributes
- Disable cookieless session support entirely in web.config if not required for legacy browser support
- Validate and reject URLs containing unexpected cookieless session identifiers (A()), (S()), (F()) patterns at application entry points
- Implement Content Security Policy (CSP) headers to restrict script/resource loading origins
- Use framework features for URL generation that provide built-in output encoding
- Perform security code review of all instances using ResolveUrl() with user-influenced paths

## Variant hunting
['Check other ASP.NET path resolution methods (TransferRequest, MapPath, Server.UrlDecode interactions with tilde paths)', 'Test URL rewriting modules to see if they normalize or validate cookieless identifiers', 'Examine custom URL routing implementations that may bypass built-in validation', 'Look for similar vulnerabilities in other frameworks that auto-resolve application-relative paths (Java EL, PHP include paths)', 'Test combinations of cookieless markers with directory traversal sequences (../, encoded characters)', 'Investigate whether the vulnerability extends to other resource types beyond scripts (images, iframes, data URIs)']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1499 - Endpoint Denial of Service
- T1059 - Command and Scripting Interpreter
- T1204 - User Execution

## Notes
This vulnerability was recognized as a Top 10 web hacking technique of 2019. The root cause is a design assumption that built-in framework methods are inherently safe, leading developers to skip output encoding. The attack exploits the intersection of two ASP.NET features: app-root-relative URLs (modern, convenient) and cookieless sessions (legacy, but still accepted). Organizations should audit applications deployed to subdirectories or using alternative deployments, as these scenarios increase reliance on ResolveUrl().

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
