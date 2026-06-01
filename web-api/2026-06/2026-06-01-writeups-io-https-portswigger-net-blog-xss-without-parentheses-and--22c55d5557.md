# XSS without Parentheses and Semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** N/A - Educational research
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), WAF Bypass, Filter Evasion
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute JavaScript functions without using parentheses or semi-colons by leveraging the onerror handler and throw statement. The method works by assigning functions to the onerror handler and using throw with expressions to pass arguments, effectively bypassing common WAF filters that block these characters.

## Attack scenario (step by step)
1. Attacker identifies a web application filtering parentheses and semi-colons in user input
2. Attacker crafts XSS payload using onerror handler: <script>{onerror=alert}throw 1337</script>
3. Payload bypasses WAF/filter because it contains no parentheses or semi-colons
4. JavaScript engine executes the block statement and throw statement sequentially
5. The throw statement creates an exception, triggering the onerror handler with the thrown value as argument
6. Alert function executes with attacker-controlled data, achieving arbitrary code execution

## Root cause
WAF/filter implementations assume JavaScript function calls require parentheses and statements require semi-colons. This overlooks alternative JavaScript execution patterns using exception handlers and expression evaluation. Additionally, Firefox's error message prefixing behavior can be circumvented using Error object prototypes.

## Attacker mindset
Attackers recognize that defensive filters focus on syntactic patterns rather than semantic execution paths. By understanding JavaScript's exception handling mechanism and block statement semantics, alternative execution vectors bypass naive character-based filters. The attacker exploits the flexibility of JavaScript's grammar to achieve the same result through non-obvious syntax.

## Defensive takeaways
- Character-based blacklisting of parentheses/semi-colons is insufficient; implement context-aware sanitization
- Use Content Security Policy (CSP) with strict script-src to prevent inline script execution
- Employ a robust HTML parser and sanitizer rather than regex-based filtering
- Validate and encode output based on context (HTML, JavaScript, URL, CSS)
- Consider AST-based analysis rather than string matching for payload detection
- Use allowlist-based filtering of permitted syntax patterns when possible
- Test filters against creative JavaScript syntax variations and grammar alternatives

## Variant hunting
Search for additional JavaScript execution methods bypassing common filters: (1) using template literals and expression interpolation, (2) leveraging getter/setter properties, (3) exploiting Event handler attributes with newlines/unicode, (4) using Function constructor alternatives, (5) chaining methods without parentheses via proxies or symbols, (6) using spread operators and destructuring syntax

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1055 - Process Injection (via XSS)
- T1087 - Account Discovery

## Notes
This research demonstrates the danger of syntactic filtering without understanding language semantics. The technique is particularly relevant for applications with weak input validation. Chrome and Firefox handle error prefixing differently, requiring browser-specific adaptations. The research includes practical demonstrations of working around both parentheses/semi-colon filters and browser-specific error message formatting.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
