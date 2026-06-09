# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Input Validation Bypass, Filter Evasion
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript and call functions without using parentheses or semi-colons by leveraging onerror handlers and throw statements. The method works across browsers by using different exception handling approaches, bypassing common WAF/filter restrictions that block parentheses and semicolons.

## Attack scenario (step by step)
1. Attacker identifies a web application filtering parentheses and semi-colons in user input
2. Attacker crafts XSS payload using onerror handler assignment within throw statement: <script>{onerror=alert}throw 1337</script>
3. Attacker alternatively uses throw expression syntax: <script>throw onerror=alert,'payload'</script>
4. For eval-based payloads on Chrome, attacker prefixes string with '=' to leverage 'Uncaught' prefix: <script>{onerror=eval}throw'=alert\x281337\x29'</script>
5. On Firefox where 'uncaught exception' prefix causes issues, attacker uses Error object literal with required properties to bypass: <script>{onerror=eval}throw{lineNumber:1,columnNumber:1,fileName:1,message:'alert\x281\x29'}</script>
6. JavaScript executes arbitrary code, stealing cookies, session tokens, or performing malicious actions

## Root cause
Input filters blocking parentheses and semi-colons are insufficient to prevent XSS attacks. The onerror handler and throw statement provide alternative execution paths that bypass syntactic restrictions. Different browsers handle exception prefixing differently, creating multiple bypass vectors. Object literal properties can emulate Error behavior without requiring function calls.

## Attacker mindset
Bypass common filter/WAF restrictions by finding alternative JavaScript execution syntax. Exploit exception handling mechanisms that developers overlook. Research browser-specific behaviors to develop cross-platform payloads. Use object literals and property manipulation to avoid forbidden syntax.

## Defensive takeaways
- Filter parentheses and semi-colons alone are insufficient - implement proper output encoding/escaping
- Use Content Security Policy (CSP) to restrict inline script execution and eval usage
- Validate and sanitize all user input server-side, not just filter specific characters
- Block onerror event handlers and script tags entirely if not needed
- Implement allowlist-based input validation rather than blacklist-based filtering
- Use templating engines with automatic HTML escaping
- Test security controls against known XSS bypass techniques
- Monitor for suspicious exception handling patterns in JavaScript

## Variant hunting
['Test with other event handlers (oninput, onload, onmouseover) combined with throw statements', 'Explore other Error object properties across browser versions', 'Investigate whether other statement types (try/catch, if blocks) can serve as statement separators', 'Test whether comma operator or other operators can chain statements without semi-colons', 'Research additional exception prefixes in other browsers or Edge cases', 'Examine whether getter/setter properties can bypass execution restrictions', 'Test combinations with template literals and expression syntax']

## MITRE ATT&CK
- T1190
- T1059.007

## Notes
This research demonstrates that character-level input filtering is an ineffective security control. The technique exploits fundamental JavaScript language features (exception handling, statement syntax) that filters typically don't consider. Browser-specific behaviors create additional complexity for defensive measures. Originally published May 2019, updated March 2020, suggesting ongoing refinement and testing. The writeup is from PortSwigger (Burp Suite creators), indicating this is security research rather than an actual bug bounty finding.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
