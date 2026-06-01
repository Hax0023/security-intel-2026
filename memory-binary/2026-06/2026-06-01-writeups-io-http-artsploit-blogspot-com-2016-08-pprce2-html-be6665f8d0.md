# PayPal Demo Node.js Code Injection (RCE) via Dust.js Template Engine

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Template Injection, Unsafe eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A critical RCE vulnerability was discovered in PayPal's demo.paypal.com where user-supplied input was passed to eval() via the Dust.js templating engine's 'if' helper function. By leveraging type confusion through URL parameter array syntax, an attacker could bypass input sanitization and execute arbitrary shell commands on the server.

## Attack scenario (step by step)
1. Attacker fuzzes HTTP parameters and identifies that backslash (\) and newline (%0a) characters cause syntax errors, revealing server-side template processing
2. Attacker analyzes error messages and identifies the use of Dust.js templating engine with vulnerable 'if' helpers that use eval()
3. Attacker discovers that standard quote character filtering uses a replace() function that only handles string types, not arrays
4. Attacker exploits type confusion by sending array parameters using bracket syntax: ?device[]=value1&device[]=value2, causing qs module to parse as Array instead of string
5. Attacker crafts payload using array syntax with closing quote and JavaScript code: ?device[]=x&device[]=y'-require('child_process').exec('command')-'
6. Attacker executes arbitrary commands (e.g., exfiltrating /etc/passwd) on the vulnerable server

## Root cause
Multiple security failures: (1) Use of eval() in Dust.js 'if' helper for expression evaluation, (2) Input sanitization logic that only handles string type and fails when parameter is parsed as array, (3) Insufficient server-side template engine hardening, (4) Type confusion between string and array parameters in URL parsing

## Attacker mindset
Methodical fuzzing approach to identify unusual error responses, followed by source code analysis to understand the underlying technology. Exploited type confusion and the assumption that sanitization would handle all inputs, demonstrating deep understanding of Node.js module behavior and server-side template injection techniques.

## Defensive takeaways
- Never use eval() for expression evaluation; use safer alternatives like expression parsers or sandboxed evaluation environments
- Implement input validation that accounts for all possible parameter types (strings, arrays, objects), not just strings
- Use parameterized/safe templating engines that do not execute arbitrary code
- Apply defense-in-depth: validate input at multiple layers and use security contexts/sandboxing
- Keep templating library dependencies updated and monitor for security advisories
- Disable eval() entirely if possible, or restrict its usage with comprehensive code review
- Implement strict Content Security Policy and disable dangerous JavaScript execution modes

## Variant hunting
["Search for other Dust.js 'if' helper usage patterns in Node.js applications", 'Test for similar type confusion in other parameter parsing libraries (body-parser, express, etc.)', 'Audit other Node.js templating engines (EJS, Handlebars, Jade) for eval() usage', 'Check for eval() or Function() constructor usage in expression evaluation contexts', 'Hunt for applications that perform sanitization only on string types without type validation', 'Test array parameter handling in various Node.js frameworks for bypass opportunities', 'Look for other sandbox escapes in Node.js require() contexts']

## MITRE ATT&CK
- T1190
- T1203
- T1059.004
- T1059.001

## Notes
This vulnerability represents a classic case of multi-layered security failure: dangerous function (eval), incomplete input validation (type assumption), and type confusion exploitation. The payload demonstrates real command execution with data exfiltration. The $10,000 bounty reflects the critical nature and clear RCE impact.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
