# PayPal Node.js Code Injection via Dust.js Template Engine (RCE)

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Template Injection, Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A critical RCE vulnerability was discovered in PayPal's demo application due to unsafe use of eval() in the Dust.js templating engine's 'if' helper function. By exploiting type confusion through array parameters and bypassing character encoding filters, an attacker could inject arbitrary JavaScript code and execute system commands with server privileges.

## Attack scenario (step by step)
1. Attacker performs HTTP parameter fuzzing and notices the server responds differently to backslash (\) and newline (%0a) characters, revealing syntax errors
2. Through error analysis, attacker identifies the application uses Dust.js templating engine with 'if' helpers that internally use eval()
3. Attacker discovers that single and double quotes are HTML-encoded as input filters, but realizes the filter function only works on strings
4. Attacker crafts a request using array parameter syntax (?device[]=...) to bypass the string encoding filter, since the qs module parses arrays differently
5. Attacker injects JavaScript payload that breaks out of the template context: ?device[]=x&device[]=y'-require('child_process').exec('command')-'
6. Server executes arbitrary system commands with application privileges, allowing data exfiltration and system compromise

## Root cause
Multiple compounding issues: (1) Use of eval() in Dust.js helper for expression evaluation, (2) Insufficient input validation relying only on string-based character encoding, (3) Type confusion vulnerability where array parameters bypass the encoding filter, (4) Lack of sandboxing or content security policies for template evaluation

## Attacker mindset
Methodical fuzzing approach to identify error-inducing inputs, followed by source code analysis to understand the templating engine. Recognition that input filters work on type assumptions (strings) and exploitation of type polymorphism in the query parameter parser. Pragmatic crafting of a minimal PoC to exfiltrate sensitive files.

## Defensive takeaways
- Never use eval() or equivalent dynamic code execution with user-controlled input
- Implement input validation at the type level, not just character filtering - validate both type AND content
- Use templating engines with sandboxed evaluation or expression languages without arbitrary code execution
- Apply defense in depth: filter dangerous characters, validate parameter types, use allowlists, and implement sandboxing
- Regularly audit dependencies for unsafe patterns, especially in security-critical components
- Consider using safer expression evaluators (e.g., expression parsers rather than full JavaScript eval)
- Implement request logging and monitoring to detect suspicious parameter patterns

## Variant hunting
['Test other templating engines for similar eval() usage patterns in helper functions', 'Look for parameter type confusion vulnerabilities in other Node.js frameworks where filters assume string types', 'Search for other instances where qs module array parsing bypasses string-based filters', "Examine other Dust.js helpers beyond 'if' that might use eval or unsafe evaluation", 'Test similar injection patterns against other PayPal endpoints using different parameter structures', 'Look for math/expression evaluation helpers in template engines that might have similar issues']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1059.007 - JavaScript/Node.js
- T1203 - Exploitation for Client Execution
- T1083 - File and Directory Discovery

## Notes
This vulnerability demonstrates the critical risks of using eval() with user input and the importance of understanding how parameter parsers handle different data types. The attack bypassed input sanitization through type confusion, a sophisticated technique requiring knowledge of both the templating engine internals and the underlying framework's parameter parsing behavior. The vulnerability chain shows how multiple seemingly minor issues compound into critical RCE.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
