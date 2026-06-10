# PayPal Node.js Dust.js Template Injection RCE

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Server-Side Template Injection, Code Injection, Remote Code Execution, Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A critical RCE vulnerability in PayPal's demo.paypal.com was discovered through Server-Side Template Injection in the Dust.js templating engine. The vulnerability exploited unsafe eval() usage in the 'if' helper combined with improper input sanitization that could be bypassed using array parameters, allowing arbitrary command execution.

## Attack scenario (step by step)
1. Attacker performs fuzzing on HTTP parameters and observes different responses for backslash (\) and newline (%0a) characters, indicating potential template injection
2. Analysis of error messages reveals Dust.js templating engine is in use, which uses eval() for 'if' helper expression evaluation
3. Attacker identifies that single and double quotes are HTML-encoded, preventing direct string breakout
4. Attacker discovers that query parameters can be parsed as arrays (device[]=value) by the qs module, bypassing string-based sanitization
5. Attacker crafts payload using array syntax to inject arbitrary JavaScript: device[]=x&device[]=y'-require('child_process').exec(...)-'
6. Payload executes system commands (cat /etc/passwd) and exfiltrates data via HTTP to attacker-controlled server

## Root cause
Multiple layered vulnerabilities combined: (1) Use of eval() in Dust.js 'if' helper for expression evaluation, (2) Insufficient input validation that only escaped strings while failing to handle array type parameters, (3) Type confusion vulnerability where input sanitization assumed string type but arrays bypassed the escaping logic

## Attacker mindset
Methodical fuzzing to discover unusual server behaviors, deep source code analysis of the templating engine, understanding of Node.js request parsing quirks (qs module), and type coercion exploitation to bypass security controls

## Defensive takeaways
- Never use eval() for expression evaluation; use safe expression parsers instead
- Implement comprehensive input validation that accounts for different parameter types (strings, arrays, objects), not just string escaping
- Validate and enforce parameter types at the application level before passing to templating engines
- Use allowlists for template expressions rather than blocklists for dangerous characters
- Implement strict Content Security Policy headers to limit template injection impact
- Use template engines with security-first design that don't support arbitrary code execution
- Apply defense-in-depth: sandbox template execution, use restrictive security contexts, limit available functions

## Variant hunting
Search for other applications using Dust.js with 'if' helpers; audit other templating engines (EJS, Pug, Handlebars) for similar eval() usage; test array parameter handling in query string parsers; look for type confusion vulnerabilities in input sanitization functions; identify other endpoints that reflect user input into template contexts

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1583

## Notes
This vulnerability chains multiple security issues: unsafe function (eval), weak input validation (string-only escaping), and type confusion (array vs string). The $10,000 bounty reflects the critical severity. The attack demonstrates the importance of understanding framework-specific parsing (qs module behavior) and how security controls can be circumvented through type system quirks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
