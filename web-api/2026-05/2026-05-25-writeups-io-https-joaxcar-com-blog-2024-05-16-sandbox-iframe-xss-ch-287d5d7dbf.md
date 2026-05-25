# Sandbox-iframe XSS Challenge Solution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** Educational/CTF
- **Severity:** high
- **Vuln types:** Content Security Policy Bypass, Cross-Site Scripting (XSS), Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandboxed iframe XSS challenge demonstrating CSP bypass through exploiting redirect behavior and CSP path matching rules. Attackers can load arbitrary scripts from CDNs after a redirect, bypassing strict script-src CSP directives that restrict to specific paths. Combined with sandbox escape techniques, this allows arbitrary code execution and access to parent frame data.

## Attack scenario (step by step)
1. Attacker base64-encodes malicious HTML payload containing a script tag pointing to an open redirect endpoint
2. Payload is submitted via the 'xss' parameter, injected into srcdoc of sandboxed iframe
3. Script tag references open redirect with target CDN URL (e.g., /redirect?url=https://cdnjs.cloudflare.com/...)
4. Browser loads redirect from 'self' origin (allowed by CSP), then follows redirect to CDN
5. After redirect, CSP only validates base domain (cdnjs.cloudflare.com), allowing arbitrary path loading
6. Gadget scripts like HTMX or Angular are loaded, providing execution context to access parent window and steal hash flag

## Root cause
CSP specification deliberately allows redirects to relax path-based restrictions to prevent side-channel leakage, but this creates a security gap when combined with: (1) overly permissive CSP directives with full paths, (2) open redirects, and (3) gadget libraries on allowed domains. The sandboxed iframe's srcdoc inheritance of parent CSP, combined with null origin origin restrictions being bypassable through certain fetch/navigation techniques, allows context escalation.

## Attacker mindset
Security researcher identifying CSP as a key attack surface, recognizing the deliberate but exploitable redirect behavior in CSP specifications. Leveraging publicly available gadget libraries and well-known JavaScript frameworks as execution primitives. Methodically chaining multiple security boundaries (CSP, sandbox, origin restrictions) to achieve full context escape.

## Defensive takeaways
- Avoid overly specific CSP paths when using 'self' - use domain-level allowlists instead
- Eliminate open redirects entirely; validate redirect targets against strict whitelists
- Add 'strict-dynamic' to script-src to prevent gadget library loading via 'self'
- Use nonces/hashes exclusively rather than 'unsafe-eval' and 'self' together
- Consider sandbox attribute values carefully - remove 'allow-scripts' if possible; prefer 'allow-same-origin' removal
- Monitor and restrict gadget libraries on CDNs; keep dependencies updated to remove known XSS gadgets
- Implement subresource integrity (SRI) for all external script loads
- Treat URL fragments/hashes as sensitive - avoid storing secrets there accessible to iframes
- Test CSP bypass vectors during security review, including redirect chains

## Variant hunting
Similar bypass patterns exist in: (1) other redirect endpoints on same domain accepting CSP-allowed origins, (2) alternative gadget libraries on CDNs (Angular, jQuery, Lodash, etc.), (3) service worker registration for scope escalation, (4) form-action/frame-src directives exploitable via same redirect technique, (5) X-Frame-Options bypass combinations, (6) postMessage-based parent access in different sandbox configurations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1559.001 - Inter-Process Communication: Component Object Model
- T1566.002 - Phishing: Spearphishing Link
- T1538 - Steal Web Session Cookie

## Notes
This writeup excellently documents a real-world security chaining scenario. The CSP redirect behavior is specified and intentional but creates exploitable gaps when combined with weak sanitization and gadget availability. The challenge demonstrates why security layers must be designed holistically - sandbox isolation alone fails when CSP is bypassable. Key learning: CSP path-based restrictions are fundamentally weak against redirect chains; always prefer allowlist-based domain restrictions and strict-dynamic for dynamic code.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
