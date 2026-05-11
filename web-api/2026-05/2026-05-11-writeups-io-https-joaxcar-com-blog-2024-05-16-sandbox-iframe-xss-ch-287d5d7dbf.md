# Sandbox-iframe XSS Challenge Solution

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Custom CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** Educational/CTF - No monetary bounty mentioned
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A multi-stage XSS vulnerability combining CSP bypass via open redirect, JavaScript gadget loading from CDN, and sandbox iframe escape through srcdoc inheritance. The challenge demonstrates how CSP redirects are only validated against base domain post-redirect, allowing loading of arbitrary scripts from whitelisted CDNs, combined with sandboxed iframe's inherited CSP to access parent window flag.

## Attack scenario (step by step)
1. Attacker crafts Base64-encoded HTML payload containing script redirect to open redirect endpoint
2. Payload is submitted via xss parameter and inserted into sandboxed iframe via srcdoc attribute
3. CSP validation occurs on initial script request; open redirect endpoint is allowed by 'self' directive
4. Browser follows redirect to cdnjs.cloudflare.com; post-redirect CSP only validates base domain not path
5. Arbitrary JavaScript gadget (HTMX or Angular) is loaded and executed within iframe context
6. Script uses srcdoc inheritance properties and fetch behavior to access parent window's URL hash containing flag, then displays via alert

## Root cause
Multiple compounding design/implementation issues: (1) CSP specification allows post-redirect base-domain-only validation, (2) srcdoc iframe inherits parent CSP instead of using null origin restrictions, (3) presence of open redirect endpoint combined with overly broad CDN whitelist, (4) no HTML sanitization on base64-decoded payload, (5) JavaScript gadgets (HTMX, Angular) available on whitelisted CDN can be weaponized

## Attacker mindset
Security researcher demonstrating sophisticated understanding of CSP specification edge cases, redirect bypass techniques, and iframe sandbox behavior. Focus on finding overlooked but documented features (CSP redirect handling) rather than zero-days. Leveraged publicly available libraries as execution gadgets, showing how legitimate dependencies become attack vectors.

## Defensive takeaways
- Implement path-level CSP restrictions and validate post-redirect URLs against full path, not just base domain
- Use 'sandbox' without 'allow-scripts' for truly untrusted content; if scripts needed, use more granular isolation
- Never apply srcdoc to sandboxed iframes expecting origin null behavior; use external src= with proper origin isolation
- Whitelist specific script versions/hashes rather than entire CDN domains; use Subresource Integrity (SRI) hashes
- Sanitize HTML content even when base64-encoded; encoding is not sanitization
- Review CSP redirect behavior at https://www.w3.org/TR/CSP3/#source-list-paths-and-redirects and apply strict controls
- Monitor and restrict open redirects; treat as security boundary, not convenience feature
- Consider using frame-ancestors CSP directive to prevent iframe embedding of sensitive content

## Variant hunting
['Test other whitelisted CDNs for available gadget libraries (jQuery, prototype.js, dojo.js, etc.)', 'Investigate if other CSP directives (form-action, frame-src) can be bypassed via same redirect technique', 'Check if srcdoc behavior differs across browsers in CSP inheritance and same-origin policy', 'Look for other open redirects on same origin that could be chained for bypass', "Test fetch('') behavior variations and other implicit requests that may leak parent origin information", 'Examine hash/fragment handling across different iframe creation methods (srcdoc vs src vs contentDocument)', 'Try alternate encoding schemes or multi-stage payloads to bypass base64 sanitization checks']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1566.002 - Phishing: Spearphishing Link
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1083 - File and Directory Discovery
- T1185 - Browser Information Discovery

## Notes
This is a well-designed educational CTF challenge that teaches critical real-world security concepts often missed by developers. The writeup demonstrates deep knowledge of CSP specification details (RFC 7230 redirect handling), iframe sandbox behavior differences, and JavaScript gadget exploitation. The challenge elegantly combines multiple vulnerabilities that individually might be considered acceptable (open redirect on internal endpoint, sandbox without same-origin, public CDN whitelist) but together enable complete compromise. The mention of 'fetch("")' behavior suggests leveraging implicit request mechanics to extract information across sandbox boundaries - a sophisticated exploitation technique. This represents advanced application-level security research relevant to bug bounty hunters targeting modern JavaScript applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
