# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute JavaScript and call functions without using parentheses or semicolons by leveraging the onerror handler combined with throw statements. The method works by assigning functions to onerror and using throw to pass arguments, with variations using block statements, throw expressions, and error object literals to bypass input filters.

## Attack scenario (step by step)
1. Attacker identifies that target application filters parentheses and semicolons from user input to prevent XSS
2. Attacker uses the block statement technique: <script>{onerror=alert}throw 1337</script> to execute alert without parentheses or semicolons
3. Alternatively, attacker assigns onerror inside throw expression: <script>throw onerror=alert,'payload'</script>
4. For eval-based payloads, attacker prepends '=' to bypass 'Uncaught' exception prefix: <script>{onerror=eval}throw'=alert\x281337\x29'</script>
5. On Firefox where 'uncaught exception' prefix breaks syntax, attacker uses error object literal with message property containing payload
6. Payload executes arbitrary JavaScript in victim's browser context, stealing cookies, session tokens, or redirecting to malicious site

## Root cause
Input filters blocking parentheses and semicolons as XSS mitigation are incomplete. The onerror handler and throw statement combination provides alternative execution paths. The JavaScript exception handling mechanism allows implicit function calls without explicit parenthesis syntax, and error object literals can be crafted to work with eval without semicolons.

## Attacker mindset
Security through obscurity via syntax filtering is bypassable. The researcher discovered that JavaScript's exception handling and object literal syntax provide alternative code paths to achieve the same result. Understanding language semantics and exception flow is key to finding filter evasion techniques.

## Defensive takeaways
- Do not rely on blacklist filters for parentheses, semicolons, or other syntax elements as primary XSS prevention
- Implement Content Security Policy (CSP) with strict directives (script-src 'none') to prevent inline script execution
- Use output encoding/escaping appropriate to context (HTML entity encoding, JavaScript string escaping)
- Consider allowlist-based input validation rather than blacklist filtering
- Disable inline event handlers and script tags through CSP headers
- Use templating engines that auto-escape by default
- Regularly test filter effectiveness against known bypass techniques

## Variant hunting
Search for other JavaScript constructs that achieve function calls without parentheses: tagged template literals, Proxy handlers, getters/setters, async/await without parentheses, destructuring assignments, computed property access with side effects. Test against application/json responses that might bypass HTML context filters.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1598 - Phishing for Information (credential theft via XSS)

## Notes
This research demonstrates that syntax-based security filters are fundamentally flawed. The onerror/throw technique is browser-agnostic but requires different payloads for Chrome vs Firefox due to exception message prefixes. The technique is practical in real-world scenarios where developers attempt to 'sanitize' by filtering specific characters rather than implementing proper encoding/CSP controls.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
