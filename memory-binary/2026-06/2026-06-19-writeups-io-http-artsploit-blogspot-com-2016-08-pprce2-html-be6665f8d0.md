# PayPal Node.js Dust.js Template Injection RCE via Array Parameter Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Server-Side Template Injection (SSTI), Code Injection, Remote Code Execution (RCE), Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A critical RCE vulnerability existed in PayPal's demo.paypal.com due to unsafe use of eval() in Dust.js template engine's 'if' helper combined with improper input sanitization. The vulnerability was exploitable by bypassing character encoding filters through Node.js array parameter parsing, allowing arbitrary code execution on the server.

## Attack scenario (step by step)
1. Attacker performs HTTP parameter fuzzing and discovers that backslash (\) and newline (%0a) characters cause syntax errors, revealing server-side template processing
2. Attacker identifies Dust.js templating engine from error messages and reviews public source code to find eval() usage in 'if' helpers
3. Attacker discovers that single/double quotes are HTML-encoded to prevent direct string breakout, but recognizes this sanitization has a flaw
4. Attacker crafts a request using Node.js array syntax (?device[]=value) which causes the 'device' parameter to be parsed as an Array instead of a string
5. Attacker sends payload with array elements that bypass the string-based sanitization: ?device[]=x&device[]=y'-require('child_process').exec('curl...')-'
6. Server evaluates the unsanitized array in eval() context, executing arbitrary shell commands and exfiltrating /etc/passwd file

## Root cause
Multiple compounding flaws: (1) Use of eval() for template expression evaluation; (2) Sanitization logic that only handles string types and fails when input is an Array; (3) Lack of proper input type validation before passing to sanitization and eval functions; (4) No allowlist-based expression evaluation or safer template parsing mechanism

## Attacker mindset
Opportunistic security researcher who systematically fuzzes parameters to identify unusual server behavior, then performs code review of identified technologies to understand their internals and find exploitable patterns. The attacker recognized that type-based vulnerabilities (Array vs String) could bypass character-level filtering—a sophisticated bypass technique.

## Defensive takeaways
- Never use eval() or similar dynamic code execution for template processing; use safe templating engines with restricted expression evaluation
- Apply input validation and sanitization consistently across all possible input types (strings, arrays, objects), not just strings
- Validate and enforce expected parameter types at the framework level before processing user input
- Use allowlist-based filtering instead of blacklist-based character encoding where possible
- Implement Content Security Policy (CSP) headers to limit impact of template injection
- Keep template engine dependencies updated and monitor for security advisories
- Perform security code review of template engine helpers and understand their implementation before use
- Consider using template engines specifically designed with security (sandboxing) as a primary feature

## Variant hunting
['Search for other uses of eval() or Function() constructor in Node.js applications, especially in template processing contexts', 'Identify other template engines (EJS, Handlebars, Jade/Pug) that may have similar eval-based helper implementations', 'Test array/object parameter parsing bypasses on sanitization filters across different frameworks (Express, Fastify, etc.)', 'Look for type-confusion vulnerabilities where string sanitization is applied to other data types', 'Hunt for similar issues in other PayPal services and legacy applications using old Dust.js versions', "Check for 'if' helper usage patterns in production Dust.js templates that might be exploitable with this technique"]

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1059.008: Command and Scripting Interpreter - Node.js
- T1203: Exploitation for Client Execution
- T1210: Exploitation of Remote Services

## Notes
This is a textbook case of defense-in-depth failure. While PayPal attempted sanitization, they failed to account for JavaScript's dynamic typing. The researcher's systematic fuzzing approach and understanding of Node.js internals were crucial to discovering this high-impact vulnerability. The public availability of Dust.js source code on GitHub enabled the attacker to understand the vulnerability mechanism. This incident highlights why eval() and similar constructs are considered security anti-patterns in modern secure coding practices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
