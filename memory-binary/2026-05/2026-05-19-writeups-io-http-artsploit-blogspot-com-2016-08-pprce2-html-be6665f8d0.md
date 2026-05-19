# PayPal Node.js Code Injection via Dust.js Template Engine

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Template Injection, Unsafe eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
PayPal's demo.paypal.com endpoint used the Dust.js templating engine with unsafe eval() in the 'if' helper function to evaluate user-controlled input. By exploiting type confusion through array parameters that bypassed string-based character filtering, an attacker could inject arbitrary JavaScript code and achieve remote code execution.

## Attack scenario (step by step)
1. Attacker performs HTTP parameter fuzzing and discovers the server responds differently to backslash (\) and newline (%0a) characters, indicating template injection
2. Attacker identifies Dust.js templating engine from error messages and reviews its source code, discovering the 'if' helper uses eval() for expression evaluation
3. Attacker analyzes the input sanitization function and discovers it only filters strings, not arrays
4. Attacker sends crafted request with array parameters: ?device[]=x&device[]=y'-payload-' which bypasses string filtering
5. Attacker injects arbitrary JavaScript code to execute system commands via require('child_process').exec()
6. Attacker exfiltrates sensitive files (e.g., /etc/passwd) to external server via curl command

## Root cause
Multiple compounding vulnerabilities: (1) Use of unsafe eval() in Dust.js 'if' helper for expression evaluation, (2) Input sanitization only protecting string types while allowing array types to bypass filtering, (3) Type confusion vulnerability where array parameters weren't properly validated before eval() processing

## Attacker mindset
Systematic fuzzing approach to identify template injection vectors, deep analysis of open-source library source code to understand security mechanisms, exploitation of type confusion edge case that developers overlooked during sanitization implementation

## Defensive takeaways
- Avoid eval() and similar dynamic code execution functions; use safe expression evaluators or sandboxed environments
- Apply input validation and sanitization consistently across all parameter types (strings, arrays, objects)
- Implement strict type checking before processing user input with security-sensitive functions
- Use parameterized/templated expressions instead of dynamic code evaluation
- Keep third-party templating engines and libraries updated to latest secure versions
- Implement defense-in-depth with multiple validation layers rather than relying on single sanitization function
- Use Content Security Policy and other runtime security controls to limit impact of injection flaws

## Variant hunting
['Test other array/object parameters for similar type confusion bypasses in sanitization logic', "Check for other Dust.js helpers beyond 'if' that might use eval() or similar functions", 'Look for similar patterns in other Node.js templating engines (EJS, Handlebars, Pug) using eval()', 'Test nested array/object structures for deeper bypass of sanitization (device[foo][bar]=...)', 'Examine other PayPal endpoints or subdomains using legacy Dust.js versions', 'Research other applications using old versions of Dust.js or similar vulnerable templating patterns']

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1047
- T1087

## Notes
This vulnerability chain demonstrates the importance of understanding type systems in sanitization contexts. The attacker's systematic approach (fuzzing → error analysis → source code review → type confusion exploitation) is exemplary. The $10,000 bounty reflects the critical nature of unauthenticated RCE. The use of array syntax to bypass string-specific filtering is a common pattern in parameter parsing vulnerabilities across multiple frameworks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
