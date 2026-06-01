# Sandbox-iframe XSS Challenge: CSP Bypass via Redirect & Flag Exfiltration

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** CTF/Bug Bounty Educational Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** N/A - Educational CTF
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandboxed iframe XSS challenge demonstrated a multi-step exploitation technique combining CSP bypass via redirect chains with sandboxed iframe escape. The vulnerability leveraged an open redirect endpoint to bypass strict CSP restrictions, load arbitrary scripts from CDN, and ultimately exfiltrate URL fragment-based flags despite sandbox restrictions.

## Attack scenario (step by step)
1. Attacker provides Base64-encoded malicious HTML in the 'xss' search parameter
2. HTML is decoded and injected into sandboxed iframe via srcdoc attribute, inheriting parent CSP
3. Attacker bypasses CSP script-src restriction using open redirect endpoint at /redirect?url=<EXTERNAL_CDN_URL>
4. Redirect to CDN allows loading of arbitrary scripts (HTMX or Angular) without explicit CSP allowance
5. Loaded gadget library (HTMX/Angular) enables code execution within iframe context
6. Attacker leverages fetch('') from null-origin iframe to access parent context and exfiltrate URL fragment flag

## Root cause
CSP specification design choice permitting expanded scope matching post-redirect; combined with srcdoc iframe inheriting parent CSP, presence of 'self' in script-src directive, open redirect endpoint, and publicly available JavaScript gadget libraries on whitelisted CDNs.

## Attacker mindset
Security researcher identifying layered defense bypass through understanding CSP specification nuances and redirect behavior. Methodical approach: identify CSP restrictions → find redirect mechanism → leverage CDN gadgets → exploit sandbox quirks. Focus on 'known unknowns' in security specifications rather than novel vulns.

## Defensive takeaways
- Implement CSP path-specific restrictions without relying on redirects from trusted domains; validate final redirect destination
- Avoid 'self' in script-src when combined with open redirects; use strict nonce/hash-based CSP
- Do not use srcdoc for untrusted content; use external src with separate origin and stricter CSP
- Apply consistent and strict CSP to both parent and iframe contexts independently
- Remove unnecessary external dependencies and trim CDN include paths; audit gadget chains on whitelisted domains
- Monitor and alert on unusual fetch/navigation patterns from null-origin frames
- Consider allow-same-origin implications; evaluate if sandbox restrictions are sufficient for threat model

## Variant hunting
['Test other CDN-hosted JavaScript libraries for gadget chains (D3.js, jQuery, Lodash, Moment.js)', 'Probe alternate open redirect patterns and chained redirects', 'Examine other iframe sandbox attribute combinations (allow-popups, allow-top-navigation) for escalation', 'Investigate if srcdoc inherits other CSP directives beyond script-src (style-src, frame-src)', "Test if fetch('') behavior differs in other sandbox configurations or with allow-same-origin", 'Look for CSP report-uri leakage or violations that could indicate presence of flags/sensitive data', 'Explore window.location manipulation from null-origin contexts to access parent URL']

## MITRE ATT&CK
- T1190
- T1059
- T1518
- T1036

## Notes
Educational writeup of deliberate CTF challenge; not a real-world vulnerability disclosure. Highlights importance of understanding security specification corner cases (CSP path+redirect interaction per W3C spec). Demonstrates that 'defense in depth' can have gaps when individual layers (CSP, sandbox, SOP) interact unexpectedly. The challenge elegantly combines three conceptually simple bypasses into a practical escalation chain.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
