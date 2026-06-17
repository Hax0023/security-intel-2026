# Sandbox-iframe XSS Challenge: CSP Bypass via Redirect and Parent Window Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Self-hosted CTF Challenge (sandbox-iframe-ctf.glitch.me)
- **Bounty:** N/A (Educational CTF)
- **Severity:** high
- **Vuln types:** Content Security Policy Bypass, Cross-Site Scripting (XSS), Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandboxed iframe XSS challenge demonstrated bypassing strict CSP protections through a known CSP redirect loophole that allows loading arbitrary scripts from whitelisted domains after redirects. The attacker leveraged an open redirect endpoint combined with CDN-hosted libraries (HTMX or Angular) to achieve code execution, then accessed the parent window's URL fragment containing a flag despite sandbox restrictions.

## Attack scenario (step by step)
1. Attacker crafts Base64-encoded HTML payload containing a script tag that redirects through the vulnerable /redirect endpoint
2. The redirect URL points to a CDN script (htmx.min.js or angular.js) from a domain listed in CSP directives
3. Browser's CSP validation passes on initial request to /redirect (allowed by 'self'), then after redirect only validates base domain per CSP specification
4. Arbitrary library loads and executes, providing XSS gadgets (HTMX event handlers or Angular template injection)
5. JavaScript code uses fetch('') or similar technique to access parent window context despite null origin sandbox restriction
6. Flag from parent URL hash is extracted and displayed in alert box, exfiltrating the sensitive data

## Root cause
CSP specification intentionally allows redirects to match only base domain rather than full path to prevent side-channel leaks. Combined with: (1) unsanitized Base64 payload injection into iframe, (2) open redirect endpoint permitted by 'self' directive, (3) overly permissive iframe sandbox attributes (allow-scripts present), and (4) unsafe reliance on null origin as security boundary.

## Attacker mindset
Security researcher/CTF player systematically probed CSP constraints, recognized the redirect loophole as documented attack surface, identified gadget chains in popular libraries, and exploited nuanced behavior differences between sandboxed iframe origins and parent window access mechanisms.

## Defensive takeaways
- Avoid relying solely on sandbox restrictions; combine with additional isolation mechanisms
- Use 'unsafe-none' CSP or eliminate 'unsafe-eval' to reduce gadget library availability
- Implement strict path-based CSP directives but acknowledge redirect bypass potential in threat model
- Disable 'allow-scripts' in iframe sandbox unless absolutely necessary; use 'allow-same-origin' cautiously
- Sanitize all user input before Base64 encoding for iframe srcdoc injection
- Avoid open redirects entirely; if required, validate redirect targets against strict allowlist
- Store sensitive data (flags) outside URL fragments; use secure, httpOnly session mechanisms
- Monitor and restrict loading of gadget-rich libraries; consider SRI (Subresource Integrity) hashes
- Use nonces/hashes in CSP but understand they don't protect against gadget chains in whitelisted libraries

## Variant hunting
['Explore other CSP-whitelisted CDNs for additional RCE gadgets beyond HTMX/Angular', "Test whether fetch('') behavior extends to accessing other cross-origin parent resources", "Investigate if srcdoc iframe can abuse 'report-uri' CSP directive for data exfiltration", 'Probe whether timing-based attacks on CSP violations leak parent URL structure', 'Test postMessage vectors to communicate between sandboxed iframe and parent despite restrictions', 'Search for library versions with pre-existing vulnerabilities on whitelisted CDNs', 'Examine if frame-ancestors CSP bypass techniques apply to sandbox escape scenarios']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1203: Exploitation for Client Execution
- T1059: Command and Scripting Interpreter
- T1563: Exploitation for Credential Access
- T1052: Exfiltration Over Web Service

## Notes
Challenge elegantly demonstrates that security-in-depth layering (CSP + sandbox + path restrictions) can still fail when individual components have design choices or loopholes that interact unexpectedly. The writeup is educational for understanding CSP redirect behavior (W3C spec intentional design, not a bug). Real-world applicability: developers often misunderstand CSP path enforcement and assume redirects are blocked; this is a critical assumption to validate during security reviews.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
