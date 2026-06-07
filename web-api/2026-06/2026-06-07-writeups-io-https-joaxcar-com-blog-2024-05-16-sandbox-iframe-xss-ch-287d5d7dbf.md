# Sandbox-iframe XSS Challenge Solution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Personal CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** Not specified (CTF challenge)
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
An XSS challenge combining sandboxed iframes, CSP restrictions, and open redirects demonstrates how CSP path-based restrictions can be bypassed through HTTP redirects followed by loading gadget scripts from CDNs. The vulnerability allows arbitrary code execution inside a sandboxed iframe and potential access to parent window data through srcdoc inheritance mechanisms.

## Attack scenario (step by step)
1. Attacker crafts a Base64-encoded HTML payload containing a script that triggers an open redirect to a CDN (e.g., htmx.min.js)
2. Payload is submitted via the 'xss' parameter, which is decoded and inserted into an iframe with srcdoc attribute
3. The iframe inherits parent page's CSP policy; while 'script-src' restricts to 'self', the redirect exception allows loading from cdnjs.cloudflare.com
4. After redirect, browser only validates base domain against CSP, permitting any script from the CDN to load
5. Loaded gadget script (HTMX or Angular) executes attacker code within iframe context
6. Attacker leverages srcdoc inheritance or fetch('') behavior to access parent window data including the flag in URL hash

## Root cause
CSP specification intentionally permits redirects to bypass path-based source restrictions to prevent side-channel leaks; however this design choice enables attackers to chain open redirects with gadget scripts for XSS. Additionally, srcdoc-based iframes inherit parent CSP and enable cross-origin communication through certain mechanisms.

## Attacker mindset
An attacker recognizes that CSP is not foolproof and that standards-compliant behavior (redirect handling) can be weaponized. They identify gadget scripts available on allowed CDNs and chain multiple weaknesses: open redirect + CSP bypass + sandbox iframe policy misunderstanding + srcdoc inheritance behavior.

## Defensive takeaways
- Avoid allowing 'self' in script-src if the application hosts open redirects; restrict redirects or use stricter CSP directives
- Do not rely solely on sandboxed iframes for isolation when parent and child documents share origins or inheritance
- Be cautious with srcdoc-based iframes as they inherit parent CSP policies; consider frame-src and sandbox restrictions in combination
- Implement proper URL sanitization and validation on redirect endpoints to prevent redirecting to arbitrary external URLs
- Use 'unsafe-eval' sparingly in CSP; it enables gadget-based XSS through loaded libraries like Angular or HTMX
- Monitor for gadget scripts on trusted CDNs that could be exploited for XSS (Angular, HTMX, etc.)
- Consider using Trusted Types API to prevent DOM-based XSS and restrict script evaluation

## Variant hunting
Search for applications using: (1) Open redirects combined with CSP restrictions; (2) Sandboxed iframes with srcdoc attribute loading user-controlled HTML; (3) CSP policies allowing CDNs with path restrictions but not validating post-redirect paths; (4) Gadget scripts (Angular, HTMX, jQuery) on whitelisted domains; (5) Fetch('') or similar implicit requests from srcdoc contexts that may leak parent window data

## MITRE ATT&CK
- T1190
- T1200
- T1021
- T1048

## Notes
This writeup documents a sophisticated multi-stage attack chain that exploits a standards-compliant CSP feature (redirect handling) as documented in W3C CSP3 specification. The challenge demonstrates that security boundaries (CSP + sandbox) can be layered incorrectly. The use of 'srcdoc' instead of 'src' for iframe loading introduces inheritance semantics that reduce isolation. The redirect-to-gadget technique is reusable across many applications and is particularly dangerous when gadget scripts are hosted on trusted CDNs. Key insight: 'allow-scripts' in sandbox with CSP 'unsafe-eval' is a critical combination.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
