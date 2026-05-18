# Sandbox-iframe XSS Challenge Solution: CSP Bypass via Redirect + Parent Window Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Self-hosted CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** Educational/CTF (no monetary bounty mentioned)
- **Severity:** High
- **Vuln types:** Content Security Policy Bypass, Open Redirect, Cross-Site Scripting (XSS), Sandbox Bypass, Information Disclosure
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandbox-iframe XSS challenge that combined multiple vulnerabilities: Base64-encoded arbitrary HTML injection, CSP misconfiguration, and an open redirect. The attacker bypassed CSP using the redirect-relaxes-path rule to load gadget scripts from CDNs, then accessed the parent window's URL hash containing the flag despite sandbox restrictions.

## Attack scenario (step by step)
1. Attacker base64-encodes malicious HTML payload and injects it via the 'xss' search parameter
2. Payload is rendered inside a sandboxed iframe with allow-scripts, inheriting parent CSP policy
3. Attacker exploits CSP redirect behavior: CSP allows 'self' (open redirect endpoint) as script-src
4. Attacker crafts redirect URL pointing to allowed CDN domain, which after redirect only validates base domain
5. Attacker loads gadget script (HTMX or Angular) from CDN to achieve arbitrary JavaScript execution
6. Attacker uses fetch('') or other techniques to access parent window properties containing the flag hash, displaying it in alert()

## Root cause
Multiple layered security issues: (1) Base64 HTML injection without sanitization, (2) CSP misconfiguration treating redirect destinations differently (only base domain validation post-redirect), (3) Open redirect functionality enabled on trusted origin, (4) Reliance on iframe sandbox as primary XSS defense without robust input validation

## Attacker mindset
Understand that security layers must work in depth; a single bypass (CSP via redirect) combined with gadget loading enables full XSS. Recognize that CSP path restrictions are relaxed after redirects by design, creating an exploitable loophole. Leverage existing popular libraries as execution gadgets rather than crafting custom payloads.

## Defensive takeaways
- Implement input validation and HTML sanitization on all user-supplied content, not relying solely on sandbox attributes
- Avoid open redirects entirely; if required, strictly validate redirect targets against a whitelist
- Use CSP effectively but understand its limitations: path-based restrictions are relaxed post-redirect per spec
- Remove unnecessary dependencies from CSP allowlists, especially full-path CDN references
- Use 'allow-same-origin' restrictively; consider alternative communication mechanisms (postMessage) instead of relying on origin isolation
- Disable 'allow-modals' if not strictly necessary; it enables alert() execution
- Monitor and update library versions; known gadgets in popular libraries (Angular, HTMX) can be weaponized
- Test CSP effectiveness with actual redirect chains, not just direct loads

## Variant hunting
Similar vulnerabilities exist in: (1) Applications using blob: or data: URIs with iframe srcdoc and inherited CSP, (2) Systems allowing base64-decoded content without sanitization in other contexts (email clients, document viewers), (3) CDN-hosted libraries with known gadget chains (Angular, Vue, jQuery plugins), (4) Redirect endpoints on whitelisted domains used as proxies to bypass CSP directives

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566.002: Phishing - Spearphishing Link
- T1005: Data from Local System
- T1041: Exfiltration Over C2 Channel
- T1598: Phishing for Information

## Notes
This writeup demonstrates sophisticated CSP bypass technique documented in W3C spec but often overlooked. The challenge elegantly combines three attack layers: injection, CSP bypass via redirect, and sandbox escape. The author's hint about fetch('') behavior suggests leveraging inherited credentials or request metadata. Angular and HTMX gadgets are widely applicable across other XSS scenarios. The 'nonce' in CSP was ineffective against redirect-bypassed scripts.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
