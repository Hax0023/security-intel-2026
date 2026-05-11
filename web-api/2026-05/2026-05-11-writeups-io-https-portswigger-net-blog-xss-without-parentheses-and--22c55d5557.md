# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** PortSwigger Research / General Security Community
- **Bounty:** N/A - Security Research Publication
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Injection
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
Gareth Heyes discovered multiple techniques to execute arbitrary JavaScript code in contexts where parentheses and semi-colons are filtered, using onerror handlers combined with throw statements and creative object literal constructions. The research demonstrates how exception handlers can be abused to bypass input validation filters that target common function call syntax.

## Attack scenario (step by step)
1. Attacker identifies a web application that filters parentheses and semi-colons in user input to prevent XSS attacks
2. Attacker crafts a payload using onerror assignment within a block statement, such as: <script>{onerror=alert}throw 1337</script>
3. Attacker alternatively uses throw statement with assignment expression to execute function without semi-colon separator
4. For filters that block simple payloads, attacker uses eval exception handler with Firefox-compatible object literal containing Error properties: {lineNumber:1,columnNumber:1,fileName:1,message:payload}
5. Attacker exploits platform-specific differences (Chrome vs Firefox) in exception message prefixes to craft working payloads
6. Injected payload executes in victim's browser context, allowing cookie theft, session hijacking, or malware delivery

## Root cause
Input validation filters that specifically target parentheses and semi-colons fail to account for alternative JavaScript syntax paths that achieve function execution. The onerror exception handler mechanism provides a direct channel to execute functions outside normal call syntax, and JavaScript's flexible expression evaluation allows assignments and function references to be embedded within statement contexts.

## Attacker mindset
Security researcher demonstrating limitations of blacklist-based input filtering. The attacker mindset focuses on finding creative JavaScript syntax alternatives, understanding browser-specific exception handling behavior, and systematically testing minimal payloads to bypass incremental filter improvements. This represents offensive security research to educate defenders about filter evasion.

## Defensive takeaways
- Whitelist-based input validation is superior to blacklist approaches; define exactly what characters/patterns are allowed rather than blocking specific syntax
- Understand that multiple JavaScript syntactic paths can achieve the same execution result - filtering one syntax doesn't prevent alternatives
- Implement Content Security Policy (CSP) to prevent inline script execution regardless of payload syntax
- Use JavaScript sandboxing or template systems that prevent arbitrary code execution entirely
- Test filter effectiveness against exception handling mechanisms, not just direct function call patterns
- Consider browser context and exception handling differences when designing filters
- Apply output encoding appropriate to context (HTML encoding, JavaScript string escaping, etc.) rather than input filtering alone

## Variant hunting
['Test other exception types (ReferenceError, SyntaxError) as alternative paths to onerror handler invocation', 'Explore Promise.reject() and async/await rejection handlers as execution vectors', 'Research event handler alternatives beyond onerror (onload, ontimeout, etc.) that bypass filters', 'Investigate whether Proxy objects or Reflect API can create function calls without parentheses', 'Test filters against template literals with embedded expressions that bypass parenthesis blocking', 'Examine whether import() dynamic module loading works without parentheses in filtered contexts', 'Research Symbol.hasInstance or other metaprogramming approaches to achieve code execution']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059.007 - Command and Scripting Interpreter: JavaScript/Node.js
- T1021.011 - Remote Services: Application Layer Protocol

## Notes
This is foundational XSS filter bypass research published by a leading security researcher. The techniques demonstrate that security controls based on character/syntax blacklisting are fundamentally weak. The blog post includes contributions from @terjanq and Pepe Vila showing even more creative bypass vectors. Key insight: JavaScript's exception handling mechanism was not designed with security filtering in mind, making it a reliable channel for code execution when input sanitization focuses only on typical function call syntax. The research spans multiple browser implementations, revealing that browser-specific behaviors create additional bypass opportunities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
