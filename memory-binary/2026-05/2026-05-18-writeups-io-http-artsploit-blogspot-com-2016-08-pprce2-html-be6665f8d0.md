# PayPal Node.js Dust.js Template Injection RCE

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Template Injection, Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A critical code injection vulnerability was discovered in PayPal's demo.paypal.com using the Dust.js templating engine. By exploiting type confusion in parameter parsing combined with incomplete input sanitization in the Dust.js 'if' helper which uses eval(), an attacker could achieve remote code execution.

## Attack scenario (step by step)
1. Attacker performs fuzzing of HTTP parameters and notices different error responses for backslash (\) and newline (%0a) characters, identifying Dust.js templating engine in use
2. Attacker examines Dust.js source code and discovers the 'if' helper internally uses JavaScript eval() for expression evaluation
3. Attacker identifies that single and double quotes are HTML-encoded as sanitization, but tests if parameter type confusion could bypass this protection
4. Attacker sends a request with array syntax (device[]=value) which causes Node.js qs module to parse the parameter as an Array instead of a String
5. Attacker crafts payload device[]=x&device[]=y'-require('child_process').exec(...)-' which bypasses sanitization because Array.toString() is not subject to the quote encoding logic
6. The unsanitized array value reaches eval() in the Dust.js 'if' helper, allowing arbitrary JavaScript code execution and shell command execution

## Root cause
Multiple layers of vulnerability: (1) Use of eval() in Dust.js 'if' helper for expression evaluation, (2) Incomplete input sanitization that only handles String type inputs and relies on character encoding, (3) Type confusion between String and Array parameters that bypasses the sanitization layer, (4) No context-aware escaping or sandboxing of template expressions

## Attacker mindset
Methodical fuzzer who explores unexpected server responses to identify backend technologies, then conducts source code analysis to understand implementation details. Demonstrates deep knowledge of Node.js runtime behavior (qs module parsing, Array.toString() behavior) to craft a bypass. Shows understanding of security boundaries and how type confusion can defeat character-level sanitization.

## Defensive takeaways
- Never use eval() for untrusted template expressions; use safe expression evaluators or sandboxed contexts instead
- Implement type-agnostic input validation that handles all possible input types (strings, arrays, objects) consistently
- Sanitize input at the earliest point of entry and maintain invariants throughout processing
- Use allowlists for template syntax rather than blacklisting dangerous characters
- Apply defense-in-depth: even if one sanitization layer is bypassed, subsequent layers should catch malicious input
- Upgrade dependencies regularly; this vulnerability was fixed in newer versions of Dust.js
- Implement Content Security Policy and other runtime protections to limit impact of code injection
- Use static analysis tools to detect eval() usage and flag it for review

## Variant hunting
Search for: (1) Other Dust.js applications using outdated versions with the vulnerable 'if' helper, (2) Similar eval()-based expression evaluators in other templating engines, (3) Other Node.js applications using qs module with insufficient type-aware sanitization, (4) Template injection in other PayPal domains or subdomain, (5) Parameter pollution or type confusion in other template engines (Jade, EJS, Handlebars), (6) Similar issues where sanitization is String-specific but input parsing supports multiple types

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter (Node.js)
- T1203: Exploitation for Client Execution
- T1569: System Services (exec through child_process)
- T1070: Indicator Removal (could use for log tampering post-exploitation)

## Notes
Discovered August 2016. Demonstrates importance of type confusion vulnerabilities in security validation. The vulnerability chain required understanding of three distinct systems: (1) Dust.js templating, (2) Node.js qs module parsing behavior, (3) JavaScript Array.toString() coercion. This is a classic example of how defensive layers must account for all input types, not just the 'expected' type.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
