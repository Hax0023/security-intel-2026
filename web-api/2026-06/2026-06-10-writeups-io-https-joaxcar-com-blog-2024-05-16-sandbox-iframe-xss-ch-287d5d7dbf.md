# Sandbox-iframe XSS Challenge Solution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Self-hosted CTF challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** N/A (Educational CTF)
- **Severity:** high
- **Vuln types:** Content Security Policy Bypass, Cross-Site Scripting (XSS), Open Redirect, Sandbox Escape
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandboxed iframe XSS challenge exploiting CSP redirect behavior to bypass script-src restrictions, then leveraging iframe srcdoc behavior to access parent window data. The vulnerability chain combines Base64 HTML injection, CSP path-based redirect loopholes, and sandbox iframe origin tricks to extract the flag from the URL hash.

## Attack scenario (step by step)
1. Attacker crafts Base64-encoded HTML payload containing script tags
2. Payload is injected into xss parameter and decoded into sandboxed iframe via srcdoc
3. Attacker uses open redirect endpoint (/redirect) to bypass CSP script-src 'self' restriction
4. Redirect points to CDN (cdnjs.cloudflare.com) where CSP only validates base domain post-redirect
5. HTMX or Angular gadget library is loaded, enabling JavaScript execution within iframe context
6. JavaScript executes with about:srcdoc origin, allowing fetch('') calls to parent context and flag extraction via alert()

## Root cause
Three compounding design/implementation issues: (1) CSP specification allows base domain matching after redirects for side-channel prevention, (2) iframe srcdoc inheritance of parent CSP combined with 'self' open redirect, (3) About:srcdoc origin treatment enabling fetch calls to parent URL fragments

## Attacker mindset
Exploit the subtle distinction between CSP path-based restrictions and post-redirect behavior; understand that CSP's redirect allowance is intentional but can be weaponized; leverage CDN libraries as execution gadgets; abuse iframe srcdoc origin semantics to access parent context

## Defensive takeaways
- Avoid 'self' in script-src when open redirects exist; use nonce/hash-based CSP instead of allowlists
- Be aware that CSP path restrictions are relaxed post-redirect by design—restrict base domains if redirects are necessary
- Sandbox iframe with minimal permissions (remove allow-scripts if possible, use allow-same-origin carefully)
- Don't load sensitive data in URL fragments accessible to sandboxed content; use postMessage with targetOrigin validation
- Sanitize and validate Base64-encoded HTML inputs even if CSP is in place
- Use integrity hashes for external CDN dependencies to prevent gadget-based attacks
- Understand that srcdoc iframes inherit parent CSP and can still access parent window via fetch/postMessage under certain conditions

## Variant hunting
['Test other CDN gadgets (jsDelivr, unpkg, jsdelivr) that may have fewer path restrictions', 'Explore alternative bypass methods: DNS rebinding, protocol-relative URLs, unicode normalization in paths', 'Check if form-action or frame-ancestors directives can be bypassed similarly via redirects', 'Investigate whether postMessage filtering can be bypassed by chaining with other vulnerabilities', 'Hunt for similar redirect+CSP combinations in real applications, especially those using srcdoc for dynamic content', "Test CSP bypass with script-src 'unsafe-eval' + redirects to libraries that execute eval()"]

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1197: BITS Jobs
- T1566: Phishing

## Notes
Educational writeup demonstrating sophisticated XSS chaining. Key insight: CSP's intentional redirect behavior (RFC-designed to prevent side-channel leaks) becomes a weapon when combined with open redirects and gadget libraries. The challenge elegantly shows why 'defense in depth' is crucial—CSP alone, sandboxing alone, and input validation alone each failed; all three were needed. The srcdoc inheritance behavior is subtle and often overlooked in threat modeling.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
