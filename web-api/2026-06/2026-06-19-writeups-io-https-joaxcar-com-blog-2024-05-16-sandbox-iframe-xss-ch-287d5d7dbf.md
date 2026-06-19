# Sandbox-iframe XSS Challenge: CSP Bypass via Redirect and Parent Window Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Bug Bounty CTF Challenge
- **Bounty:** Non-monetary (CTF/Educational)
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Open Redirect, Sandbox Escape
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
The challenge demonstrated a multi-stage XSS vulnerability in a sandboxed iframe that combines CSP bypass via redirect exploitation, JavaScript gadget loading from CDNs, and parent window access through srcdoc inheritance. An attacker could bypass CSP restrictions by chaining an open redirect with a library gadget from an allowed CDN, then access the parent window's URL hash containing the flag.

## Attack scenario (step by step)
1. Attacker crafts malicious HTML payload as Base64 and passes it via xss parameter
2. Payload loads via srcdoc attribute in sandboxed iframe, inheriting parent CSP policy
3. Attacker exploits CSP redirect loophole: CSP restricts script-src but allows 'self' which includes open redirect endpoint
4. Attacker chains redirect to load HTMX or Angular from CDN (allowed after redirect due to base domain matching)
5. Loaded library executes attacker's embedded JavaScript gadget within iframe context
6. Despite sandbox restrictions, srcdoc-based frame can access parent via fetch('') to URL hash and trigger alert with flag

## Root cause
CSP specification allows redirects to bypass path-based restrictions by matching only base domain post-redirect; combined with srcdoc iframe inheriting parent CSP and library gadgets on allowed CDNs, this enables XSS. Additionally, srcdoc iframes can access parent window through non-standard channels despite sandbox restrictions.

## Attacker mindset
Recognizing that CSP is often a layered defense; looking for logical gaps like redirect handling in specification. Understanding that popular libraries become exploit gadgets. Knowing that sandbox implementations have subtle loopholes when combined with other mechanisms like srcdoc attribute.

## Defensive takeaways
- Implement strict CSP with 'strict-dynamic' to prevent gadget-based XSS even if external libraries are whitelisted
- Avoid open redirects entirely; if necessary, use allowlist validation without protocol-relative URLs
- Do not allow 'self' in script-src when hosting untrusted content; be explicit about allowed paths and files
- Consider CSP redirect behavior when designing policies; understand that base-domain matching post-redirect weakens path restrictions
- Use sandboxed iframes with srcdoc cautiously; prefer loading from truly cross-origin sources for stronger isolation
- Remove unnecessary library dependencies; audit CDN-hosted libraries for XSS gadgets
- Test iframe sandbox escapes by attempting fetch('') and window access from sandboxed contexts

## Variant hunting
Look for: (1) Other open redirects combined with whitelisted domains in CSP, (2) Alternative gadget libraries on allowed CDNs (jQuery, Dojo, etc.), (3) Sandbox escapes via other channels (postMessage with improper validation, blob: URLs), (4) CSP bypass via meta tags in srcdoc content, (5) Frame-bust techniques combined with CSP weaknesses

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539

## Notes
This writeup is educational and demonstrates real CSP weaknesses documented in W3C spec and referenced blogs. The CSP redirect bypass is a design choice to prevent side-channel leaks per spec, making it legitimate but dangerous. The challenge highlighted overlooked CSP mechanics; many security practitioners underestimate redirect handling implications. Sandbox escapes are subtle when combined with srcdoc inheritance.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
