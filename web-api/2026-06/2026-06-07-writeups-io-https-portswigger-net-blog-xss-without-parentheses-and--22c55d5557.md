# XSS without Parentheses and Semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** N/A - Research Publication
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Execution
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript and call functions without parentheses or semi-colons by leveraging onerror handlers and throw statements. The vulnerability bypasses input filters that block parentheses and semi-colons by using block statements, throw expressions, and object literals with Error prototypes.

## Attack scenario (step by step)
1. Attacker identifies a web application that filters parentheses and semi-colons from user input
2. Attacker crafts XSS payload using <script>{onerror=alert}throw 1337</script> syntax without parentheses
3. Attacker uses throw expression inside onerror assignment: <script>throw onerror=alert,'payload'</script>
4. For eval-based payloads, attacker prefixes strings with '=' to leverage Firefox exception handling differences
5. Attacker bypasses Firefox's 'uncaught exception' prefix by using Error object literal with specific properties
6. Payload executes arbitrary JavaScript in victim's browser context, stealing cookies/sessions or performing actions

## Root cause
Input filtering mechanisms that block parentheses and semi-colons fail to account for alternative JavaScript syntax patterns using onerror handlers, throw statements, block statements, and object literals. Developers assume these characters are necessary for function execution and exception creation.

## Attacker mindset
Researching edge cases and browser-specific behaviors to find polyglot payloads that work across multiple browsers. Testing alternative syntax that accomplishes the same goal (function execution) without restricted characters. Leveraging error handling mechanisms in unexpected ways.

## Defensive takeaways
- Implement allowlist-based input validation rather than blocklist filtering of specific characters
- Apply Content Security Policy (CSP) with strict script-src directives to prevent inline script execution
- Use parameterized contexts and proper output encoding for all user-controlled data
- Sanitize input comprehensively understanding full JavaScript syntax, not just common patterns
- Test filters against known bypass techniques and maintain updated WAF/filter rules
- Implement server-side template sandboxing and avoid server-side code generation from user input
- Use security headers like X-XSS-Protection and properly configure CORS policies

## Variant hunting
Research alternate JavaScript execution contexts (oninput, onload, onmouseover), test other exception-handling mechanisms (Promise.reject), explore template literals and destructuring assignment, investigate optional chaining and nullish coalescing operators for filter evasion, test with different encoding schemes (unicode escapes, hex entities)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing

## Notes
Groundbreaking research published by Gareth Heyes demonstrating that character-based blacklist filtering is fundamentally flawed. The technique shows how browser-specific error handling (Chrome vs Firefox differences) can be exploited. Original publication in May 2019, updated March 2020. Demonstrates importance of understanding JavaScript semantics beyond basic syntax.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
