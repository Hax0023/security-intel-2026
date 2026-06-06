# ASP.NET ResolveUrl Path Traversal and XSS via Cookieless Session Identifiers

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** ASP.NET Framework
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Path Traversal, URL Manipulation, Authentication Bypass
- **Category:** web-api
- **Writeup:** https://blog.isec.pl/all-is-xss-that-comes-to-the-net/

## Summary
ASP.NET's ResolveUrl method, designed to convert app-root-relative paths using tilde (~) notation, can be exploited by injecting cookieless session identifiers into URLs to manipulate resolved paths. An attacker can craft URLs containing malicious path segments in the session identifier format (e.g., (A(ABCD))) that ResolveUrl will incorporate into resolved resources, allowing arbitrary URI paths to be loaded and executed as trusted application resources.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using ResolveUrl for dynamic resource loading (CSS, JavaScript)
2. Attacker crafts a malicious URL with cookieless session identifier syntax: http://target.com/(A(malicious_payload))/path/to/page.aspx
3. When the victim visits the crafted URL, ResolveUrl processes the session identifier as part of path resolution
4. The resolved resource path now contains attacker-controlled content: /(A(malicious_payload))/resource.js
5. Browser requests the manipulated resource path from attacker-controlled domain or server
6. Attacker's malicious JavaScript executes in the context of the victim's session, leading to credential theft or session hijacking

## Root cause
ResolveUrl method does not properly validate or sanitize URL paths before resolution. It treats cookieless session identifiers (formatted as (S(?)), (A(?)), (F(?))) as legitimate path components even when cookieless sessions are disabled. ASP.NET's design accepts these identifiers in URLs without validation, allowing them to be embedded in resolved resource paths. The framework assumes these identifiers only appear in legitimate cookieless session scenarios but does not restrict their presence when cookies are enforced.

## Attacker mindset
An attacker recognizes that developers rely on framework features for security and convenience without understanding underlying mechanics. By exploiting the gap between cookieless session identifier format and actual enforcement policies, the attacker can inject arbitrary path components into resolved URLs. The attacker realizes that many developers trust ResolveUrl output implicitly and may not validate resolved paths, making this a reliable vector for injecting malicious resources.

## Defensive takeaways
- Implement URL validation and sanitization on ResolveUrl output before using it in HTML contexts, especially for resource URLs
- Validate that resolved paths match expected patterns and do not contain unexpected identifiers or special characters
- Use Content Security Policy (CSP) headers to restrict resource loading to trusted domains only
- Explicitly disable cookieless sessions and validate that no cookieless identifiers appear in production URLs
- Implement server-side checks to reject requests containing suspicious session identifier patterns when cookieless mode is disabled
- Use integrity checks (SRI - Subresource Integrity) for external resource loading to prevent unauthorized script execution
- Regularly audit framework version security advisories and apply patches promptly
- Encode or escape tilde (~) and other special characters in user-supplied URL components before path resolution

## Variant hunting
['Test other ASP.NET methods that perform URL resolution (e.g., Control.ResolveClientUrl, Page.ResolveUrl) for similar vulnerabilities', 'Examine applications using URL rewriting modules that may interact unpredictably with session identifiers', 'Investigate applications mixing cookieless and cookie-based session management across different application modules', 'Search for applications using ResolveUrl in AJAX endpoints or API responses where XSS impact amplifies', 'Test applications with custom authentication schemes that may use URL-encoded session data in similar formats', 'Analyze mobile application frameworks in .NET ecosystem (e.g., ASP.NET Mobile) for analogous path resolution flaws', 'Test whether other programming frameworks (.NET Framework, .NET Core) handle cookieless identifiers differently', 'Investigate reverse proxy and load balancer configurations that may strip or modify session identifiers', 'Examine WebForms vs MVC implementations for differential behavior in ResolveUrl handling']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol
- T1098 - Valid Accounts
- T1056 - Input Capture
- T1040 - Traffic Sniffing
- T1021 - Remote Services
- T1566 - Phishing
- T1598 - Phishing for Information

## Notes
This vulnerability was recognized as one of Top 10 web hacking techniques of 2019. The bug highlights the danger of implicit trust in framework features without understanding their underlying implementation. ResolveUrl's behavior with cookieless identifiers reveals a design inconsistency where the framework continues to parse and inject these identifiers even when the feature is disabled. The vulnerability is particularly dangerous because it affects resource loading, which developers typically assume is safe when handled by the framework. Exploitation requires social engineering to deliver malicious URLs but does not require previous authentication or complex attack infrastructure. The technique demonstrates how legacy features (cookieless sessions from ASP.NET v1.0) can create modern security vulnerabilities when modern configurations are applied to code that still processes these legacy formats.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
