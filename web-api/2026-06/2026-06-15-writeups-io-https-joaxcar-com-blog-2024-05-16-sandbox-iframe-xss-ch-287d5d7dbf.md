# Sandbox-iframe XSS Challenge Solution - CSP Bypass via Redirect and Flag Exfiltration

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Bug Bounty CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** Not specified - CTF Challenge
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Open Redirect, Sandbox Bypass
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
An XSS challenge that combined multiple security mechanisms (sandboxed iframe, CSP restrictions, and Base64 encoding) to protect a URL fragment flag. The solution exploited a CSP design flaw where redirects only validate the base domain, allowing loading of arbitrary scripts from whitelisted CDNs to achieve code execution and flag exfiltration from the sandboxed iframe.

## Attack scenario (step by step)
1. Attacker identifies that the challenge accepts arbitrary HTML through a Base64-encoded XSS parameter loaded into a sandboxed iframe
2. Attacker recognizes CSP allows 'self' in script-src directive and discovers an open redirect endpoint at /redirect
3. Attacker crafts payload leveraging CSP redirect behavior: initial request to /redirect is allowed by 'self', but after redirect browser only validates base domain (https://cdnjs.cloudflare.com)
4. Attacker injects script tag pointing to redirect with arbitrary CDN payload (e.g., HTMX or Angular library): `<script src="/redirect?url=https://cdnjs.cloudflare.com/ajax/libs/htmx/1.9.12/htmx.min.js"></script>`
5. Loaded library enables XSS execution (HTMX event handler or Angular template injection) to execute arbitrary JavaScript within iframe context
6. Attacker uses special about:srcdoc origin behavior to access parent window/flag hash via fetch("") or similar techniques to exfiltrate flag data

## Root cause
CSP specification intentionally allows redirects to loosen path restrictions to prevent information leakage, but this design choice creates a security gap when combined with: (1) open redirect endpoints whitelisted by CSP, (2) CDN-hosted libraries with gadget functions for XSS, (3) srcdoc iframe inheritance of parent CSP, and (4) sandbox attributes allowing script execution with insufficient origin isolation.

## Attacker mindset
Security researcher systematically identifying layered defenses and finding the intersection of multiple security features that create exploitable conditions. Focus on understanding standards specifications (CSP redirect behavior) and recognizing that design choices for one threat model may create different risks in combined scenarios. Opportunistic use of popular libraries (HTMX, Angular) as gadgets for achieving execution.

## Defensive takeaways
- Do not rely solely on sandbox iframes for security isolation when srcdoc inherits parent CSP - inherited CSP can be bypassed
- Implement strict CSP without 'unsafe-eval' and restrict script-src to specific files/integrity hashes rather than broad paths
- Eliminate open redirect vulnerabilities; if redirects are necessary, implement additional validation or do not whitelist the redirect endpoint in CSP
- For sandboxed content, use origins that cannot access parent context (avoid about:srcdoc if parent security context matters)
- Understand CSP redirect behavior and its security implications - document CSP bypass techniques in threat models
- Use SRI (Subresource Integrity) hashes for external scripts to prevent loading arbitrary CDN versions
- Consider disallowing allow-scripts in sandbox attribute if execution is not strictly necessary
- Store sensitive data (flags, tokens) in HTTP-only cookies or secure storage, not in URL fragments accessible to child contexts

## Variant hunting
Similar vulnerabilities could exist in: (1) other sandboxed iframe implementations inheriting parent CSP, (2) applications using srcdoc with user-controlled content, (3) APIs exposing open redirects on whitelisted domains, (4) any CSP configuration with path-based restrictions and redirect endpoints, (5) other JavaScript gadgets on popular CDNs beyond HTMX/Angular (jQuery plugins, MathJax, etc.), (6) Blob URLs or Data URLs that may inherit CSP differently, (7) sandboxed iframes with allow-top-navigation combined with fragment access.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1200 - Hardware Additions
- T1216 - System Script Proxy Execution
- T1059.007 - JavaScript/ECMAScript Execution
- T1567 - Exfiltration Over Web Service

## Notes
This writeup exemplifies advanced XSS exploitation combining multiple security boundaries. Key insight: CSP redirect exemption is a specification feature, not a flaw, but creates risk when combined with open redirects and whitelisted CDNs containing gadgets. The about:srcdoc origin behavior is subtle and often overlooked. Challenge demonstrates importance of threat modeling security feature interactions rather than evaluating controls in isolation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
