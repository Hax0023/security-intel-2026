# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** PortSwigger Research (Educational)
- **Bounty:** N/A - Research Publication
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Injection
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript code and call functions without using parentheses or semi-colons by leveraging the onerror handler with throw statements. The method works across multiple browsers using different approaches: block statements, expression-based throws, and eval with Error object properties, bypassing common WAF/input filters.

## Attack scenario (step by step)
1. Attacker identifies web application filtering parentheses and semi-colons to prevent XSS
2. Attacker injects payload using block statement syntax: <script>{onerror=alert}throw 1337</script>
3. JavaScript parser executes the block statement without requiring semi-colon separation
4. Throw statement triggers onerror handler, passing value as argument to alert function
5. For eval-based payloads, attacker uses Error object literal with message property containing encoded JavaScript
6. Arbitrary code executes despite input filtering restrictions

## Root cause
Input validation filters focus on syntactic requirements (parentheses, semi-colons) rather than semantic execution paths. The onerror exception handler provides an alternative function invocation mechanism not protected by typical filters. Browser exception handling behavior allows expressions within throw statements and Error object properties to bypass parser restrictions.

## Attacker mindset
Filter evasion through alternative execution paths - when direct function call syntax is blocked, find indirect invocation mechanisms. Leverage JavaScript's flexible syntax (block statements, throw expressions) and exception handling to achieve code execution. Reverse-engineer browser exception formatting to craft payloads that work cross-browser.

## Defensive takeaways
- Filter validation must focus on code semantics and execution capabilities, not just syntax characters
- Implement comprehensive Content Security Policy (CSP) to prevent inline script execution
- Use allowlist-based HTML sanitization rather than blacklist filtering
- Disable or restrict onerror handlers in user-controlled content contexts
- Apply context-aware output encoding for all user input
- Test filters against various JavaScript execution patterns and browser quirks
- Consider using a Web Application Firewall with semantic JavaScript analysis

## Variant hunting
['Similar techniques using onload, oninput, or other event handlers as exception handlers', 'Leveraging other statement types (try/catch, if blocks) for semi-colon avoidance', 'Using template literals with expression evaluation to bypass filters', 'Combining with other character encoding schemes (unicode escapes, entity encoding) to bypass parentheses filters', 'Testing with different Error object properties across browser versions', 'Using arrow functions or generator functions as exception handlers where supported']

## MITRE ATT&CK
- T1190
- T1059.007
- T1562.008

## Notes
This is a seminal research piece by Gareth Heyes demonstrating filter bypass techniques. The article documents multiple working approaches: basic block statement variant, expression-based throw variant, and eval-based variant with Error object literals for cross-browser compatibility. Published May 2019, updated March 2020. Highlights how restrictive filters create false sense of security if underlying execution mechanisms remain unprotected.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
