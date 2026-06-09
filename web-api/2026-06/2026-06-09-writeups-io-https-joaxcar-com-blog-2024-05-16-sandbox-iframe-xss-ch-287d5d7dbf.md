# Sandbox iframe XSS Challenge - CSP Redirect Bypass & Parent Window Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Educational CTF Challenge
- **Bounty:** N/A (Educational writeup)
- **Severity:** High
- **Vuln types:** Content Security Policy (CSP) Bypass, Cross-Site Scripting (XSS), Sandbox Escape, Open Redirect Exploitation
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandbox iframe XSS challenge was solved by exploiting CSP redirect behavior to load arbitrary JavaScript libraries from CDNs, then using sandbox inheritance properties to access parent window data. The vulnerability chain combined an open redirect, CSP path-based bypass, and srcdoc iframe inheritance to leak URL fragment data.

## Attack scenario (step by step)
1. Attacker submits base64-encoded HTML payload via 'xss' parameter containing script tag pointing to open redirect
2. Payload is decoded and injected into sandboxed iframe via srcdoc attribute, inheriting parent CSP
3. Script tag loads redirect endpoint (allowed by 'self' CSP directive) which redirects to CDN JavaScript library
4. Browser applies CSP path relaxation post-redirect, loading arbitrary gadget library (HTMX or Angular)
5. Gadget library enables arbitrary code execution within iframe context
6. Executed JavaScript fetches parent window's URL fragment using srcdoc-specific behavior to access sibling context data

## Root cause
CSP specification allows base domain matching after redirects (by design to prevent side-channel leaks), but this enables gadget loading when combined with: (1) open redirect in allowed origin, (2) srcdoc iframe inheritance of parent CSP, (3) sandboxed iframe allowing script execution with allow-scripts flag.

## Attacker mindset
Adversary recognizes CSP as a layered defense and identifies redirect-based bypass as overlooked attack vector. Instead of direct CSP bypass, exploits specification's intentional design choice. Leverages public CDN gadget libraries (HTMX, Angular) as RCE primitives. Understands iframe sandbox semantics and srcdoc behavior to chain sandbox escape with CSP bypass.

## Defensive takeaways
- Restrict redirect endpoints strictly; validate redirect URLs against whitelist rather than relying on CSP
- Use full-path CSP directives for external CDN resources to prevent gadget loading post-redirect
- Implement 'allow-same-origin' carefully; consider whether sandbox truly needs script execution + parent access
- Review CSP path/redirect behavior (W3C spec) during policy design; document intentional design choices
- Monitor and limit dependency on public CDN gadget libraries (Angular, HTMX); consider SRI hashes
- For srcdoc iframes, explicitly evaluate whether CSP inheritance is necessary or if stricter policies should apply
- Test sandbox + CSP combinations in threat models; avoid assuming multiple layers are independent

## Variant hunting
['Test other CDN libraries on same domain for gadget chains beyond Angular/HTMX (Prototype.js, MooTools, jQuery with plugins)', 'Probe for other open redirects or whitelisted redirect domains in CSP', "Check if 'unsafe-eval' directive can be exploited in conjunction with gadget libraries for code generation", 'Investigate fetch("") behavior from srcdoc iframes to other sandboxed contexts or parent window', "Search for other endpoints returning 3xx redirects that would pass 'self' directive", 'Test whether additional sandbox flags (allow-top-navigation, allow-popups) exist that could chain to full parent access', 'Check if base64 encoding/decoding itself presents injection vectors before srcdoc parsing']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (CSP bypass via redirect)
- T1059 - Command and Scripting Interpreter (JavaScript execution in iframe)
- T1083 - File and Directory Discovery (JavaScript gadget library discovery on CDN)
- T1557 - Man-in-the-Middle (potential for CSP-based side channel)
- T1599 - Network Boundary Bridging (sandbox escape to access parent context)

## Notes
This writeup demonstrates that CSP redirects are a documented but underutilized bypass vector. The challenge's inclusion of 'unsafe-eval' was critical for gadget-based RCE. The srcdoc iframe inheritance behavior is subtle—content loaded via srcdoc (not src) inherits parent CSP but has origin about:srcdoc, creating a specific attack surface. The challenge hints at using fetch("") to demonstrate frame context escalation, suggesting XSS-to-parent-data exfiltration via subtle fetch behavior. Practical relevance: organizations using CSP + sandboxed iframes should audit redirect endpoints and CDN dependencies carefully.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
