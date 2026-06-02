# Sandbox-iframe XSS Challenge Solution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** N/A (Educational CTF)
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Sandbox Attribute Bypass, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A multi-step XSS challenge exploiting CSP redirect handling, CDN gadgets, and iframe sandbox limitations. The vulnerability chain combines an open redirect, CSP path-based bypass via redirects, and use of external library gadgets (HTMX or Angular) to achieve code execution and flag exfiltration from a sandboxed iframe.

## Attack scenario (step by step)
1. Attacker crafts Base64-encoded HTML payload containing a redirect-based script inclusion that bypasses CSP path restrictions
2. Payload is injected via the 'xss' search parameter into the challenge page, which loads it into a sandboxed iframe via srcdoc
3. Script tag references /redirect?url=https://cdnjs.cloudflare.com/ajax/libs/htmx/1.9.12/htmx.min.js to bypass CSP by using allowed redirect followed by CDN domain loading
4. CSP allows the redirect (script-src 'self'), but after redirect, browser only validates base domain https://cdnjs.cloudflare.com per CSP specification
5. HTMX or Angular library loads from CDN and provides XSS gadget (hx-on:error event handler or ng-app template injection)
6. Attacker executes JavaScript in iframe context to access parent window location hash containing the flag and displays it via alert()

## Root cause
Multiple compounding weaknesses: (1) CSP redirect behavior allowing base domain matching after redirect, (2) srcdoc iframe inheriting parent CSP while maintaining script execution, (3) lack of allow-same-origin sandbox attribute offset by fetch() relative URL resolution to parent, (4) availability of XSS gadgets on allowed CDN domains, (5) insufficient isolation between iframe and parent context despite sandbox restrictions.

## Attacker mindset
Methodical layering of bypasses: recognize CSP is present but exploit its redirect specification; identify that sandbox still allows scripts; discover that srcdoc inherits CSP; map available gadgets on trusted CDNs; use fetch('') trick to access parent resources; chain all components to extract sensitive data from URL hash.

## Defensive takeaways
- Implement strict CSP without 'unsafe-eval' and avoid allowing entire CDN domains; use nonce/hash-based allowlists for inline scripts
- Understand CSP redirect behavior (RFC 6454) and its security implications; consider disallowing redirects in script-src or use strict path validation
- When using sandboxed iframes, carefully evaluate necessity of allow-scripts and allow-modals; consider removing allow-same-origin only if communication protocol uses explicit postMessage
- Avoid srcdoc for untrusted content; prefer external iframe src with appropriate origin restrictions
- Audit third-party CDN libraries for available XSS gadgets; consider using Subresource Integrity (SRI) to pin specific versions
- Test iframe sandbox escape vectors including fetch('') relative URL resolution and window.name postMessage techniques
- Validate and sanitize Base64-encoded payloads, not just the decoded content; apply output encoding appropriate to context (HTML, JavaScript, URL)
- Use Security headers like X-Frame-Options and Frame-Ancestors to restrict iframe embedding contexts

## Variant hunting
['Test CSP bypass via other redirect endpoints or open redirects on allowed domains (form-action, frame-src directives)', "Explore fetch('') behavior from sandboxed iframe with allow-same-origin enabled; test window.name and postMessage exfiltration", 'Audit other JavaScript libraries on allowed CDNs (jQuery, Bootstrap, Vue.js) for XSS gadgets beyond Angular/HTMX', 'Attempt breaking out of iframe via javascript: protocol in links or form targets', 'Test if srcdoc CSP inheritance can be bypassed via <meta> tags or <link> rel=stylesheet with event handlers', 'Investigate if SVG or other XML vectors can bypass CSP restrictions in srcdoc context', 'Check for timing-based side channels in CSP violation reporting to leak information', 'Test hash/fragment identifier access patterns; verify if location.hash is truly isolated in null-origin sandbox']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter (JavaScript)
- T1021: Remote Service Session Hijacking (Cross-Origin Access)
- T1040: Network Sniffing (CSP Redirect Leakage)
- T1592: Gather Victim Host Information (CSP Policy Discovery)

## Notes
This writeup is exceptional for documenting a sophisticated security research technique. Key insight: CSP redirect behavior (W3C CSP3 spec feature) is a legitimate design choice but creates a powerful bypass vector when combined with gadget chains. The challenge demonstrates why multi-layered defenses are necessary and how a single misconfiguration (open redirect + full-path CDN dependency) can unravel an entire security posture. The fetch('') technique for accessing parent context from null-origin sandbox is a valuable lesser-known bypass. Relevant for: security training, XSS exploitation, CSP analysis, sandbox escapes, and third-party library risk assessment.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
