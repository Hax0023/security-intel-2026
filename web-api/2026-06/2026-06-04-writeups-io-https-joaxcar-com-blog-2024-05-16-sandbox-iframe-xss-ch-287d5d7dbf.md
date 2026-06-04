# Sandbox-iframe XSS Challenge Solution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Self-hosted CTF Challenge
- **Bounty:** Educational/CTF
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandbox iframe XSS challenge demonstrating CSP bypass through open redirects to load arbitrary scripts from CDNs, combined with sandbox attribute misconfigurations. The vulnerability chain allows executing arbitrary JavaScript within a sandboxed iframe to access the parent window's hash fragment containing a flag.

## Attack scenario (step by step)
1. Attacker crafts Base64-encoded HTML payload containing script tags and image elements
2. Payload is injected via the 'xss' parameter into a sandboxed iframe with allow-scripts enabled
3. Attacker bypasses CSP by leveraging an open redirect endpoint allowed by 'self' in script-src directive
4. Redirect chains to a CDN (cdnjs.cloudflare.com) which is then treated as a valid source after redirect per CSP spec
5. Attacker loads JavaScript gadgets (HTMX or AngularJS) from CDN to achieve arbitrary code execution
6. Within the iframe context, attacker uses fetch or other techniques to access parent window's hash fragment containing the flag

## Root cause
Multiple security control weaknesses: (1) CSP implementation allows redirects to bypass path-specific restrictions per W3C spec, (2) open redirect endpoint exists at /redirect, (3) sandbox iframe allows both scripts and modals, (4) srcdoc-loaded content inherits parent CSP and can access parent frame hash, (5) Base64 sanitization only protects DOM structure, not content execution

## Attacker mindset
Security researcher identifying that CSP path restrictions are bypassable via redirects—a documented but overlooked feature. Recognizing that public CDNs host exploitable JavaScript libraries (HTMX event handlers, AngularJS templates) that can be weaponized when loaded after a redirect. Combining multiple weak controls to escalate from HTML injection to arbitrary code execution with potential parent frame access.

## Defensive takeaways
- Avoid open redirects entirely; if necessary, implement strict allowlist validation without external redirects
- Use CSP directives that restrict entire domains cautiously—understand redirect behavior per W3C CSP3 spec
- For sandbox iframes, omit allow-scripts unless absolutely necessary; consider allow-scripts with restricted sandbox origins
- Use nonce-based or hash-based CSP with 'unsafe-eval' removal to prevent gadget-chain attacks
- Sanitize and validate Base64-decoded content, not just the encoded string itself
- Store sensitive data (like flags/tokens) in secure, httpOnly cookies or server-side sessions rather than URL fragments
- Test sandbox iframe security with threat models that assume JavaScript execution within the frame
- Monitor and restrict access to public CDNs hosting known gadget libraries in security-critical contexts

## Variant hunting
['Test other open redirect patterns (query params, fragments) combined with different CSP directives (style-src, font-src, frame-src)', 'Identify alternative gadget libraries on CDNs exploitable via CSP bypass (jQuery, Lodash, Webpack bundles with exposed globals)', 'Explore sandbox attribute combinations: allow-same-origin + allow-scripts without allow-top-navigation-by-user-activation', 'Investigate srcdoc vs src iframe loading differences and CSP inheritance behaviors across browsers', "Test fetch('') and other relative URL requests from null-origin sandboxed contexts to identify parent access vectors", 'Search for similar CTF-style challenges combining sandbox + CSP + gadget chains']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS via parameter injection)
- T1021 - Remote Services (sandbox escape to parent window access)
- T1566.002 - Phishing: Spearphishing Link (malicious base64 payload in URL parameter)

## Notes
This writeup is particularly valuable for understanding CSP bypass mechanics—specifically the W3C-specified behavior where redirects reset path-based CSP restrictions to domain-level matching. The challenge elegantly combines multiple weak controls (open redirect + gadget-chain libraries + sandbox + CSP inheritance) into an exploitable chain. Key insight: CSP 'self' + open redirect + allowed CDN domain = arbitrary script loading. The hint about fetch('') behavior from null-origin frames suggests additional parent-frame communication vectors not fully detailed in the excerpt. Educational value high for understanding modern XSS exploitation beyond simple injection.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
