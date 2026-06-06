# Sandbox-iframe XSS Challenge Solution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Personal CTF Challenge
- **Bounty:** N/A - Educational CTF
- **Severity:** high
- **Vuln types:** Content Security Policy Bypass, Cross-Site Scripting (XSS), Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandbox iframe XSS challenge demonstrating CSP bypass through open redirects combined with CDN gadget loading. The vulnerability chain bypasses CSP restrictions by exploiting the CSP specification's redirect handling behavior, allowing arbitrary JavaScript execution within a sandboxed iframe and subsequent access to parent window data.

## Attack scenario (step by step)
1. Attacker base64-encodes malicious HTML payload containing script tags and gadget elements
2. Payload is submitted via the xss parameter, decoded, and rendered in a sandboxed iframe with srcdoc attribute
3. Attacker crafts initial script tag pointing to attacker-controlled open redirect endpoint (allowed by 'self' directive)
4. Browser follows redirect to CDN domain; CSP only validates base domain after redirect (per specification), bypassing path restrictions
5. Attacker loads JavaScript gadget (HTMX or Angular) from CDN to achieve code execution within iframe
6. Attacker leverages iframe-to-parent communication or fetch() behavior to extract flag from parent window URL hash and display via alert()

## Root cause
The combination of three security mechanisms working against each other: (1) CSP redirect handling exemption allowing base domain matching post-redirect, (2) iframe inheriting parent CSP when using srcdoc attribute, (3) sandbox attribute not preventing all communication vectors with parent context. The open redirect mechanism is unprotected and serves as the pivot point.

## Attacker mindset
An attacker would recognize that sandbox restrictions are not absolute and that CSP redirects represent a documented but underutilized bypass vector. The attacker would research available gadgets on allowed CDNs (HTMX, Angular) rather than crafting inline payloads, understand iframe srcdoc CSP inheritance mechanics, and exploit the specific fetch('') behavior to communicate across iframe boundaries despite null origin assignment.

## Defensive takeaways
- Do not rely on sandbox attribute alone for content isolation; use complementary protections
- Implement redirect validation and restrict redirect targets, especially from user-controlled parameters
- Be aware of CSP redirect handling exceptions and their security implications per W3C specification
- Avoid loading unnecessary third-party libraries from CDNs; use subresource integrity (SRI) for any external resources
- Test iframe sandboxing with realistic XSS payloads and gadget libraries to verify actual security posture
- Consider using frame-ancestors directive alongside sandbox to restrict iframe embedding contexts
- Apply CSP consistently to srcdoc iframes; document and verify inheritance behavior

## Variant hunting
Similar bypasses could target: (1) other CDN-hosted gadget libraries not explicitly blocked (Vue, React, jQuery plugins), (2) alternative redirect mechanisms (meta refresh, form submission), (3) different iframe loading methods (src with data: URIs), (4) fetch() variations exploiting empty string or relative path behavior, (5) postMessage communication if allow-same-origin is enabled elsewhere, (6) timing attacks against CSP validation during redirects

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1090 - Proxy (open redirect)
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1656 - Impersonate Valid User

## Notes
This is an exceptional educational writeup demonstrating sophisticated exploit chaining. Key insight is that CSP's redirect handling (RFC-documented, intentional design) becomes a liability when combined with open redirects and gadget loading. The challenge elegantly demonstrates why security mitigations in depth are necessary. The fetch('') hint references a subtle behavior where relative fetches from null-origin iframes may still resolve against parent context in certain scenarios.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
