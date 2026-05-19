# Sandbox iFrame XSS Challenge Solution - CSP Bypass & Fragment Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Personal CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** None - Educational CTF Challenge
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A multi-stage XSS challenge demonstrating CSP bypass through HTTP redirects combined with sandboxed iframe escape. The vulnerability allows executing arbitrary JavaScript in a sandboxed iframe and accessing the parent page's URL fragment containing a flag by leveraging CSP path-based restrictions that are relaxed after redirects.

## Attack scenario (step by step)
1. Attacker crafts a Base64-encoded HTML payload containing a script tag pointing to an open redirect endpoint
2. The redirect is allowed by CSP (due to 'self' directive) and points to a gadget library on an allowed CDN domain
3. After redirect, CSP only validates the base domain (https://cdnjs.cloudflare.com) rather than the full path, allowing arbitrary library loading
4. HTMX or Angular library is loaded, providing an XSS execution gadget via event handlers or template injection
5. JavaScript executes within the sandboxed iframe context and performs a fetch('') request to the parent page
6. The request's referrer header or response reveals the parent URL fragment containing the flag, which is displayed via alert()

## Root cause
CSP specification deliberately allows redirects to bypass path-based restrictions to prevent side-channel attacks. Combined with: (1) unsanitized HTML in Base64 payload, (2) srcdoc iframe inheritance of parent CSP, (3) availability of gadget libraries on allowed CDN, and (4) implicit parent origin access through certain fetch behaviors in sandboxed contexts.

## Attacker mindset
An attacker would recognize that CSP path restrictions are not enforced post-redirect and systematically identify gadget libraries on allowed domains. They would exploit the sandbox's partial isolation by using relative or empty fetch requests to leak parent context information. This requires deep understanding of browser security model nuances and CDN library ecosystems.

## Defensive takeaways
- Avoid allowing full CDN domains in CSP; use specific file paths with hash/nonce validation instead
- Be aware that CSP path-based restrictions are intentionally bypassed after HTTP redirects - design CSP accordingly
- Do not rely on sandboxed iframes as sole XSS mitigation; combine with strict input validation and output encoding
- Sanitize and validate Base64-decoded content the same as raw HTML input
- Limit gadget libraries available on allowed domains (HTMX, Angular, jQuery) that enable expression evaluation
- Use 'allow-same-origin' sparingly in sandbox; the absence doesn't guarantee isolation against all attack vectors
- Test CSP effectiveness against real-world gadget chains, not just theoretical XSS payloads
- Consider using Trusted Types API to prevent DOM-based XSS in complex scenarios

## Variant hunting
Search for: (1) other gadget libraries on popular CDNs exploitable via template injection or event handlers, (2) alternative fetch/request techniques in sandboxed contexts to leak parent data, (3) CSP bypass via service workers or other redirect mechanisms, (4) combinations of sandbox attributes that provide unexpected access (allow-popup + allow-scripts interactions), (5) srcdoc-specific behaviors that differ from src-loaded frames

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS in web application)
- T1598 - Phishing: Web Credential Harvesting (if weaponized to steal session tokens from fragment)
- T1059 - Command and Scripting Interpreter (JavaScript execution)
- T1566 - Phishing (delivery vector for payload)

## Notes
This writeup exemplifies how security controls (CSP + sandbox) can be bypassed through chaining multiple subtle issues. The key insight is understanding CSP redirect handling (W3C design choice), recognizing gadget libraries as execution primitives, and identifying that sandbox isolation has edge cases. The srcdoc attribute's inheritance of parent CSP is often overlooked. This challenge is valuable for understanding that security is layered and no single control is bulletproof.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
