# Sandbox-iframe XSS Challenge Solution: CSP Bypass via Redirect + Flag Exfiltration

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** N/A (CTF Challenge)
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Sandbox Escape, Open Redirect Abuse
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandboxed iframe XSS challenge demonstrated CSP bypass through redirect-based script loading combined with gadget libraries (HTMX/Angular). The vulnerability chain exploits CSP's documented design choice to allow redirects to bypass path-based script-src restrictions, enabling arbitrary JavaScript execution within the iframe and subsequent flag exfiltration from the parent document's hash fragment.

## Attack scenario (step by step)
1. Attacker encodes malicious HTML payload in Base64 and submits via 'xss' parameter
2. Challenge application loads HTML into sandboxed iframe via srcdoc attribute, inheriting parent CSP
3. Attacker crafts script tag leveraging the open redirect endpoint: <script src="/redirect?url=https://cdnjs.cloudflare.com/ajax/libs/htmx/1.9.12/htmx.min.js"></script>
4. Browser fetches from /redirect (allowed by script-src 'self'), receives redirect to CDN; post-redirect, browser only validates base domain against CSP
5. Gadget library (HTMX or Angular) executes, enabling arbitrary code execution (e.g., hx-on:error or ng-app templates)
6. Executed JavaScript performs fetch("") or similar technique to access parent frame's location hash containing flag and displays via alert()

## Root cause
CSP specification (W3C CSP3) deliberately permits redirects from whitelisted domains to bypass path-based restrictions to prevent side-channel information leakage. Combined with: (1) unsanitized Base64 input, (2) presence of gadget libraries on allowed CDN, (3) open redirect endpoint, and (4) iframe inheriting parent CSP despite sandbox attribute, this creates an exploitable chain.

## Attacker mindset
Sophisticated understanding of CSP mechanics and legitimate design choices that can be weaponized. Recognizes that path-restrictive CSP rules are often introduced with false confidence and searches for redirect endpoints. Leverages existing public gadget libraries rather than crafting novel payloads. Methodically chains multiple weak controls (CSP + sandbox) to achieve full compromise.

## Defensive takeaways
- Avoid path-based script-src restrictions without understanding CSP redirect behavior; consider nonce-based or hash-based directives instead
- Never expose open redirect endpoints, especially on the same origin as security-sensitive content
- Be cautious of including gadget libraries (Angular, htmx, jQuery) with CSP bypass potential on the same CDN
- When sandboxing iframe content, prefer srcdoc with strict CSP over src with external resources; recognize srcdoc inheritance of parent CSP
- Implement explicit allow-same-origin only when necessary; validate that sandbox attribute isolation is not assumed sufficient protection
- Store sensitive data (flags, secrets) outside URL fragments; use secure session-based mechanisms instead
- For CSP, prefer strict allow-lists without full domain entries; use nonce/hash for inline scripts and avoid 'unsafe-eval'
- Monitor and audit third-party CDN libraries for XSS gadget potential; consider hosting local copies with integrity checks

## Variant hunting
['Test other redirect patterns (302, 301, 307, 308) to confirm all honor CSP post-redirect behavior', 'Investigate alternative gadget libraries on allowed CDNs (Prototype, Dojo, Ember, Vue) for similar bypass vectors', 'Probe whether other iframe loading mechanisms (about:blank with innerHTML, data: URIs) bypass CSP differently', 'Examine fetch("") and related techniques for leaking parent window context without same-origin', 'Search for other open redirect endpoints or redirect-like behaviors (meta refresh, location assignment)', 'Test CSP path restrictions on other directives (frame-src, form-action, default-src) for similar bypass potential', 'Attempt to chain with other sandbox bypasses (plugin-types, allow-popups combined with window.open leaks)', 'Fuzz CDN paths to discover accidentally exposed debug/unminified versions with additional gadgets']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1567: Exfiltration Over Web Service
- T1200: Traffic Signaling
- T1104: Protocol Tunneling

## Notes
This writeup exemplifies a real-world complex vulnerability requiring knowledge of specs (CSP3) often overlooked in practice. The author intentionally hinted at the bypass via unnecessary full-path dependency and open redirect, making it a well-designed CTF challenge. The vulnerability is not a flaw in CSP per se but demonstrates how multiple weak controls (isolation + CSP + gadget availability) compound. The fetch("") technique mentioned (incomplete in source) likely leverages about:srcdoc origin handling to leak parent context. Key insight: security mechanisms designed with one threat model (side-channel leakage via CSP path probing) can be exploited when combined with other factors (redirects, gadgets, iframe sandbox). Practical for real applications using CDN libraries and redirect endpoints.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
